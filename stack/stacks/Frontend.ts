import { StackContext, StaticSite, use } from "sst/constructs";
import { API } from "./API";

export function Frontend({ stack }: StackContext) {
  const { api } = use(API);
  const frontend = new StaticSite(stack, "frontend", {
    path: "packages/frontend/",
    customDomain: stack.stage === "prod" ? "app.example.org" : `app${stack.stage}.dev.example.org`,
    buildOutput: "dist",
    buildCommand: "npm run build",
    errorPage: "redirect_to_index_page",
    environment: {
      VITE_APP_API_URL: String(api.customDomainUrl),
    },
  });
}
