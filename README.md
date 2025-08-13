# 🤖 Investment Advisor AI Platform

A comprehensive AI-powered investment advisory platform built with **Terraform**, **Streamlit**, **AWS CDK**, and **MCP Servers** on AWS.

[![AWS](https://img.shields.io/badge/AWS-Cloud-orange)](https://aws.amazon.com/)
[![Terraform](https://img.shields.io/badge/Terraform-Infrastructure-purple)](https://terraform.io/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)](https://streamlit.io/)
[![CDK](https://img.shields.io/badge/CDK-Serverless-blue)](https://aws.amazon.com/cdk/)
[![MCP](https://img.shields.io/badge/MCP-AI_Integration-green)](https://modelcontextprotocol.io/)

## 🎯 **Overview**

The Investment Advisor AI Platform is a modern, cloud-native application that provides intelligent investment recommendations using advanced AI models. Built with a microservices architecture, it combines the power of Amazon Bedrock, sophisticated portfolio optimization algorithms, and an intuitive web interface.

### **Key Features**

- 🤖 **AI-Powered Analysis**: Leverages Amazon Bedrock (Titan, Nova, Claude) for investment insights
- 📊 **Portfolio Optimization**: Advanced mathematical models for asset allocation
- 🎨 **Interactive Dashboard**: Beautiful Streamlit-based web interface
- 🔧 **MCP Integration**: Model Context Protocol for seamless AI service integration
- 🏗️ **Infrastructure as Code**: Complete Terraform and CDK automation
- 🔒 **Enterprise Security**: AWS-native security with IAM, VPC, and encryption
- 📈 **Scalable Architecture**: Auto-scaling ECS Fargate deployment
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices

## 🏗️ **Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Investment Advisor AI Platform               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Users ──► Load Balancer ──► Streamlit App ──► MCP Servers     │
│              (ALB)           (ECS Fargate)      (AI Services)   │
│                                    │                            │
│                                    ▼                            │
│  ┌─────────────────────────────────────────────────────────────┤
│  │  AWS Services: Bedrock │ S3 │ Lambda │ RDS │ CloudWatch     │
│  └─────────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 **Quick Start**

### **Prerequisites**

- AWS CLI configured with appropriate permissions
- Terraform >= 1.0
- Docker and Docker Compose
- Node.js >= 18.x
- Python >= 3.11
- AWS CDK CLI

### **1. Clone Repository**

```bash
git clone https://github.com/your-username/cdk-investment-advisor.git
cd cdk-investment-advisor
```

### **2. Configure Environment**

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
vim .env
```

### **3. Deploy Infrastructure**

```bash
# Run complete deployment
./scripts/deploy.sh dev

# Or deploy components individually
cd terraform && terraform init && terraform apply
cd ../streamlit-app && docker build -t investment-advisor .
cd ../cdk-investment-advisor && cdk deploy
```

### **4. Access Application**

After deployment, access your application at the provided ALB DNS name.

## 📁 **Project Structure**

```
cdk-investment-advisor/
├── 📁 terraform/                          # Infrastructure as Code
│   ├── 📁 environments/                   # Environment-specific configs
│   ├── 📁 modules/                        # Reusable Terraform modules
│   ├── main.tf                           # Main Terraform configuration
│   └── variables.tf                      # Input variables
├── 📁 streamlit-app/                      # Frontend Application
│   ├── 📁 pages/                          # Multi-page application
│   ├── 📁 components/                     # Reusable UI components
│   ├── 📁 utils/                          # Utility functions
│   ├── app.py                            # Main application
│   ├── Dockerfile                        # Container configuration
│   └── requirements.txt                  # Python dependencies
├── 📁 cdk/                               # CDK Infrastructure
│   ├── 📁 lib/                           # CDK constructs
│   ├── 📁 lambda/                        # Lambda function code
│   └── app.py                            # CDK application
├── 📁 mcp-servers/                       # MCP Server Configurations
│   ├── 📁 aws-mcp/                       # AWS services integration
│   ├── 📁 bedrock-mcp/                   # Bedrock AI integration
│   └── mcp-config.json                   # MCP configuration
├── 📁 scripts/                           # Deployment scripts
│   ├── deploy.sh                         # Main deployment script
│   ├── setup.sh                          # Environment setup
│   └── cleanup.sh                        # Resource cleanup
├── 📁 docs/                              # Documentation
│   ├── ARCHITECTURE.md                   # System architecture
│   ├── DEPLOYMENT.md                     # Deployment guide
│   └── API.md                            # API documentation
└── 📁 tests/                             # Testing
    ├── unit/                             # Unit tests
    ├── integration/                      # Integration tests
    └── e2e/                              # End-to-end tests
```

## 🔧 **Configuration**

### **Environment Variables**

```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_PROFILE=Juanelo

# Application Configuration
ENVIRONMENT=dev
PROJECT_NAME=investment-advisor

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# MCP Configuration
MCP_CONFIG_PATH=/app/mcp-config.json

# Database Configuration (Optional)
ENABLE_RDS=false
DB_NAME=investment_advisor
DB_USERNAME=admin
```

### **Terraform Variables**

```hcl
# terraform/terraform.tfvars
aws_region = "us-east-1"
environment = "dev"
project_name = "investment-advisor"

# ECS Configuration
ecs_cpu = 512
ecs_memory = 1024
desired_count = 2

# Bedrock Models
bedrock_models = [
  "amazon.titan-text-express-v1",
  "amazon.nova-pro-v1:0",
  "anthropic.claude-3-haiku-20240307-v1:0"
]
```

## 🤖 **MCP Server Integration**

### **Available MCP Servers**

1. **AWS MCP Server**: Direct AWS service integration
2. **Bedrock MCP Server**: AI model interactions
3. **Portfolio MCP Server**: Financial calculations
4. **S3 MCP Server**: Data storage operations

### **MCP Configuration**

```json
{
  "mcpServers": {
    "aws": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-aws"],
      "capabilities": ["resources", "tools"]
    },
    "bedrock": {
      "command": "python",
      "args": ["-m", "mcp_server_bedrock"],
      "capabilities": ["tools", "prompts"]
    }
  }
}
```

## 📊 **Features**

### **Investment Analysis**
- AI-powered investment recommendations
- Risk tolerance assessment
- Time horizon optimization
- Goal-based planning

### **Portfolio Management**
- Asset allocation optimization
- Rebalancing recommendations
- Performance tracking
- Risk analysis

### **Interactive Dashboard**
- Real-time portfolio visualization
- Performance charts and metrics
- Customizable investment parameters
- Export capabilities

### **AI Integration**
- Multiple AI models (Titan, Nova, Claude)
- Natural language processing
- Contextual recommendations
- Continuous learning

## 🔒 **Security**

### **Infrastructure Security**
- VPC with private subnets
- Security groups and NACLs
- IAM roles with least privilege
- Encryption at rest and in transit

### **Application Security**
- Input validation and sanitization
- Session management
- Secure API endpoints
- Audit logging

### **Data Security**
- S3 bucket encryption
- Database encryption
- Secrets management
- Backup and recovery

## 📈 **Monitoring & Observability**

### **CloudWatch Integration**
- Application metrics and logs
- Infrastructure monitoring
- Custom dashboards
- Automated alerting

### **Performance Monitoring**
- Response time tracking
- Error rate monitoring
- Resource utilization
- Cost optimization

## 🧪 **Testing**

### **Run Tests**

```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# End-to-end tests
pytest tests/e2e/

# All tests
pytest
```

### **Test Coverage**

```bash
# Generate coverage report
pytest --cov=src --cov-report=html
```

## 🚀 **Deployment**

### **Development Environment**

```bash
./scripts/deploy.sh dev
```

### **Staging Environment**

```bash
./scripts/deploy.sh staging
```

### **Production Environment**

```bash
./scripts/deploy.sh prod
```

### **Manual Deployment**

```bash
# Deploy infrastructure
cd terraform
terraform init
terraform plan -var="environment=dev"
terraform apply

# Build and deploy application
cd ../streamlit-app
docker build -t investment-advisor .
docker push <ecr-repo-url>

# Deploy serverless components
cd ../cdk-investment-advisor
cdk deploy
```

## 📚 **Documentation**

- [Architecture Guide](docs/ARCHITECTURE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [API Documentation](docs/API.md)
- [MCP Server Guide](docs/MCP.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- AWS for providing the cloud infrastructure
- Streamlit for the amazing web framework
- The MCP community for protocol development
- Open source contributors and maintainers

## 📞 **Support**

- 📧 Email: support@investment-advisor.ai
- 💬 Discord: [Join our community](https://discord.gg/investment-advisor)
- 📖 Documentation: [docs.investment-advisor.ai](https://docs.investment-advisor.ai)
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/cdk-investment-advisor/issues)

---

**Built with ❤️ by the Investment Advisor AI Team**

*Empowering intelligent investment decisions through AI and cloud technology.*
