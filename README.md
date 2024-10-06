# AWS-Multitenant-Serverless

A Full-Stack Multi-Tenant Serverless SaaS Demo Setup on AWS.

[SST Framework](https://sst.dev/) is being used in this project to build the full-stack setup on your AWS acount. The setup also support deployment to multiple "stages"; the `prod` stage (AWS account) and several development stages or accounts.

## Blog Post

For more info see the [Blog Post](https://safelyup.net/).

## Local Deployment to AWS

You need to update/create file `~/.aws/credentials` and include the keys to the AWS account that you want to use for deploying the demo setup.
```
[default]
aws_access_key_id =
aws_secret_access_key =
```

Next. deploy the setup and start the development console locally.
```
cd stack
npx sst dev
npx sst deploy --stage dev
npx sst console --stage dev
```

For any kind of `prod` setup it is recommended to use a platform like [Seed](https://seed.run/) instead of local deployment.

## Local Frontend Development

To start the [Vue3/Nuxt](https://nuxt.com/) frontend application locally:
```
cd packages/frontend
npm install
npm run dev
```
