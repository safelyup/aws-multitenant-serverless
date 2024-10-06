# demo by safelyup.net
import json
import common.api_utils as utils
import common.schemas as schemas
import common.validator as validator
import tasks.organization


@validator.input(schema=schemas.ORG_INSERT)
def registration(event, context):
    try:
        userRole = event['requestContext']['authorizer']['lambda']['userRole']
        if not utils.isSaaSProvider(userRole):
            return validator.resp_forbidden()
        org_details = json.loads(event['body'])
        org_details['orgId'] = utils.randomKey(16).lower()
        tasks.organization.registration(org_details)
    except Exception as e:
        return validator.resp_failure('Error registering a new organization' + str(e))
    else:
        return validator.resp_success("organization has been registered")

def get_all(event, context):
    try:
        userRole = event['requestContext']['authorizer']['lambda']['userRole']
        if not utils.isSaaSProvider(userRole):
            return validator.resp_forbidden()
        result = tasks.organization.get_all()
    except Exception as e:
        return validator.resp_failure('Error getting all organizations')
    return validator.resp_success(result)

def get(event, context):
    try:
        requester_orgId = event['requestContext']['authorizer']['lambda']['orgId']    
        userRole = event['requestContext']['authorizer']['lambda']['userRole']
        orgId = event['pathParameters']['id']
        if not (utils.isOrgAdmin(userRole) and orgId == requester_orgId) and (not utils.isSaaSProvider(userRole)):
            return validator.resp_forbidden()
        result = tasks.organization.get(orgId)
        if result is None:
            return validator.resp_notfound("organization not found")
    except Exception as e:
        return validator.resp_failure('Error getting organization')
    return validator.resp_success(result)

@validator.input(schema=schemas.ORG_UPDATE)
def update(event, context):
    try:
        requester_orgId = event['requestContext']['authorizer']['lambda']['orgId']    
        userRole = event['requestContext']['authorizer']['lambda']['userRole']
        orgId = event['pathParameters']['id']
        if not (utils.isOrgAdmin(userRole) and orgId == requester_orgId) and (not utils.isSaaSProvider(userRole)):
            return validator.resp_forbidden()
        org_details = json.loads(event['body'])
        org_details['orgId'] = orgId
        result = tasks.organization.update(org_details)
        if result is None:
            return validator.resp_failure("organization not updated")
    except Exception as e:
        return validator.resp_failure('Error updating organization'+str(e))
    return validator.resp_success(result)

def deactivate(event, context):
    try:
        requester_orgId = event['requestContext']['authorizer']['lambda']['orgId']    
        userRole = event['requestContext']['authorizer']['lambda']['userRole']
        orgId = event['pathParameters']['id']
        if not (utils.isOrgAdmin(userRole) and orgId == requester_orgId) and (not utils.isSaaSProvider(userRole)):
            return validator.resp_forbidden()
        result = tasks.organization.deactivate(orgId)
        if result is None:
            return validator.resp_failure("organization not updated")
    except Exception as e:
        return validator.resp_failure('Error updating organization'+str(e))
    return validator.resp_success(result)

def activate(event, context):
    try:
        userRole = event['requestContext']['authorizer']['lambda']['userRole']
        if not utils.isSaaSProvider(userRole):
            return validator.resp_forbidden()
        orgId = event['pathParameters']['id']
        result = tasks.organization.activate(orgId)
        if result is None:
            return validator.resp_failure("organization not updated")
    except Exception as e:
        return validator.resp_failure('Error updating organization'+str(e))
    return validator.resp_success(result)
