#!/usr/bin/env python3
from warrant import Cognito

def auth_user(userPoolId, userPoolClientId, username, password):
    u = Cognito(userPoolId, userPoolClientId, user_pool_region="us-east-1", username=username)
    u.authenticate(password=password)
    #user = u.get_user(attr_map={"given_name":"first_name","family_name":"last_name"})
    return u.id_token

if __name__ == '__main__':
    print(auth_user("", "", "", ""))
