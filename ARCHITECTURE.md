# Investment Advisor AI - Complete Architecture

## 🏗️ **System Architecture Overview**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Investment Advisor AI Platform               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐    │
│  │   Users     │    │  Load        │    │   Streamlit     │    │
│  │  (Web UI)   │◄──►│  Balancer    │◄──►│   Application   │    │
│  └─────────────┘    │   (ALB)      │    │   (ECS Fargate) │    │
│                     └──────────────┘    └─────────────────┘    │
│                                                   │             │
│  ┌─────────────────────────────────────────────────────────────┤
│  │                    MCP Layer                                │
│  ├─────────────────────────────────────────────────────────────┤
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐    │
│  │  │   AWS MCP   │  │ Bedrock MCP │  │ Portfolio MCP   │    │
│  │  │   Server    │  │   Server    │  │    Server       │    │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘    │
│  └─────────────────────────────────────────────────────────────┤
│                                                   │             │
│  ┌─────────────────────────────────────────────────────────────┤
│  │                   AWS Services                              │
│  ├─────────────────────────────────────────────────────────────┤
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐    │
│  │  │   Amazon    │  │     S3      │  │     Lambda      │    │
│  │  │   Bedrock   │  │  Storage    │  │   Functions     │    │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘    │
│  │                                                             │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐    │
│  │  │     RDS     │  │ CloudWatch  │  │   API Gateway   │    │
│  │  │  (Optional) │  │ Monitoring  │  │      (CDK)      │    │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘    │
│  └─────────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 **Technology Stack**

### **Infrastructure as Code**
- **Terraform**: Primary infrastructure provisioning
- **AWS CDK**: Serverless components and Lambda functions
- **CloudFormation**: Underlying AWS resource management

### **Frontend & Application**
- **Streamlit**: Interactive web application framework
- **Python 3.11**: Primary programming language
- **Plotly**: Data visualization and charts
- **Pandas**: Data processing and analysis

### **Container & Orchestration**
- **Docker**: Application containerization
- **Amazon ECS Fargate**: Serverless container hosting
- **Application Load Balancer**: Traffic distribution
- **Amazon ECR**: Container image registry

### **AI & Machine Learning**
- **Amazon Bedrock**: Foundation models (Titan, Nova, Claude)
- **MCP (Model Context Protocol)**: AI service integration
- **Custom MCP Servers**: Specialized AI capabilities
- **QuantLib**: Financial modeling and optimization

### **Data & Storage**
- **Amazon S3**: Object storage for data and documents
- **Amazon RDS**: Relational database (optional)
- **DynamoDB**: Session and user data (via CDK)
- **CloudWatch**: Logging and monitoring

### **Networking & Security**
- **Amazon VPC**: Isolated network environment
- **NAT Gateways**: Secure outbound internet access
- **Security Groups**: Network-level security
- **IAM Roles**: Fine-grained access control

## 🔄 **Data Flow Architecture**

### **1. User Interaction Flow**
```
User Request → ALB → ECS Fargate → Streamlit App → MCP Servers → AWS Services
```

### **2. AI Processing Flow**
```
Investment Query → Bedrock MCP → Amazon Bedrock → AI Model → Response → UI
```

### **3. Data Storage Flow**
```
User Data → S3 Buckets → Lambda Processing → Analysis Results → Dashboard
```

### **4. Portfolio Optimization Flow**
```
Portfolio Data → Portfolio MCP → QuantLib Engine → Optimization → Recommendations
```

## 🏗️ **Infrastructure Components**

### **Terraform Modules**

#### **VPC Module**
- **Purpose**: Network foundation
- **Components**: VPC, Subnets, NAT Gateways, Route Tables
- **Security**: Private/Public subnet separation
- **Endpoints**: S3 and Bedrock VPC endpoints

#### **ECS Module**
- **Purpose**: Container orchestration
- **Components**: ECS Cluster, Service, Task Definition
- **Scaling**: Auto-scaling based on CPU/Memory
- **Load Balancing**: Application Load Balancer integration

#### **S3 Module**
- **Purpose**: Data storage
- **Buckets**: 
  - Investment data storage
  - Knowledge base documents
  - Static assets
- **Security**: Encryption at rest, access policies

#### **Bedrock Module**
- **Purpose**: AI model access
- **Models**: Titan, Nova, Claude integration
- **Permissions**: IAM roles for model access
- **Monitoring**: Usage tracking and logging

### **CDK Components**

#### **Lambda Functions**
- **Investment Analyzer**: AI-powered investment analysis
- **Portfolio Optimizer**: Mathematical optimization
- **Risk Assessor**: Risk calculation and modeling
- **Report Generator**: Automated report creation

#### **API Gateway**
- **Purpose**: RESTful API endpoints
- **Authentication**: IAM-based access control
- **Rate Limiting**: Request throttling
- **Monitoring**: CloudWatch integration

#### **DynamoDB Tables**
- **User Sessions**: Session management
- **Portfolio Data**: User portfolio storage
- **Analysis History**: Historical analysis results
- **System Configuration**: Application settings

## 🔧 **MCP Server Architecture**

### **AWS MCP Server**
```javascript
{
  "command": "npx",
  "args": ["@modelcontextprotocol/server-aws"],
  "capabilities": ["resources", "tools"],
  "services": ["s3", "bedrock", "lambda", "dynamodb"]
}
```

### **Bedrock MCP Server**
```python
class BedrockMCPServer:
    - analyze_investment()
    - optimize_portfolio()
    - assess_risk()
    - generate_report()
```

### **Portfolio MCP Server**
```python
class PortfolioMCPServer:
    - calculate_metrics()
    - optimize_allocation()
    - stress_test()
    - rebalance_recommendations()
```

## 🚀 **Deployment Architecture**

### **Multi-Environment Support**
```
environments/
├── dev/        # Development environment
├── staging/    # Staging environment
└── prod/       # Production environment
```

### **CI/CD Pipeline**
```
Code Commit → Build → Test → Deploy → Monitor
     ↓           ↓      ↓       ↓        ↓
   GitHub    Docker   Unit   Terraform CloudWatch
            Build    Tests   Deploy   Monitoring
```

### **Deployment Stages**
1. **Infrastructure**: Terraform provisions AWS resources
2. **Application**: Docker builds and ECS deployment
3. **Configuration**: MCP servers and CDK components
4. **Validation**: Health checks and smoke tests
5. **Monitoring**: CloudWatch dashboards and alerts

## 📊 **Monitoring & Observability**

### **CloudWatch Dashboards**
- **Application Metrics**: Response times, error rates
- **Infrastructure Metrics**: CPU, memory, network usage
- **Business Metrics**: User engagement, analysis requests
- **Cost Metrics**: AWS service usage and costs

### **Logging Strategy**
- **Application Logs**: Streamlit application events
- **MCP Server Logs**: AI service interactions
- **Infrastructure Logs**: ECS, ALB, and VPC flow logs
- **Audit Logs**: User actions and system changes

### **Alerting**
- **Performance Alerts**: High latency, error rates
- **Infrastructure Alerts**: Resource utilization
- **Security Alerts**: Unauthorized access attempts
- **Cost Alerts**: Budget threshold notifications

## 🔒 **Security Architecture**

### **Network Security**
- **VPC Isolation**: Private subnets for sensitive components
- **Security Groups**: Restrictive inbound/outbound rules
- **NACLs**: Additional network-level protection
- **VPC Endpoints**: Private AWS service access

### **Application Security**
- **IAM Roles**: Least privilege access
- **Encryption**: Data at rest and in transit
- **Authentication**: User session management
- **Input Validation**: Secure data processing

### **Data Security**
- **S3 Encryption**: Server-side encryption
- **Database Encryption**: RDS/DynamoDB encryption
- **Secrets Management**: AWS Secrets Manager
- **Backup Strategy**: Automated backups and retention

## 📈 **Scalability & Performance**

### **Horizontal Scaling**
- **ECS Auto Scaling**: Container instance scaling
- **ALB**: Load distribution across instances
- **Lambda Concurrency**: Serverless function scaling
- **Database Scaling**: RDS read replicas (if used)

### **Performance Optimization**
- **Caching**: Redis/ElastiCache for frequent data
- **CDN**: CloudFront for static assets
- **Database Optimization**: Query optimization and indexing
- **API Optimization**: Response caching and compression

### **Cost Optimization**
- **Reserved Instances**: Long-term compute savings
- **Spot Instances**: Cost-effective batch processing
- **S3 Lifecycle**: Automated data archiving
- **Resource Tagging**: Cost allocation and tracking

## 🔄 **Disaster Recovery**

### **Backup Strategy**
- **Database Backups**: Automated daily backups
- **S3 Cross-Region Replication**: Data redundancy
- **Infrastructure as Code**: Rapid environment recreation
- **Configuration Backups**: System settings preservation

### **Recovery Procedures**
- **RTO (Recovery Time Objective)**: < 4 hours
- **RPO (Recovery Point Objective)**: < 1 hour
- **Multi-AZ Deployment**: High availability
- **Automated Failover**: Minimal downtime

This architecture provides a robust, scalable, and secure foundation for the Investment Advisor AI platform, leveraging modern cloud-native technologies and best practices.
