# demo by safelyup.net
import json
import common.api_utils as utils
import common.schemas as schemas
import common.validator as validator
import tasks.subscription
import tasks.organization


@validator.input(schema=schemas.ORG_SUBSCRIBE)
def aws(event, context):
    try:
        # https://github.com/aws-samples/aws-marketplace-serverless-saas-integration/blob/master/src/register-new-subscriber.js
        # https://docs.aws.amazon.com/marketplace/latest/userguide/saas-code-examples.html#saas-resolvecustomer-example
        org_details = json.loads(event['body'])
        org_details['orgId'] = utils.randomKey(16).lower()
        marketplaceInfo = tasks.subscription.aws(org_details['registrationToken'])
        tasks.organization.registration(org_details, marketplaceInfo)
    except Exception as e:
        return validator.resp_failure('Error registering a new organization' + str(e))
    else:
        return validator.resp_success("organization has been registered")
