# Investment Advisor - Complete Architecture

## 🏗️ Project Structure

```
cdk-investment-advisor/
├── 📁 terraform/                          # Infrastructure as Code
│   ├── 📁 environments/
│   │   ├── dev/
│   │   ├── staging/
│   │   └── prod/
│   ├── 📁 modules/
│   │   ├── vpc/
│   │   ├── ecs/
│   │   ├── rds/
│   │   ├── s3/
│   │   └── bedrock/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── versions.tf
├── 📁 streamlit-app/                      # Frontend Application
│   ├── 📁 pages/
│   ├── 📁 components/
│   ├── 📁 utils/
│   ├── 📁 config/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
├── 📁 cdk/                               # CDK Infrastructure
│   ├── 📁 lib/
│   ├── 📁 bin/
│   ├── 📁 lambda/
│   ├── app.py
│   ├── cdk.json
│   └── requirements.txt
├── 📁 mcp-servers/                       # MCP Server Configurations
│   ├── 📁 aws-mcp/
│   ├── 📁 bedrock-mcp/
│   ├── 📁 s3-mcp/
│   └── mcp-config.json
├── 📁 docker/                           # Container Configurations
│   ├── streamlit/
│   ├── nginx/
│   └── docker-compose.yml
├── 📁 scripts/                          # Deployment Scripts
│   ├── deploy.sh
│   ├── setup.sh
│   └── cleanup.sh
├── 📁 docs/                             # Documentation
│   ├── architecture.md
│   ├── deployment.md
│   └── api.md
└── 📁 tests/                            # Testing
    ├── unit/
    ├── integration/
    └── e2e/
```

## 🎯 Architecture Components

### 1. **Terraform Infrastructure**
- VPC with public/private subnets
- ECS Fargate for Streamlit deployment
- Application Load Balancer
- RDS for data persistence
- S3 for static assets
- Bedrock for AI services

### 2. **Streamlit Application**
- Multi-page investment advisor interface
- Real-time portfolio optimization
- Interactive charts and visualizations
- User authentication and sessions

### 3. **CDK Components**
- Lambda functions for business logic
- API Gateway for REST endpoints
- DynamoDB for session management
- CloudWatch for monitoring

### 4. **MCP Servers**
- AWS services integration
- Bedrock model management
- S3 data operations
- Real-time data streaming

## 🔄 Data Flow

1. **User Interface** (Streamlit) → **Load Balancer** → **ECS Fargate**
2. **Streamlit App** → **API Gateway** → **Lambda Functions**
3. **Lambda** → **Bedrock** (via MCP) → **AI Analysis**
4. **Results** → **S3 Storage** → **User Dashboard**
