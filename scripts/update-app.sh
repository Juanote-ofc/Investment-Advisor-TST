#!/bin/bash

# Investment Advisor - Update Deployed Application
# Updates the ECS service with the latest Streamlit app changes

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
AWS_REGION="us-east-1"
AWS_PROFILE="Juanelo"
ECS_CLUSTER="investment-advisor-dev-cluster"
ECS_SERVICE="investment-advisor-dev-service"

echo -e "${BLUE}🔄 Updating Investment Advisor Application${NC}"
echo -e "${BLUE}=========================================${NC}"

# Function to print status
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Update ECS service to force new deployment
echo -e "${BLUE}🚀 Forcing ECS service update...${NC}"

aws ecs update-service \
    --cluster $ECS_CLUSTER \
    --service $ECS_SERVICE \
    --force-new-deployment \
    --profile $AWS_PROFILE \
    --region $AWS_REGION

if [ $? -eq 0 ]; then
    print_status "ECS service update initiated"
else
    print_error "Failed to update ECS service"
    exit 1
fi

# Wait for deployment to complete
echo -e "${BLUE}⏳ Waiting for deployment to complete...${NC}"

aws ecs wait services-stable \
    --cluster $ECS_CLUSTER \
    --services $ECS_SERVICE \
    --profile $AWS_PROFILE \
    --region $AWS_REGION

if [ $? -eq 0 ]; then
    print_status "Deployment completed successfully"
else
    print_warning "Deployment may still be in progress"
fi

# Get the application URL
ALB_DNS=$(aws elbv2 describe-load-balancers \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --query 'LoadBalancers[?contains(LoadBalancerName, `investment-advisor-dev`)].DNSName' \
    --output text)

if [ ! -z "$ALB_DNS" ]; then
    echo ""
    echo -e "${GREEN}🎉 Application Updated Successfully!${NC}"
    echo -e "${GREEN}===================================${NC}"
    echo -e "${BLUE}🌐 Application URL: http://${ALB_DNS}${NC}"
    echo ""
    echo -e "${BLUE}📋 What's New:${NC}"
    echo -e "✅ Enhanced Streamlit configuration"
    echo -e "✅ Professional styling and themes"
    echo -e "✅ Wide mode enabled by default"
    echo -e "✅ Improved responsive design"
    echo -e "✅ Better user experience"
    echo ""
    echo -e "${YELLOW}💡 Tip: Clear your browser cache to see all changes${NC}"
else
    print_warning "Could not retrieve application URL"
fi

echo ""
print_status "Update process completed!"
