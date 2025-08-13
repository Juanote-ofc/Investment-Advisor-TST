#!/bin/bash

# Investment Advisor - Complete Deployment Script
# Deploys Terraform infrastructure, builds Docker images, and configures MCP servers

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="investment-advisor"
AWS_REGION="us-east-1"
AWS_PROFILE="Juanelo"
ENVIRONMENT="${1:-dev}"

echo -e "${BLUE}🚀 Investment Advisor Deployment Script${NC}"
echo -e "${BLUE}======================================${NC}"
echo -e "Environment: ${ENVIRONMENT}"
echo -e "AWS Region: ${AWS_REGION}"
echo -e "AWS Profile: ${AWS_PROFILE}"
echo ""

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

# Function to check prerequisites
check_prerequisites() {
    echo -e "${BLUE}🔍 Checking prerequisites...${NC}"
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI not found. Please install AWS CLI."
        exit 1
    fi
    
    # Check Terraform
    if ! command -v terraform &> /dev/null; then
        print_error "Terraform not found. Please install Terraform."
        exit 1
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker not found. Please install Docker."
        exit 1
    fi
    
    # Check CDK
    if ! command -v cdk &> /dev/null; then
        print_error "AWS CDK not found. Please install AWS CDK."
        exit 1
    fi
    
    # Check Node.js (for MCP servers)
    if ! command -v node &> /dev/null; then
        print_error "Node.js not found. Please install Node.js."
        exit 1
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity --profile $AWS_PROFILE &> /dev/null; then
        print_error "AWS credentials not configured for profile: $AWS_PROFILE"
        exit 1
    fi
    
    print_status "All prerequisites met"
}

# Function to setup Terraform backend
setup_terraform_backend() {
    echo -e "${BLUE}🏗️  Setting up Terraform backend...${NC}"
    
    # Create S3 bucket for Terraform state
    BUCKET_NAME="${PROJECT_NAME}-terraform-state-${ENVIRONMENT}"
    
    if ! aws s3 ls "s3://${BUCKET_NAME}" --profile $AWS_PROFILE &> /dev/null; then
        aws s3 mb "s3://${BUCKET_NAME}" --region $AWS_REGION --profile $AWS_PROFILE
        
        # Enable versioning
        aws s3api put-bucket-versioning \
            --bucket $BUCKET_NAME \
            --versioning-configuration Status=Enabled \
            --profile $AWS_PROFILE
        
        # Enable encryption
        aws s3api put-bucket-encryption \
            --bucket $BUCKET_NAME \
            --server-side-encryption-configuration '{
                "Rules": [{
                    "ApplyServerSideEncryptionByDefault": {
                        "SSEAlgorithm": "AES256"
                    }
                }]
            }' \
            --profile $AWS_PROFILE
        
        print_status "Terraform state bucket created: $BUCKET_NAME"
    else
        print_status "Terraform state bucket already exists: $BUCKET_NAME"
    fi
}

# Function to deploy Terraform infrastructure
deploy_terraform() {
    echo -e "${BLUE}🏗️  Deploying Terraform infrastructure...${NC}"
    
    cd terraform
    
    # Initialize Terraform
    terraform init \
        -backend-config="bucket=${PROJECT_NAME}-terraform-state-${ENVIRONMENT}" \
        -backend-config="key=${ENVIRONMENT}/terraform.tfstate" \
        -backend-config="region=${AWS_REGION}" \
        -backend-config="profile=${AWS_PROFILE}"
    
    # Plan deployment
    terraform plan \
        -var="environment=${ENVIRONMENT}" \
        -var="aws_region=${AWS_REGION}" \
        -out=tfplan
    
    # Apply deployment
    terraform apply tfplan
    
    # Save outputs
    terraform output -json > ../terraform-outputs.json
    
    cd ..
    
    print_status "Terraform infrastructure deployed"
}

# Function to build and push Docker images
build_docker_images() {
    echo -e "${BLUE}🐳 Building Docker images...${NC}"
    
    # Get ECR repository URL from Terraform outputs
    ECR_REPO=$(cat terraform-outputs.json | jq -r '.ecr_repository_url.value')
    
    if [ "$ECR_REPO" != "null" ]; then
        # Login to ECR
        aws ecr get-login-password --region $AWS_REGION --profile $AWS_PROFILE | \
            docker login --username AWS --password-stdin $ECR_REPO
        
        # Build Streamlit image
        cd streamlit-app
        docker build -t $PROJECT_NAME-streamlit:latest .
        docker tag $PROJECT_NAME-streamlit:latest $ECR_REPO:latest
        docker push $ECR_REPO:latest
        cd ..
        
        print_status "Docker images built and pushed to ECR"
    else
        print_warning "ECR repository not found, skipping Docker build"
    fi
}

# Function to setup MCP servers
setup_mcp_servers() {
    echo -e "${BLUE}🔧 Setting up MCP servers...${NC}"
    
    # Install MCP server dependencies
    cd mcp-servers
    
    # Install AWS MCP server
    npm install -g @modelcontextprotocol/server-aws
    
    # Install custom MCP servers
    cd bedrock-mcp
    pip install -r requirements.txt
    cd ..
    
    cd ..
    
    print_status "MCP servers configured"
}

# Function to deploy CDK components
deploy_cdk() {
    echo -e "${BLUE}☁️  Deploying CDK components...${NC}"
    
    cd cdk-investment-advisor
    
    # Activate virtual environment
    source .venv/bin/activate
    
    # Install dependencies
    pip install -r requirements.txt
    
    # Bootstrap CDK (if not already done)
    cdk bootstrap --profile $AWS_PROFILE
    
    # Deploy CDK stack
    cdk deploy --profile $AWS_PROFILE --require-approval never
    
    cd ..
    
    print_status "CDK components deployed"
}

# Function to run post-deployment configuration
post_deployment_config() {
    echo -e "${BLUE}⚙️  Running post-deployment configuration...${NC}"
    
    # Update ECS service with new image
    if [ -f terraform-outputs.json ]; then
        ECS_CLUSTER=$(cat terraform-outputs.json | jq -r '.ecs_cluster_name.value')
        ECS_SERVICE=$(cat terraform-outputs.json | jq -r '.ecs_service_name.value')
        
        if [ "$ECS_CLUSTER" != "null" ] && [ "$ECS_SERVICE" != "null" ]; then
            aws ecs update-service \
                --cluster $ECS_CLUSTER \
                --service $ECS_SERVICE \
                --force-new-deployment \
                --profile $AWS_PROFILE \
                --region $AWS_REGION
            
            print_status "ECS service updated"
        fi
    fi
    
    # Upload sample data to S3
    if [ -f terraform-outputs.json ]; then
        DATA_BUCKET=$(cat terraform-outputs.json | jq -r '.s3_data_bucket.value')
        KB_BUCKET=$(cat terraform-outputs.json | jq -r '.s3_knowledge_base_bucket.value')
        
        if [ "$DATA_BUCKET" != "null" ]; then
            # Upload sample investment data
            echo '{"sample": "investment data"}' | aws s3 cp - "s3://${DATA_BUCKET}/sample/data.json" --profile $AWS_PROFILE
            print_status "Sample data uploaded to S3"
        fi
        
        if [ "$KB_BUCKET" != "null" ]; then
            # Upload knowledge base documents
            if [ -d "knowledge-base" ]; then
                aws s3 sync knowledge-base/ "s3://${KB_BUCKET}/" --profile $AWS_PROFILE
                print_status "Knowledge base documents uploaded"
            fi
        fi
    fi
}

# Function to run health checks
run_health_checks() {
    echo -e "${BLUE}🏥 Running health checks...${NC}"
    
    if [ -f terraform-outputs.json ]; then
        ALB_DNS=$(cat terraform-outputs.json | jq -r '.alb_dns_name.value')
        
        if [ "$ALB_DNS" != "null" ]; then
            echo "Waiting for application to be ready..."
            sleep 30
            
            # Check application health
            if curl -f "http://${ALB_DNS}/_stcore/health" &> /dev/null; then
                print_status "Application health check passed"
            else
                print_warning "Application health check failed - may need more time to start"
            fi
        fi
    fi
    
    # Check AWS services
    aws sts get-caller-identity --profile $AWS_PROFILE > /dev/null
    print_status "AWS connectivity verified"
    
    # Check Bedrock access
    if aws bedrock list-foundation-models --profile $AWS_PROFILE --region $AWS_REGION &> /dev/null; then
        print_status "Bedrock access verified"
    else
        print_warning "Bedrock access limited - may need model permissions"
    fi
}

# Function to display deployment summary
display_summary() {
    echo ""
    echo -e "${GREEN}🎉 Deployment Complete!${NC}"
    echo -e "${GREEN}=====================${NC}"
    
    if [ -f terraform-outputs.json ]; then
        echo -e "${BLUE}📊 Deployment Summary:${NC}"
        
        ALB_DNS=$(cat terraform-outputs.json | jq -r '.alb_dns_name.value')
        if [ "$ALB_DNS" != "null" ]; then
            echo -e "🌐 Application URL: http://${ALB_DNS}"
        fi
        
        DATA_BUCKET=$(cat terraform-outputs.json | jq -r '.s3_data_bucket.value')
        if [ "$DATA_BUCKET" != "null" ]; then
            echo -e "📦 Data Bucket: ${DATA_BUCKET}"
        fi
        
        KB_BUCKET=$(cat terraform-outputs.json | jq -r '.s3_knowledge_base_bucket.value')
        if [ "$KB_BUCKET" != "null" ]; then
            echo -e "📚 Knowledge Base Bucket: ${KB_BUCKET}"
        fi
        
        echo ""
        echo -e "${BLUE}🔧 Next Steps:${NC}"
        echo -e "1. Access the application at the URL above"
        echo -e "2. Upload investment documents to the knowledge base bucket"
        echo -e "3. Configure Bedrock model access if needed"
        echo -e "4. Monitor application logs in CloudWatch"
        echo -e "5. Set up custom domain and SSL certificate"
    fi
    
    echo ""
    echo -e "${GREEN}✅ Investment Advisor AI is now deployed and ready!${NC}"
}

# Main deployment flow
main() {
    check_prerequisites
    setup_terraform_backend
    deploy_terraform
    build_docker_images
    setup_mcp_servers
    deploy_cdk
    post_deployment_config
    run_health_checks
    display_summary
}

# Run main function
main
