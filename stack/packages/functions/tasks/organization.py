# demo by safelyup.net
import boto3
import os
import common.api_utils as utils

APP_NAME = os.environ['APP_NAME']
dynamodb = boto3.resource('dynamodb')

def registration(org_details, marketplaceInfo):
    mgmt = OrgManagement()
    user_pool_response = mgmt.create_user_pool(org_details['orgId'])
    user_pool_id = user_pool_response['UserPool']['Id']
    app_client_response = mgmt.create_user_pool_client(user_pool_id)
    app_client_id = app_client_response['UserPoolClient']['ClientId']
    mgmt.create_user_pool_domain(user_pool_id, org_details['orgId'])
    org_user_group_response = mgmt.create_user_group(user_pool_id, org_details['orgId'], "User group for org {0}".format(org_details['orgId']))
    org_admin_user_name = 'admin'
    mgmt.create_org_admin(user_pool_id, org_admin_user_name, org_details)
    mgmt.add_user_to_group(user_pool_id, org_admin_user_name, org_user_group_response['Group']['GroupName'])
    org_details['userPoolId'] = user_pool_id
    org_details['appClientId'] = app_client_id
    org_details['orgAdminUserName'] = org_admin_user_name
    mgmt.create_org_records(org_details, marketplaceInfo)
    return True

def get_all():
    table_org_details = dynamodb.Table(os.environ['TABLE_ORGDETAILS'])
    response = table_org_details.scan()
    return response['Items']

def get(orgId):
    table_org_details = dynamodb.Table(os.environ['TABLE_ORGDETAILS'])
    org_details = table_org_details.get_item(
        Key={
            'orgId': orgId,
        },
        AttributesToGet=[
            'orgId',
            'orgName',
            'orgAddress',
            'orgEmail',
            'orgPhone',
            'orgTier',
            'isActive',
        ]
    )
    if 'Item' in org_details:
        return org_details['Item']
    return None

def update(org_details):
    validAttrs = ['orgName', 'orgAddress', 'orgEmail', 'orgPhone', 'orgTier']
    table_org_details = dynamodb.Table(os.environ['TABLE_ORGDETAILS'])
    exiting_org_details = table_org_details.get_item(
        Key={
            'orgId': org_details['orgId'],
        },
        AttributesToGet=validAttrs
    )
    if 'Item' not in exiting_org_details:
        return None
    expression = []
    expressionVals = {}
    for i in validAttrs:
        if org_details.get(i, None) is not None:
            if exiting_org_details['Item'][i] == org_details[i]:
                continue
            expression.append(i + '=:' + i) 
            expressionVals[':' + i] = org_details[i]
    if len(expression) == 0:
        return None
    result = table_org_details.update_item(
        Key={
            'orgId': org_details['orgId'],
        },
        UpdateExpression='set ' + ','.join(expression),
        ExpressionAttributeValues=expressionVals,
        ReturnValues="UPDATED_NEW"
    )
    return result["Attributes"]

def deactivate(orgId):
    table_org_details = dynamodb.Table(os.environ['TABLE_ORGDETAILS'])
    exiting_org_details = table_org_details.get_item(
        Key={
            'orgId': orgId,
        },
        AttributesToGet=['isActive']
    )
    if 'Item' not in exiting_org_details:
        return None
    if exiting_org_details['Item']['isActive'] == False:
        return None
    result = table_org_details.update_item(
        Key={
            'orgId': orgId,
        },
        UpdateExpression="set isActive = :isActive",
        ExpressionAttributeValues={
            ':isActive': False
        },
        ReturnValues="UPDATED_NEW"
    )
    return result["Attributes"]

def activate(orgId):
    table_org_details = dynamodb.Table(os.environ['TABLE_ORGDETAILS'])
    exiting_org_details = table_org_details.get_item(
        Key={
            'orgId': orgId,
        },
        AttributesToGet=['isActive']
    )
    if 'Item' not in exiting_org_details:
        return None
    if exiting_org_details['Item']['isActive'] == True:
        return None
    result = table_org_details.update_item(
        Key={
            'orgId': orgId,
        },
        UpdateExpression="set isActive = :isActive",
        ExpressionAttributeValues={
            ':isActive': True
        },
        ReturnValues="UPDATED_NEW"
    )
    return result["Attributes"]

class OrgManagement():
    def __init__(self) -> None:
        self.cognito_client = boto3.client('cognito-idp')

    def create_user_pool(self, org_id):
        application_site_url = os.environ['ORG_USER_POOL_CALLBACK_URL']
        email_message = ''.join(["Login at ", application_site_url,
                        " with your username: {username} and temporary password: {####}"])
        email_subject = "Your temporary password"  
        response = self.cognito_client.create_user_pool(
            PoolName = APP_NAME + '-' + org_id,
            AutoVerifiedAttributes = ['email'],
            AccountRecoverySetting = {
                'RecoveryMechanisms': [
                    {
                        'Priority': 1,
                        'Name': 'verified_email'
                    },
                ]
            },
            Schema = [
                {
                    'Name': 'email',
                    'AttributeDataType': 'String',
                    'Required': True,                    
                },
                {
                    'Name': 'orgId',
                    'AttributeDataType': 'String',
                    'Required': False,                    
                },            
                {
                    'Name': 'userRole',
                    'AttributeDataType': 'String',
                    'Required': False,                    
                }
            ],
            AdminCreateUserConfig = {
                'InviteMessageTemplate': {
                    'EmailMessage': email_message,
                    'EmailSubject': email_subject
                }
            }
        )    
        return response

    def create_user_pool_client(self, user_pool_id):
        user_pool_callback_url = os.environ['ORG_USER_POOL_CALLBACK_URL']
        response = self.cognito_client.create_user_pool_client(
            UserPoolId = user_pool_id,
            ClientName = APP_NAME,
            GenerateSecret = False,
            AllowedOAuthFlowsUserPoolClient = True,
            AllowedOAuthFlows = [
                'code', 'implicit'
            ],
            SupportedIdentityProviders = [
                'COGNITO',
            ],
            CallbackURLs = [
                user_pool_callback_url,
            ],
            LogoutURLs = [
                user_pool_callback_url,
            ],
            AllowedOAuthScopes = [
                'email',
                'openid',
                'profile'
            ],
            WriteAttributes = [
                'email',
                'custom:orgId',
                'custom:userRole'
            ]
        )
        return response

    def create_user_pool_domain(self, user_pool_id, org_id):
        response = self.cognito_client.create_user_pool_domain(
            Domain=APP_NAME + '-' + org_id,
            UserPoolId=user_pool_id
        )
        return response

    def create_user_group(self, user_pool_id, group_name, group_description):
        response = self.cognito_client.create_group(
            GroupName=group_name,
            UserPoolId=user_pool_id,
            Description=group_description,
            Precedence=0
        )
        return response

    def create_org_admin(self, user_pool_id, org_admin_user_name, user_details):
        response = self.cognito_client.admin_create_user(
            Username=org_admin_user_name,
            UserPoolId=user_pool_id,
            ForceAliasCreation=True,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': user_details['orgEmail']
                },
                {
                    'Name': 'email_verified',
                    'Value': 'true'
                },
                {
                    'Name': 'custom:userRole',
                    'Value': utils.UserRoles.ORG_ADMIN
                },            
                {
                    'Name': 'custom:orgId',
                    'Value': user_details['orgId']
                }
            ]
        )
        return response

    def add_user_to_group(self, user_pool_id, user_name, group_name):
        response = self.cognito_client.admin_add_user_to_group(
            UserPoolId=user_pool_id,
            Username=user_name,
            GroupName=group_name
        )
        return response

    def create_org_records(self, org_details, marketplaceInfo):
        table_org_details = dynamodb.Table(os.environ['TABLE_ORGDETAILS'])
        table_org_user_map = dynamodb.Table(os.environ['TABLE_ORGUSERMAP'])
        table_org_details.put_item(
            Item = {
                'orgId': org_details['orgId'],
                'orgName': org_details['orgName'],
                'orgAddress': org_details.get('orgAddress', ''),
                'orgEmail': org_details['orgEmail'],
                'orgPhone': org_details.get('orgPhone', ''),
                'orgTier': org_details['orgTier'],
                'userPoolId': org_details['userPoolId'],
                'appClientId': org_details['appClientId'],
                'awsmpProductCode': marketplaceInfo['ProductCode'],
                'awsmpCustomerIdentifier': marketplaceInfo['CustomerIdentifier'],
                'awsmpCustomerAWSAccountId': marketplaceInfo['CustomerAWSAccountId'],
                'isActive': True
            }
        )
        table_org_user_map.put_item(
            Item = {
                'orgId': org_details['orgId'],
                'userName': org_details['orgAdminUserName']
            }
        )
        return True
