#!/bin/bash

# Investment Advisor CDK Deployment Script
# Make sure you have the necessary AWS permissions before running this script

set -e

echo "🚀 Starting Investment Advisor CDK Deployment..."

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Install/update dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Set AWS profile
AWS_PROFILE="Juanelo"
echo "🔑 Using AWS profile: $AWS_PROFILE"

# Bootstrap CDK (if not already done)
echo "🏗️  Bootstrapping CDK..."
cdk bootstrap --profile $AWS_PROFILE || echo "⚠️  Bootstrap failed - you may need additional permissions"

# Synthesize the stack
echo "🔍 Synthesizing CloudFormation template..."
cdk synth --profile $AWS_PROFILE

# Deploy the stack
echo "🚀 Deploying Investment Advisor stack..."
cdk deploy --profile $AWS_PROFILE --require-approval never

echo "✅ Deployment completed!"
echo ""
echo "📋 Stack Outputs:"
echo "   - Check AWS Console for S3 buckets, Lambda functions, and IAM roles"
echo "   - Investment Data Bucket: investment-advisor-data-944308403469-us-east-1"
echo "   - Knowledge Base Bucket: investment-advisor-kb-944308403469-us-east-1"
echo ""
echo "🔧 Next Steps:"
echo "   1. Upload investment documents to the Knowledge Base bucket"
echo "   2. Test Lambda functions via AWS Console"
echo "   3. Configure Bedrock Knowledge Base with OpenSearch Serverless"
echo "   4. Create Bedrock Agent for investment advisory"
