import { SSTConfig } from "sst";
import { OpsAuth } from "./stacks/OpsAuth";
import { Tables } from "./stacks/Tables";
import { API } from "./stacks/API";
import { Frontend } from "./stacks/Frontend";

export default {
  config(_input) {
    return {
      name: "example",
      region: "us-east-1"
    };
  },
  stacks(app) {
    app.stack(OpsAuth).stack(Tables).stack(API).stack(Frontend);
  }
} satisfies SSTConfig;
