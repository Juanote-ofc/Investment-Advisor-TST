# AWS Permissions Request for CDK Deployment

**Subject:** Request for AWS CDK Permissions - Investment Advisor Project

**To:** [AWS Administrator]
**From:** Juanelo
**Date:** August 11, 2025

---

## Request Summary
I need additional AWS permissions to deploy infrastructure for the Investment Advisor project using AWS CDK.

## Current Issue
My AWS user (`Juanelo` - Account: 944308403469) lacks the necessary permissions to:
1. Bootstrap AWS CDK
2. Deploy CloudFormation stacks
3. Access SSM parameters required by CDK

## Specific Error Messages
```
AccessDenied: User: arn:aws:iam::944308403469:user/Juanelo is not authorized to perform: 
- cloudformation:DescribeStacks
- ssm:GetParameter on resource: arn:aws:ssm:us-east-1:944308403469:parameter/cdk-bootstrap/hnb659fds/version
```

## Recommended Solution
**Option 1 (Simplest):** Attach the AWS managed policy `PowerUserAccess`
- Policy ARN: `arn:aws:iam::aws:policy/PowerUserAccess`
- This provides full access to AWS services except IAM user/group management

**Option 2 (More Restrictive):** Attach the custom policy in the file `required-permissions.json`
- This provides only the minimum permissions needed for CDK deployment

## Project Details
- **Project:** Investment Advisor AI System
- **Technology Stack:** AWS CDK, Lambda, S3, Bedrock, CloudFormation
- **Resources to Deploy:**
  - 2 S3 Buckets
  - 2 Lambda Functions
  - 3 IAM Roles
  - 1 Bedrock Knowledge Base
  - CloudWatch Log Groups

## Business Justification
This infrastructure supports an AI-powered investment advisory system that will:
- Analyze investment scenarios using Amazon Bedrock
- Optimize portfolio allocations
- Store investment data securely in S3
- Provide scalable serverless computing via Lambda

## Timeline
**Urgent:** Development is blocked until permissions are granted.

## Files Attached
- `required-permissions.json` - Minimum required permissions policy
- `README.md` - Full project documentation

---

**Contact Information:**
- User: Juanelo
- AWS Account: 944308403469
- Region: us-east-1
- Email: [your-email]

Thank you for your assistance with this request.
