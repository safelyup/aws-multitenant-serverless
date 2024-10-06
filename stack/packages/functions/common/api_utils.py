import string
import random

class UserRoles:
    SYSTEM_ADMIN     = "SystemAdmin"
    CUSTOMER_SUPPORT = "CustomerSupport"
    ORG_ADMIN        = "OrgAdmin"    
    ORG_USER         = "OrgUser"

def isOrgAdmin(user_role):
    return (user_role == UserRoles.ORG_ADMIN)

def isSystemAdmin(user_role):
    return (user_role == UserRoles.SYSTEM_ADMIN)

def isSaaSProvider(user_role):
    return (user_role == UserRoles.SYSTEM_ADMIN or user_role == UserRoles.CUSTOMER_SUPPORT)

def isOrgUser(user_role):
    return (user_role == UserRoles.ORG_USER)

def randomKey(keysize=16):
    return ''.join(random.choice(
        string.ascii_letters + string.digits) for _ in range(keysize))
