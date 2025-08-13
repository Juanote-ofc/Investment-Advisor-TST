from aws_cdk import (
    Duration,
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_bedrock as bedrock,
    CfnOutput,
)
from constructs import Construct

class CdkInvestmentAdvisorStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3 Bucket for storing investment data and documents
        investment_data_bucket = s3.Bucket(
            self, "InvestmentDataBucket",
            bucket_name=f"investment-advisor-data-{self.account}-{self.region}",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,  # For development only
            auto_delete_objects=True  # For development only
        )

        # S3 Bucket for Bedrock knowledge base
        knowledge_base_bucket = s3.Bucket(
            self, "KnowledgeBaseBucket",
            bucket_name=f"investment-advisor-kb-{self.account}-{self.region}",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,  # For development only
            auto_delete_objects=True  # For development only
        )

        # IAM Role for Lambda functions
        lambda_execution_role = iam.Role(
            self, "InvestmentAdvisorLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ],
            inline_policies={
                "BedrockAccess": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "bedrock:InvokeModel",
                                "bedrock:InvokeModelWithResponseStream",
                                "bedrock:ListFoundationModels",
                                "bedrock:GetFoundationModel"
                            ],
                            resources=["*"]
                        )
                    ]
                ),
                "S3Access": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "s3:GetObject",
                                "s3:PutObject",
                                "s3:DeleteObject",
                                "s3:ListBucket"
                            ],
                            resources=[
                                investment_data_bucket.bucket_arn,
                                f"{investment_data_bucket.bucket_arn}/*",
                                knowledge_base_bucket.bucket_arn,
                                f"{knowledge_base_bucket.bucket_arn}/*"
                            ]
                        )
                    ]
                )
            }
        )

        # IAM Role for Bedrock Agent
        bedrock_agent_role = iam.Role(
            self, "BedrockAgentRole",
            assumed_by=iam.ServicePrincipal("bedrock.amazonaws.com"),
            inline_policies={
                "BedrockAgentPolicy": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "bedrock:InvokeModel",
                                "bedrock:InvokeModelWithResponseStream"
                            ],
                            resources=["*"]
                        ),
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "lambda:InvokeFunction"
                            ],
                            resources=["*"]  # Will be updated with specific Lambda ARNs
                        )
                    ]
                )
            }
        )

        # Lambda function for investment analysis
        investment_analyzer_lambda = _lambda.Function(
            self, "InvestmentAnalyzerFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="index.lambda_handler",
            code=_lambda.Code.from_inline("""
import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

bedrock_runtime = boto3.client('bedrock-runtime')
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Extract investment parameters from event
        investment_amount = event.get('investment_amount', 0)
        risk_tolerance = event.get('risk_tolerance', 'moderate')
        time_horizon = event.get('time_horizon', '5 years')
        
        # Prepare prompt for Bedrock
        prompt = f'''
        As an investment advisor, analyze the following investment scenario:
        - Investment Amount: ${investment_amount:,}
        - Risk Tolerance: {risk_tolerance}
        - Time Horizon: {time_horizon}
        
        Provide investment recommendations including:
        1. Asset allocation strategy
        2. Recommended investment vehicles
        3. Risk assessment
        4. Expected returns
        
        Format your response as structured JSON.
        '''
        
        # Call Bedrock model (Amazon Titan Text Express)
        response = bedrock_runtime.invoke_model(
            modelId='amazon.titan-text-express-v1',
            body=json.dumps({
                'inputText': prompt,
                'textGenerationConfig': {
                    'maxTokenCount': 1000,
                    'temperature': 0.7,
                    'topP': 0.9
                }
            })
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        advice = response_body['results'][0]['outputText']
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'investment_advice': advice,
                'parameters': {
                    'amount': investment_amount,
                    'risk_tolerance': risk_tolerance,
                    'time_horizon': time_horizon
                }
            })
        }
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
            """),
            role=lambda_execution_role,
            timeout=Duration.minutes(5),
            environment={
                "DATA_BUCKET": investment_data_bucket.bucket_name,
                "KB_BUCKET": knowledge_base_bucket.bucket_name
            }
        )

        # Lambda function for portfolio optimization
        portfolio_optimizer_lambda = _lambda.Function(
            self, "PortfolioOptimizerFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="index.lambda_handler",
            code=_lambda.Code.from_inline("""
import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # Portfolio optimization logic
        portfolio_data = event.get('portfolio', {})
        
        # This would contain your portfolio optimization algorithms
        # For now, returning a sample response
        
        optimized_portfolio = {
            'stocks': 60,
            'bonds': 30,
            'alternatives': 10,
            'expected_return': 7.5,
            'risk_score': 6.2
        }
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'optimized_portfolio': optimized_portfolio,
                'input_portfolio': portfolio_data
            })
        }
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
            """),
            role=lambda_execution_role,
            timeout=Duration.minutes(5)
        )

        # Bedrock Knowledge Base (commented out - requires OpenSearch Serverless collection)
        # Note: To enable this, first create an OpenSearch Serverless collection
        # and update the collection_arn below
        
        # knowledge_base = bedrock.CfnKnowledgeBase(
        #     self, "InvestmentKnowledgeBase",
        #     name="investment-advisor-kb",
        #     description="Knowledge base for investment advisory information",
        #     role_arn=bedrock_agent_role.role_arn,
        #     knowledge_base_configuration=bedrock.CfnKnowledgeBase.KnowledgeBaseConfigurationProperty(
        #         type="VECTOR",
        #         vector_knowledge_base_configuration=bedrock.CfnKnowledgeBase.VectorKnowledgeBaseConfigurationProperty(
        #             embedding_model_arn="arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1"
        #         )
        #     ),
        #     storage_configuration=bedrock.CfnKnowledgeBase.StorageConfigurationProperty(
        #         type="OPENSEARCH_SERVERLESS",
        #         opensearch_serverless_configuration=bedrock.CfnKnowledgeBase.OpenSearchServerlessConfigurationProperty(
        #             collection_arn="arn:aws:aoss:us-east-1:944308403469:collection/your-collection-id",
        #             vector_index_name="investment-index",
        #             field_mapping=bedrock.CfnKnowledgeBase.OpenSearchServerlessFieldMappingProperty(
        #                 vector_field="vector",
        #                 text_field="text",
        #                 metadata_field="metadata"
        #             )
        #         )
        #     )
        # )

        # Outputs
        CfnOutput(
            self, "InvestmentDataBucketName",
            value=investment_data_bucket.bucket_name,
            description="S3 bucket for investment data"
        )

        CfnOutput(
            self, "KnowledgeBaseBucketName",
            value=knowledge_base_bucket.bucket_name,
            description="S3 bucket for knowledge base documents"
        )

        CfnOutput(
            self, "InvestmentAnalyzerLambdaArn",
            value=investment_analyzer_lambda.function_arn,
            description="ARN of the investment analyzer Lambda function"
        )

        CfnOutput(
            self, "PortfolioOptimizerLambdaArn",
            value=portfolio_optimizer_lambda.function_arn,
            description="ARN of the portfolio optimizer Lambda function"
        )

        CfnOutput(
            self, "BedrockAgentRoleArn",
            value=bedrock_agent_role.role_arn,
            description="ARN of the Bedrock agent role"
        )
