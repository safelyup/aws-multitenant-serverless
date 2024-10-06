import { StackContext, Api, Function, use } from "sst/constructs";
import { OpsAuth } from "./OpsAuth";
import { Tables } from "./Tables";

export function API({ stack }: StackContext) {
  const { pool } = use(OpsAuth);
  const { orgDetails, orgUserMapping } = use(Tables);
  const api = new Api(stack, "api", {
    customDomain: {
      domainName: stack.stage === "prod" ? "api.example.org" : `api${stack.stage}.dev.example.org`,
      path: "v1",
    },
    defaults: {
      authorizer: "CustomAuthr",
      function: {
        runtime: "python3.9",
        architecture: "arm_64",
        timeout: "10 seconds",
        memorySize: "256 MB",
        logRetention: "one_day",
        environment: {
          LOG_LEVEL: "ERROR",
          APP_NAME: stack.stage === "prod" ? "example" : `example${stack.stage}`,
          TABLE_ORGDETAILS: orgDetails.tableName,
          TABLE_ORGUSERMAP: orgUserMapping.tableName,
        },
        permissions: [],
      },
    },
    authorizers: {
      CustomAuthr: {
        type: "lambda",
        function: new Function(stack, "authorizer", {
          handler: "packages/functions/authorizer.handler",
          runtime: "python3.9",
          architecture: "arm_64",
          memorySize: "256 MB",
          timeout: "10 seconds",
          permissions: ["cognito-idp:List*", orgDetails],
          environment: {
            OPERATION_USERS_USER_POOL: pool.userPoolId,
            OPERATION_USERS_APP_CLIENT: pool.userPoolClientId,
            TABLE_ORGDETAILS: orgDetails.tableName,
          },
        }),
        //resultsCacheTtl: "300 seconds",
      },
    },
    routes: {
      "POST /subscription/aws": {
        function: {
          handler: "packages/functions/subscription.aws",
          environment: {
            ORG_USER_POOL_CALLBACK_URL: stack.stage === "prod" ? "https://app.example.org/" : `https://app${stack.stage}.dev.example.org/`,
          },
          permissions: [orgDetails, orgUserMapping, "cognito-idp:*"],
        },
        authorizer: "none",  // public endpoint
      },
      "POST /organization": {
        function: {
          handler: "packages/functions/organization.registration",
          environment: {
            ORG_USER_POOL_CALLBACK_URL: stack.stage === "prod" ? "https://app.example.org/" : `https://app${stack.stage}.dev.example.org/`,
          },
          permissions: [orgDetails, orgUserMapping, "cognito-idp:*"],
        },
      },
      "GET /organization": {
        function: {
          handler: "packages/functions/organization.get_all",
          permissions: [orgDetails],
        }
      },
      "GET /organization/{id}": {
        function: {
          handler: "packages/functions/organization.get",
          permissions: [orgDetails],
        }
      },
      "PUT /organization/{id}": {
        function: {
          handler: "packages/functions/organization.update",
          permissions: [orgDetails],
        }
      },
      "PUT /organization/deactivate/{id}": {
        function: {
          handler: "packages/functions/organization.deactivate",
          permissions: [orgDetails],
        }
      },
      "PUT /organization/activate/{id}": {
        function: {
          handler: "packages/functions/organization.activate",
          permissions: [orgDetails],
        }
      },
    },
  });
  stack.addOutputs({
    ApiEndpoint: api.url,
    ApiCustomEndpoint: api.customDomainUrl,
  });
  return {
    api,
  };
}
