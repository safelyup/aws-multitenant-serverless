# demo by safelyup.net
import json
import os
import urllib.request
import boto3
import time
import common.api_utils as utils
from jose import jwk, jwt
from jose.utils import base64url_decode
from aws_lambda_powertools.utilities.data_classes import event_source
from aws_lambda_powertools.utilities.data_classes.api_gateway_authorizer_event import (
    DENY_ALL_RESPONSE,
    APIGatewayAuthorizerRequestEvent,
    APIGatewayAuthorizerResponse,
)

region = os.environ['AWS_REGION']
dynamodb = boto3.resource('dynamodb')
table_org_details = dynamodb.Table(os.environ['TABLE_ORGDETAILS'])
user_pool_operation_user = os.environ['OPERATION_USERS_USER_POOL']
app_client_operation_user = os.environ['OPERATION_USERS_APP_CLIENT']


@event_source(data_class=APIGatewayAuthorizerRequestEvent)
def handler(event: APIGatewayAuthorizerRequestEvent, context):
    user = get_user_by_token(event.get_header_value("Authorization"))
    if user is None:
        # No user was found
        # to return 401 - `{"message":"Unauthorized"}`, but pollutes lambda error count metrics
        # raise Exception("Unauthorized")
        # to return 403 - `{"message":"Forbidden"}`
        return DENY_ALL_RESPONSE
    # parse the `methodArn` as an `APIGatewayRouteArn`
    arn = event.parsed_arn
    # Create the response builder from parts of the `methodArn`
    # and set the logged in user id and context
    policy = APIGatewayAuthorizerResponse(
        principal_id=user["principal_id"],
        context=user,
        region=arn.region,
        aws_account_id=arn.aws_account_id,
        api_id=arn.api_id,
        stage=arn.stage,
    )
    # Conditional IAM Policy
    if utils.isSaaSProvider(user["userRole"]):
        policy.allow_all_routes()
    elif utils.isOrgAdmin(user["userRole"]):
        policy.allow_route('GET', "organization/" + user["orgId"])
        policy.allow_route('PUT', "organization/" + user["orgId"])
        policy.allow_route('PUT', "organization/deactivate/" + user["orgId"])
    #else:
    #    policy.allow_route('GET', "user/*")
    #    policy.allow_route('PUT', "user/*")
    return policy.asdict()


def get_user_by_token(token):
    try:
        token = token.split(" ")
        if (token[0] != 'Bearer'):
            return None
        jwt_bearer_token = token[1]
        unauthorized_claims = jwt.get_unverified_claims(jwt_bearer_token)
        if(utils.isSaaSProvider(unauthorized_claims['custom:userRole'])):
            userpool_id = user_pool_operation_user
            appclient_id = app_client_operation_user
        else:
            # get org user pool and app client to validate jwt token against
            org_details = table_org_details.get_item(
                Key ={
                    'orgId': unauthorized_claims['custom:orgId']
                }
            )
            userpool_id = org_details['Item']['userPoolId']
            appclient_id = org_details['Item']['appClientId']
        # get keys for user pool to validate
        keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)
        with urllib.request.urlopen(keys_url) as f:
            response = f.read()
        keys = json.loads(response.decode('utf-8'))['keys']
        # authenticate against cognito user pool using the key
        response = _validateJWT(jwt_bearer_token, appclient_id, keys)
        if (response == False):
            return None 
        user_name = response["cognito:username"]
        org_id = response["custom:orgId"]
        user_role = response["custom:userRole"]
        principal_id = response["sub"]
    except Exception as e:
        return None
    context = {
        'principal_id': principal_id,
        'userName': user_name,
        'orgId': org_id,
        'userPoolId': userpool_id,
        'userRole': user_role
    }
    return context


def _validateJWT(token, app_client_id, keys):
    # get the kid from the headers prior to verification
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']
    # search for the kid in the downloaded public keys
    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        return False
    # construct the public key
    public_key = jwk.construct(keys[key_index])
    # get the last two sections of the token, message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit('.', 1)
    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        return False
    # since we passed the verification, we can now safely use the unverified claims
    claims = jwt.get_unverified_claims(token)
    # additionally we can verify the token expiration
    if time.time() > claims['exp']:
        return False
    # and the Audience (use claims['client_id'] if verifying an access token)
    if claims['aud'] != app_client_id:
        return False
    return claims
