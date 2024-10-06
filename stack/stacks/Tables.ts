import { StackContext, Table } from "sst/constructs";

export function Tables({ stack }: StackContext) {
  const orgDetails = new Table(stack, "orgDetails", {
    fields: {
        orgId: "string",
        orgName: "string",
    },
    primaryIndex: { partitionKey: "orgId" },
    globalIndexes: {
        orgConfig: {
            partitionKey: "orgName",
            projection: ["userPoolId", "appClientId"],
        },
    },
  });
  const orgUserMapping = new Table(stack, "orgUserMapping", {
    fields: {
        orgId: "string",
        userName: "string",
    },
    primaryIndex: { partitionKey: "orgId", sortKey: "userName" },
    globalIndexes: {
        UserName: {
            partitionKey: "userName",
            sortKey: "orgId",
            projection: "all",
        },
    },
  });
  stack.addOutputs({
    orgDetails: orgDetails.tableName,
    orgUserMapping: orgUserMapping.tableName,
  });
  return {
    orgDetails, orgUserMapping,
  };
}