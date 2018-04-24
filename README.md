# aws-cost-notifier

[![CircleCI](https://circleci.com/gh/ytakahashi/aws-cost-notifier.svg?style=shield&circle-token=0c194c7ed2a65b5983ea0292196483067f317f72)](https://circleci.com/gh/ytakahashi/aws-cost-notifier)


AWS lambda function to check the cost and send a message to Slack.

## Description

This repository contains followings:
- lambda function 
  - checks AWS cloudwatch by calling [get-metric-statistics API](https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_GetMetricStatistics.html)
  - notifies the result via slack

- packaging script (Makefile)
  - compresses a python script and its dependent modules in a zip file

- deploy script ([AWS SAM](https://github.com/awslabs/serverless-application-model))
  - deploys a zip file to AWS Lambda and creates an event to trigger the Lambda function using AWS cloudformation


## Requirement

### Lambda function

#### Environment

- Python version >= 3.6
- Pipenv 

#### AWS IAM Policy

|  Resource           |  Permission            |
| ------------------- | ---------------------- |
|  cloudwatch         |  GetMetricStatistics   |

When running on AWS Lambda, a role attached to the lambda function should have following policy:

- AWSLambdaExecute


### Deploy script

#### Environment

- aws cli

#### AWS IAM Policy

|  Resource           |  Permission            |
| ------------------- | ---------------------- |
|  IAM                |  PassRole              |
|  S3                 |  PutObject, GetObject  |
|  Lambda             |  Write                 |
|  Cloudformation     |  Write                 |
|  Cloudwatch Events  |  Write                 |
|  Cloudwatch Logs    |  Write                 |


## Install

Run the command below to build script.

```Console
pipenv install -d
```

## Deploy

Lambda function is created by following steps.

1. Create a deployment artifact (zip file)

```Console
make
```

2. Uploading a local artifact (ZIP file) to an S3 bucket 

```Console
aws cloudformation package [ --profile PROFILE ] --template-file deploy.yml \
--s3-bucket S3_BUCKET_NAME \
--output-template-file deploy-output.yml
```

- `PROFILE`: if you use named profile stored in the config and credentials files, specify the profile name
- `S3_BUCKET_NAME`: bucket name of S3 used to upload an artifact

3. Deploying resources

```Console
aws cloudformation deploy [ --profile PROFILE ] --template-file ./deploy-output.yml \
--stack-name CFN_STACK_NAME \
--parameter-overrides \
IAMRole='LAMBDA_FUNCTION_ROLE' \
SlackWebhookUrl='SLACK_WEBHOOK_URL'
```
- `PROFILE`: if you use named profile stored in the config and credentials files, specify the profile name
- `CFN_STACK_NAME`: stack name of cloudformation
- `LAMBDA_FUNCTION_ROLE`: role ARN attached to a lambda function to be created
- `SLACK_WEBHOOK_URL`: incoming webhook URL generated by Slack

