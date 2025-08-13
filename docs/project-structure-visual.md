# Project Structure Visualization

## 📁 **Complete Project File Tree**

```
cdk-investment-advisor/
│
├── 📁 terraform/                              # Infrastructure as Code
│   ├── 📁 environments/                       # Environment Configurations
│   │   ├── 📁 dev/
│   │   │   ├── 📄 terraform.tfvars           # Development variables
│   │   │   ├── 📄 backend.tf                 # Dev backend config
│   │   │   └── 📄 locals.tf                  # Dev-specific locals
│   │   ├── 📁 staging/
│   │   │   ├── 📄 terraform.tfvars           # Staging variables
│   │   │   ├── 📄 backend.tf                 # Staging backend config
│   │   │   └── 📄 locals.tf                  # Staging-specific locals
│   │   └── 📁 prod/
│   │       ├── 📄 terraform.tfvars           # Production variables
│   │       ├── 📄 backend.tf                 # Prod backend config
│   │       └── 📄 locals.tf                  # Prod-specific locals
│   │
│   ├── 📁 modules/                            # Reusable Terraform Modules
│   │   ├── 📁 vpc/                           # VPC Module
│   │   │   ├── 📄 main.tf                    # VPC resources
│   │   │   ├── 📄 variables.tf               # VPC variables
│   │   │   ├── 📄 outputs.tf                 # VPC outputs
│   │   │   └── 📄 README.md                  # VPC documentation
│   │   │
│   │   ├── 📁 ecs/                           # ECS Module
│   │   │   ├── 📄 main.tf                    # ECS cluster & service
│   │   │   ├── 📄 variables.tf               # ECS variables
│   │   │   ├── 📄 outputs.tf                 # ECS outputs
│   │   │   ├── 📄 alb.tf                     # Load balancer
│   │   │   ├── 📄 security_groups.tf         # Security groups
│   │   │   └── 📄 autoscaling.tf             # Auto scaling
│   │   │
│   │   ├── 📁 s3/                            # S3 Module
│   │   │   ├── 📄 main.tf                    # S3 buckets
│   │   │   ├── 📄 variables.tf               # S3 variables
│   │   │   ├── 📄 outputs.tf                 # S3 outputs
│   │   │   ├── 📄 policies.tf                # Bucket policies
│   │   │   └── 📄 lifecycle.tf               # Lifecycle rules
│   │   │
│   │   ├── 📁 rds/                           # RDS Module (Optional)
│   │   │   ├── 📄 main.tf                    # RDS instance
│   │   │   ├── 📄 variables.tf               # RDS variables
│   │   │   ├── 📄 outputs.tf                 # RDS outputs
│   │   │   └── 📄 security_groups.tf         # DB security
│   │   │
│   │   └── 📁 bedrock/                       # Bedrock Module
│   │       ├── 📄 main.tf                    # Bedrock resources
│   │       ├── 📄 variables.tf               # Bedrock variables
│   │       ├── 📄 outputs.tf                 # Bedrock outputs
│   │       └── 📄 model_access.tf            # Model permissions
│   │
│   ├── 📄 main.tf                            # Main Terraform config
│   ├── 📄 variables.tf                       # Global variables
│   ├── 📄 outputs.tf                         # Global outputs
│   ├── 📄 versions.tf                        # Provider versions
│   └── 📄 terraform.tfvars.example           # Example variables
│
├── 📁 streamlit-app/                          # Frontend Application
│   ├── 📁 pages/                             # Multi-page App
│   │   ├── 📄 1_🏠_Dashboard.py              # Main dashboard
│   │   ├── 📄 2_📊_Portfolio_Analysis.py     # Portfolio page
│   │   ├── 📄 3_⚠️_Risk_Assessment.py        # Risk analysis
│   │   ├── 📄 4_📈_Market_Insights.py        # Market data
│   │   └── 📄 5_⚙️_Settings.py               # Configuration
│   │
│   ├── 📁 components/                        # Reusable Components
│   │   ├── 📄 __init__.py                    # Package init
│   │   ├── 📄 portfolio_optimizer.py        # Portfolio logic
│   │   ├── 📄 risk_analyzer.py               # Risk calculations
│   │   ├── 📄 market_data.py                 # Market data provider
│   │   ├── 📄 charts.py                      # Chart components
│   │   └── 📄 auth.py                        # Authentication
│   │
│   ├── 📁 utils/                             # Utility Functions
│   │   ├── 📄 __init__.py                    # Package init
│   │   ├── 📄 aws_client.py                  # AWS SDK wrapper
│   │   ├── 📄 mcp_client.py                  # MCP client
│   │   ├── 📄 data_processor.py              # Data processing
│   │   ├── 📄 validators.py                  # Input validation
│   │   └── 📄 helpers.py                     # Helper functions
│   │
│   ├── 📁 config/                            # Configuration
│   │   ├── 📄 __init__.py                    # Package init
│   │   ├── 📄 settings.py                    # App settings
│   │   ├── 📄 constants.py                   # Constants
│   │   └── 📄 logging_config.py              # Logging setup
│   │
│   ├── 📁 static/                            # Static Assets
│   │   ├── 📁 css/
│   │   │   ├── 📄 main.css                   # Main styles
│   │   │   └── 📄 components.css             # Component styles
│   │   ├── 📁 js/
│   │   │   ├── 📄 main.js                    # Main JavaScript
│   │   │   └── 📄 charts.js                  # Chart interactions
│   │   └── 📁 images/
│   │       ├── 📄 logo.png                   # App logo
│   │       └── 📄 favicon.ico                # Favicon
│   │
│   ├── 📄 app.py                             # Main application
│   ├── 📄 requirements.txt                   # Python dependencies
│   ├── 📄 Dockerfile                         # Container config
│   ├── 📄 docker-compose.yml                 # Local development
│   ├── 📄 .streamlit/config.toml             # Streamlit config
│   └── 📄 mcp-config.json                    # MCP configuration
│
├── 📁 cdk-investment-advisor/                # CDK Infrastructure
│   ├── 📁 lib/                               # CDK Constructs
│   │   ├── 📄 investment-advisor-stack.ts    # Main stack
│   │   ├── 📄 lambda-constructs.ts           # Lambda constructs
│   │   ├── 📄 api-constructs.ts              # API Gateway
│   │   ├── 📄 database-constructs.ts         # DynamoDB
│   │   └── 📄 monitoring-constructs.ts       # CloudWatch
│   │
│   ├── 📁 bin/                               # CDK Apps
│   │   └── 📄 investment-advisor.ts          # App entry point
│   │
│   ├── 📁 lambda/                            # Lambda Functions
│   │   ├── 📁 investment-analyzer/
│   │   │   ├── 📄 index.py                   # Main handler
│   │   │   ├── 📄 bedrock_client.py          # Bedrock integration
│   │   │   ├── 📄 requirements.txt           # Dependencies
│   │   │   └── 📄 Dockerfile                 # Container config
│   │   │
│   │   ├── 📁 portfolio-optimizer/
│   │   │   ├── 📄 index.py                   # Main handler
│   │   │   ├── 📄 optimization_engine.py     # Optimization logic
│   │   │   ├── 📄 requirements.txt           # Dependencies
│   │   │   └── 📄 layers/                    # Lambda layers
│   │   │
│   │   ├── 📁 risk-assessor/
│   │   │   ├── 📄 index.py                   # Main handler
│   │   │   ├── 📄 risk_models.py             # Risk calculations
│   │   │   └── 📄 requirements.txt           # Dependencies
│   │   │
│   │   └── 📁 report-generator/
│   │       ├── 📄 index.py                   # Main handler
│   │       ├── 📄 template_engine.py         # Report templates
│   │       └── 📄 requirements.txt           # Dependencies
│   │
│   ├── 📄 cdk.json                           # CDK configuration
│   ├── 📄 package.json                       # Node.js dependencies
│   ├── 📄 tsconfig.json                      # TypeScript config
│   └── 📄 jest.config.js                     # Testing config
│
├── 📁 mcp-servers/                            # MCP Server Configurations
│   ├── 📁 aws-mcp/                          # AWS MCP Server
│   │   ├── 📄 package.json                   # Node.js config
│   │   ├── 📄 server.js                      # MCP server logic
│   │   └── 📄 config.json                    # Server config
│   │
│   ├── 📁 bedrock-mcp/                       # Bedrock MCP Server
│   │   ├── 📄 mcp_server_bedrock.py          # Python MCP server
│   │   ├── 📄 requirements.txt               # Python dependencies
│   │   ├── 📄 config.yaml                    # Server configuration
│   │   └── 📄 models/                        # Model configurations
│   │
│   ├── 📁 s3-mcp/                            # S3 MCP Server
│   │   ├── 📄 mcp_server_s3.py               # S3 operations server
│   │   ├── 📄 requirements.txt               # Dependencies
│   │   └── 📄 bucket_config.json             # Bucket configurations
│   │
│   └── 📄 mcp-config.json                    # Global MCP config
│
├── 📁 docker/                                # Container Configurations
│   ├── 📁 streamlit/
│   │   ├── 📄 Dockerfile                     # Streamlit container
│   │   └── 📄 entrypoint.sh                  # Container entrypoint
│   │
│   ├── 📁 nginx/
│   │   ├── 📄 Dockerfile                     # Nginx container
│   │   ├── 📄 nginx.conf                     # Nginx config
│   │   └── 📄 ssl/                           # SSL certificates
│   │
│   └── 📄 docker-compose.yml                 # Multi-container setup
│
├── 📁 scripts/                               # Deployment Scripts
│   ├── 📄 deploy.sh                          # Main deployment
│   ├── 📄 setup.sh                           # Environment setup
│   ├── 📄 cleanup.sh                         # Resource cleanup
│   ├── 📄 test.sh                            # Testing script
│   └── 📄 backup.sh                          # Backup script
│
├── 📁 docs/                                  # Documentation
│   ├── 📄 ARCHITECTURE.md                    # System architecture
│   ├── 📄 DEPLOYMENT.md                      # Deployment guide
│   ├── 📄 API.md                             # API documentation
│   ├── 📄 MCP.md                             # MCP server guide
│   ├── 📄 TROUBLESHOOTING.md                 # Troubleshooting
│   ├── 📄 architecture-diagram.md            # Architecture diagrams
│   ├── 📄 cdk-structure-diagram.md           # CDK structure
│   └── 📄 project-structure-visual.md        # This file
│
├── 📁 tests/                                 # Testing
│   ├── 📁 unit/                              # Unit Tests
│   │   ├── 📄 test_portfolio_optimizer.py    # Portfolio tests
│   │   ├── 📄 test_risk_analyzer.py          # Risk tests
│   │   └── 📄 test_aws_client.py             # AWS client tests
│   │
│   ├── 📁 integration/                       # Integration Tests
│   │   ├── 📄 test_api_endpoints.py          # API tests
│   │   ├── 📄 test_mcp_servers.py            # MCP tests
│   │   └── 📄 test_lambda_functions.py       # Lambda tests
│   │
│   ├── 📁 e2e/                               # End-to-End Tests
│   │   ├── 📄 test_user_journey.py           # User flow tests
│   │   └── 📄 test_deployment.py             # Deployment tests
│   │
│   └── 📄 conftest.py                        # Test configuration
│
├── 📁 .github/                               # GitHub Configuration
│   ├── 📁 workflows/                         # GitHub Actions
│   │   ├── 📄 ci.yml                         # Continuous Integration
│   │   ├── 📄 cd.yml                         # Continuous Deployment
│   │   └── 📄 security.yml                   # Security scanning
│   │
│   └── 📄 ISSUE_TEMPLATE.md                  # Issue template
│
├── 📄 README.md                              # Project README
├── 📄 PROJECT_STRUCTURE.md                   # Project overview
├── 📄 ARCHITECTURE.md                        # Architecture overview
├── 📄 LICENSE                                # License file
├── 📄 .gitignore                             # Git ignore rules
├── 📄 .env.example                           # Environment template
├── 📄 package.json                           # Root package config
└── 📄 Makefile                               # Build automation
```

## 🎯 **Key Directory Purposes**

| Directory | Purpose | Technology |
|-----------|---------|------------|
| `terraform/` | Infrastructure provisioning | Terraform |
| `streamlit-app/` | Web application frontend | Streamlit + Python |
| `cdk-investment-advisor/` | Serverless backend | AWS CDK + TypeScript |
| `mcp-servers/` | AI service integration | MCP Protocol |
| `docker/` | Container configurations | Docker |
| `scripts/` | Automation and deployment | Bash |
| `docs/` | Project documentation | Markdown |
| `tests/` | Testing suite | pytest |

This structure provides a complete, production-ready architecture for the Investment Advisor AI platform! 🚀
