import { StackContext, Cognito } from "sst/constructs";
import * as cognito from "aws-cdk-lib/aws-cognito";

export function OpsAuth({ stack }: StackContext) {
  const callbackURLs = stack.stage === "prod" ? ["https://app.example.org/"] : [`https://app${stack.stage}.dev.example.org/`, "http://localhost:3000/"]
  const pool = new Cognito(stack, "opsAuth", {
    cdk: {
      userPool: {
        selfSignUpEnabled: false,
        autoVerify: { email: true, phone: false },
        accountRecovery: cognito.AccountRecovery.EMAIL_ONLY,
        standardAttributes: {
          email: { required: true, mutable: true },
        },
        customAttributes: {
          userRole: new cognito.StringAttribute({ mutable: true }),
          orgId: new cognito.StringAttribute({ mutable: true }),
        },
        signInAliases: {username: false, email: true},
        mfa: cognito.Mfa.OPTIONAL,
        mfaSecondFactor: { sms: false, otp: true },
      },
      userPoolClient: {
        generateSecret: false,
        writeAttributes: (new cognito.ClientAttributes())
          .withStandardAttributes({email: true})
          .withCustomAttributes('orgId', 'userRole'),
        supportedIdentityProviders: [cognito.UserPoolClientIdentityProvider.COGNITO,],
        oAuth: {
          flows: {
            authorizationCodeGrant: true,
            implicitCodeGrant: true,
          },
          callbackUrls: callbackURLs,
          logoutUrls: callbackURLs,
          scopes: [cognito.OAuthScope.EMAIL, cognito.OAuthScope.OPENID, cognito.OAuthScope.PROFILE],
        },
      },
    },
  });
  pool.cdk.userPool.addDomain('CognitoDomain', {
    cognitoDomain: {
      domainPrefix: stack.stage === "prod" ? "example" : `example-${stack.stage}`,
    },
  });
  const adminUser = new cognito.CfnUserPoolUser(stack, 'AdminUser', {
    userPoolId: pool.userPoolId,
    desiredDeliveryMediums: ['EMAIL'],
    forceAliasCreation: true,
    username: 'exampleadmin@gmail.com',
    userAttributes: [
      {
        name: 'email',
        value: 'exampleadmin@gmail.com',
      },
      {
        name: 'email_verified',
        value: 'true'
      },
      {
        name: 'custom:orgId',
        value: 'system_admins',
      },
      {
        name: 'custom:userRole',
        value: 'SystemAdmin',
      },
    ],
  });
  stack.addOutputs({
    userPoolId: pool.userPoolId,
    userPoolClientId: pool.userPoolClientId,
  });
  return {
    pool,
  };
}
