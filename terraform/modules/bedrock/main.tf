# Bedrock Module for Investment Advisor

# Note: Bedrock model access is managed through AWS Console
# This module creates IAM roles and policies for Bedrock access

# IAM Role for Bedrock access
resource "aws_iam_role" "bedrock_execution_role" {
  name = "${var.name_prefix}-bedrock-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = [
            "lambda.amazonaws.com",
            "bedrock.amazonaws.com"
          ]
        }
      }
    ]
  })

  tags = var.tags
}

# IAM Policy for Bedrock model access
resource "aws_iam_policy" "bedrock_model_access" {
  name        = "${var.name_prefix}-bedrock-model-access"
  description = "Policy for accessing Bedrock foundation models"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream",
          "bedrock:ListFoundationModels",
          "bedrock:GetFoundationModel"
        ]
        Resource = "*"
      }
    ]
  })

  tags = var.tags
}

# Attach policy to role
resource "aws_iam_role_policy_attachment" "bedrock_model_access" {
  role       = aws_iam_role.bedrock_execution_role.name
  policy_arn = aws_iam_policy.bedrock_model_access.arn
}

# CloudWatch Log Group for Bedrock operations
resource "aws_cloudwatch_log_group" "bedrock_logs" {
  name              = "/aws/bedrock/${var.name_prefix}"
  retention_in_days = 30

  tags = var.tags
}
