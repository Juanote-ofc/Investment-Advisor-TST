# CDK Components Detailed Structure

## 🔧 **CDK Resource Hierarchy**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        CDK Resource Dependency Tree                            │
│                                                                                 │
│  CDK App                                                                        │
│      │                                                                         │
│      └── InvestmentAdvisorStack                                                │
│           │                                                                    │
│           ├── IAM Roles & Policies                                             │
│           │   ├── LambdaExecutionRole                                          │
│           │   │   ├── BedrockAccess Policy                                     │
│           │   │   ├── S3Access Policy                                          │
│           │   │   └── CloudWatchLogs Policy                                    │
│           │   │                                                                │
│           │   ├── BedrockAgentRole                                             │
│           │   │   ├── BedrockInvoke Policy                                     │
│           │   │   └── LambdaInvoke Policy                                      │
│           │   │                                                                │
│           │   └── APIGatewayRole                                               │
│           │       ├── LambdaInvoke Policy                                      │
│           │       └── CloudWatchLogs Policy                                    │
│           │                                                                    │
│           ├── S3 Buckets                                                       │
│           │   ├── InvestmentDataBucket                                         │
│           │   │   ├── Versioning: Enabled                                      │
│           │   │   ├── Encryption: S3Managed                                    │
│           │   │   ├── PublicAccess: Blocked                                    │
│           │   │   └── LifecyclePolicy                                          │
│           │   │       ├── Transition to IA: 30 days                           │
│           │   │       └── Transition to Glacier: 90 days                      │
│           │   │                                                                │
│           │   ├── KnowledgeBaseBucket                                          │
│           │   │   ├── Versioning: Enabled                                      │
│           │   │   ├── Encryption: S3Managed                                    │
│           │   │   ├── PublicAccess: Blocked                                    │
│           │   │   └── NotificationConfiguration                                │
│           │   │       └── Lambda Trigger on PUT                               │
│           │   │                                                                │
│           │   ├── AssetsBucket                                                 │
│           │   │   ├── StaticWebsiteHosting                                     │
│           │   │   ├── CORS Configuration                                       │
│           │   │   └── CloudFront Distribution                                  │
│           │   │                                                                │
│           │   └── ReportsBucket                                                │
│           │       ├── Encryption: KMS                                          │
│           │       ├── AccessLogging: Enabled                                   │
│           │       └── EventBridge Integration                                  │
│           │                                                                    │
│           ├── Lambda Functions                                                 │
│           │   ├── InvestmentAnalyzerFunction                                   │
│           │   │   ├── Runtime: Python 3.11                                    │
│           │   │   ├── Memory: 1024 MB                                          │
│           │   │   ├── Timeout: 5 minutes                                       │
│           │   │   ├── Environment Variables                                    │
│           │   │   │   ├── BEDROCK_REGION                                       │
│           │   │   │   ├── S3_BUCKET_NAME                                       │
│           │   │   │   └── LOG_LEVEL                                            │
│           │   │   ├── VPC Configuration                                        │
│           │   │   │   ├── SecurityGroups                                       │
│           │   │   │   └── Subnets                                              │
│           │   │   └── Dead Letter Queue                                        │
│           │   │                                                                │
│           │   ├── PortfolioOptimizerFunction                                   │
│           │   │   ├── Runtime: Python 3.11                                    │
│           │   │   ├── Memory: 2048 MB                                          │
│           │   │   ├── Timeout: 10 minutes                                      │
│           │   │   ├── Layers                                                   │
│           │   │   │   ├── QuantLib Layer                                       │
│           │   │   │   ├── NumPy/SciPy Layer                                    │
│           │   │   │   └── Pandas Layer                                         │
│           │   │   └── Reserved Concurrency: 10                                │
│           │   │                                                                │
│           │   ├── RiskAssessorFunction                                         │
│           │   │   ├── Runtime: Python 3.11                                    │
│           │   │   ├── Memory: 1536 MB                                          │
│           │   │   ├── Timeout: 3 minutes                                       │
│           │   │   ├── EventBridge Schedule                                     │
│           │   │   │   └── Daily Risk Calculation                               │
│           │   │   └── SNS Topic Integration                                    │
│           │   │                                                                │
│           │   └── ReportGeneratorFunction                                      │
│           │       ├── Runtime: Python 3.11                                    │
│           │       ├── Memory: 1024 MB                                          │
│           │       ├── Timeout: 15 minutes                                      │
│           │       ├── S3 Event Trigger                                         │
│           │       └── SES Integration                                          │
│           │                                                                    │
│           ├── API Gateway                                                      │
│           │   ├── REST API                                                     │
│           │   │   ├── /analyze                                                 │
│           │   │   │   ├── POST → InvestmentAnalyzer                           │
│           │   │   │   ├── Request Validation                                   │
│           │   │   │   └── Rate Limiting: 100/min                              │
│           │   │   │                                                            │
│           │   │   ├── /optimize                                                │
│           │   │   │   ├── POST → PortfolioOptimizer                           │
│           │   │   │   ├── Request Validation                                   │
│           │   │   │   └── Rate Limiting: 50/min                               │
│           │   │   │                                                            │
│           │   │   ├── /risk                                                    │
│           │   │   │   ├── GET → RiskAssessor                                  │
│           │   │   │   └── Caching: 5 minutes                                  │
│           │   │   │                                                            │
│           │   │   └── /reports                                                 │
│           │   │       ├── GET → ReportGenerator                               │
│           │   │       └── Authentication Required                             │
│           │   │                                                                │
│           │   ├── API Key                                                      │
│           │   ├── Usage Plan                                                   │
│           │   │   ├── Throttle: 1000/sec                                      │
│           │   │   └── Quota: 10000/month                                      │
│           │   └── CloudWatch Logging                                          │
│           │                                                                    │
│           ├── DynamoDB Tables                                                  │
│           │   ├── UserSessions                                                 │
│           │   │   ├── PartitionKey: session_id                                │
│           │   │   ├── TTL: 24 hours                                            │
│           │   │   ├── Encryption: AWS Managed                                 │
│           │   │   └── Point-in-time Recovery                                  │
│           │   │                                                                │
│           │   ├── PortfolioData                                                │
│           │   │   ├── PartitionKey: user_id                                   │
│           │   │   ├── SortKey: timestamp                                      │
│           │   │   ├── GSI: portfolio_type                                     │
│           │   │   └── Stream: Lambda Trigger                                  │
│           │   │                                                                │
│           │   ├── AnalysisHistory                                              │
│           │   │   ├── PartitionKey: user_id                                   │
│           │   │   ├── SortKey: analysis_date                                  │
│           │   │   ├── LSI: analysis_type                                      │
│           │   │   └── Backup: Daily                                           │
│           │   │                                                                │
│           │   └── SystemConfiguration                                          │
│           │       ├── PartitionKey: config_key                               │
│           │       ├── Attributes: config_value                               │
│           │       └── Encryption: Customer Managed                           │
│           │                                                                    │
│           ├── CloudWatch Resources                                             │
│           │   ├── Log Groups                                                   │
│           │   │   ├── /aws/lambda/investment-analyzer                         │
│           │   │   ├── /aws/lambda/portfolio-optimizer                         │
│           │   │   ├── /aws/lambda/risk-assessor                               │
│           │   │   └── /aws/apigateway/investment-advisor                      │
│           │   │                                                                │
│           │   ├── Dashboards                                                   │
│           │   │   ├── Application Performance                                 │
│           │   │   ├── Business Metrics                                        │
│           │   │   └── Infrastructure Health                                   │
│           │   │                                                                │
│           │   ├── Alarms                                                       │
│           │   │   ├── Lambda Error Rate > 5%                                  │
│           │   │   ├── API Gateway 4xx > 10%                                   │
│           │   │   ├── DynamoDB Throttling                                     │
│           │   │   └── S3 PUT Error Rate                                       │
│           │   │                                                                │
│           │   └── Metrics Filters                                              │
│           │       ├── Business Events                                         │
│           │       ├── Error Patterns                                          │
│           │       └── Performance Metrics                                     │
│           │                                                                    │
│           ├── EventBridge Rules                                                │
│           │   ├── Daily Portfolio Rebalance                                   │
│           │   │   ├── Schedule: cron(0 9 * * ? *)                            │
│           │   │   └── Target: PortfolioOptimizer                              │
│           │   │                                                                │
│           │   ├── Market Data Update                                           │
│           │   │   ├── Schedule: rate(1 hour)                                  │
│           │   │   └── Target: MarketDataFunction                              │
│           │   │                                                                │
│           │   └── Risk Assessment                                              │
│           │       ├── Schedule: cron(0 18 * * ? *)                           │
│           │       └── Target: RiskAssessor                                    │
│           │                                                                    │
│           ├── SNS Topics                                                       │
│           │   ├── AlertsTopic                                                  │
│           │   │   ├── Email Subscriptions                                     │
│           │   │   └── SMS Subscriptions                                       │
│           │   │                                                                │
│           │   └── NotificationsTopic                                           │
│           │       ├── Lambda Subscriptions                                    │
│           │       └── SQS Subscriptions                                       │
│           │                                                                    │
│           └── Custom Resources                                                 │
│               ├── BedrockModelAccess                                           │
│               │   ├── Custom Lambda                                           │
│               │   └── Model Permissions                                       │
│               │                                                                │
│               ├── S3BucketNotification                                         │
│               │   ├── Custom Lambda                                           │
│               │   └── Event Configuration                                     │
│               │                                                                │
│               └── DatabaseSeeder                                               │
│                   ├── Custom Lambda                                           │
│                   └── Initial Data Load                                       │
└─────────────────────────────────────────────────────────────────────────────────┘
```
