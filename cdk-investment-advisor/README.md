# Investment Advisor CDK Stack

A comprehensive AWS CDK application for building an AI-powered investment advisory system using Amazon Bedrock, Lambda, S3, and other AWS services.

## 🏗️ Architecture

This CDK stack creates the following AWS resources:

### 📦 S3 Buckets
- **Investment Data Bucket**: Stores investment data, portfolios, and analysis results
- **Knowledge Base Bucket**: Stores documents for Bedrock Knowledge Base

### 🔧 Lambda Functions
- **Investment Analyzer**: Uses Bedrock to analyze investment scenarios and provide recommendations
- **Portfolio Optimizer**: Optimizes portfolio allocation based on risk tolerance and goals

### 🤖 Amazon Bedrock
- **Knowledge Base**: Vector database for investment advisory documents
- **Foundation Models**: Claude 3 Sonnet for investment analysis

### 🔐 IAM Roles
- **Lambda Execution Role**: Permissions for Lambda functions to access Bedrock and S3
- **Bedrock Agent Role**: Permissions for Bedrock agents to invoke Lambda functions

## 🚀 Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** configured with credentials
3. **Node.js** and **npm** installed
4. **Python 3.11+** installed
5. **AWS CDK** CLI installed globally

## 📋 Required AWS Permissions

Your AWS user needs the following permissions:
- `PowerUserAccess` (recommended) OR
- Custom policy with CloudFormation, S3, IAM, Lambda, and Bedrock permissions

## 🛠️ Setup Instructions

### 1. Clone and Navigate
```bash
cd cdk-investment-advisor
```

### 2. Activate Virtual Environment
```bash
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure AWS Profile
Make sure your AWS profile is set up:
```bash
aws configure list-profiles
# Should show 'Juanelo' profile
```

### 5. Bootstrap CDK (First Time Only)
```bash
cdk bootstrap --profile Juanelo
```

### 6. Deploy the Stack
```bash
# Option 1: Use the deployment script
./deploy.sh

# Option 2: Manual deployment
cdk deploy --profile Juanelo
```

## 📊 Stack Resources

### S3 Buckets
- `investment-advisor-data-{account}-{region}`: Investment data storage
- `investment-advisor-kb-{account}-{region}`: Knowledge base documents

### Lambda Functions
- `InvestmentAnalyzerFunction`: Analyzes investment scenarios
- `PortfolioOptimizerFunction`: Optimizes portfolio allocations

### IAM Roles
- `InvestmentAdvisorLambdaRole`: Lambda execution permissions
- `BedrockAgentRole`: Bedrock agent permissions

## 🧪 Testing the Functions

### Test Investment Analyzer Lambda
```json
{
  "investment_amount": 100000,
  "risk_tolerance": "moderate",
  "time_horizon": "10 years"
}
```

### Test Portfolio Optimizer Lambda
```json
{
  "portfolio": {
    "stocks": 70,
    "bonds": 20,
    "alternatives": 10
  }
}
```

## 🔧 Useful CDK Commands

- `cdk list` - List all stacks in the app
- `cdk synth` - Emits the synthesized CloudFormation template
- `cdk deploy` - Deploy this stack to your AWS account/region
- `cdk diff` - Compare deployed stack with current state
- `cdk destroy` - Remove the stack from your AWS account

## 📁 Project Structure

```
cdk-investment-advisor/
├── app.py                          # CDK app entry point
├── cdk_investment_advisor/
│   ├── __init__.py
│   └── cdk_investment_advisor_stack.py  # Main stack definition
├── requirements.txt                # Python dependencies
├── cdk.json                       # CDK configuration
├── deploy.sh                      # Deployment script
└── README.md                      # This file
```

## 🚨 Important Notes

### Development vs Production
- Current configuration uses `RemovalPolicy.DESTROY` for easy cleanup
- For production, change to `RemovalPolicy.RETAIN` for data safety

### Bedrock Knowledge Base
- Requires OpenSearch Serverless collection (not included in this stack)
- You'll need to create the collection separately and update the ARN

### Cost Considerations
- Bedrock model invocations are charged per token
- S3 storage costs apply
- Lambda execution costs apply

## 🔄 Next Steps

1. **Upload Documents**: Add investment research documents to the Knowledge Base bucket
2. **Configure OpenSearch**: Set up OpenSearch Serverless collection for the Knowledge Base
3. **Create Bedrock Agent**: Build a conversational agent using the Knowledge Base
4. **Add API Gateway**: Create REST API endpoints for the Lambda functions
5. **Build Frontend**: Create a web interface for the investment advisor

## 🐛 Troubleshooting

### Permission Errors
- Ensure your AWS user has `PowerUserAccess` or equivalent permissions
- Check that the `Juanelo` profile is properly configured

### Bedrock Model Access
- Ensure Bedrock models are enabled in your AWS region
- Request access to Claude 3 models if needed

### Knowledge Base Issues
- Create OpenSearch Serverless collection first
- Update the collection ARN in the stack

## 📞 Support

For issues with this CDK stack, check:
1. AWS CloudFormation console for deployment errors
2. Lambda function logs in CloudWatch
3. IAM permissions for your user and roles

## 🏷️ Tags and Metadata

- **Project**: Investment Advisor
- **Technology**: AWS CDK, Python, Bedrock, Lambda
- **Environment**: Development
- **Owner**: Juanelo
