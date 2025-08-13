# Bedrock Module Outputs

output "bedrock_execution_role_arn" {
  description = "ARN of the Bedrock execution role"
  value       = aws_iam_role.bedrock_execution_role.arn
}

output "bedrock_execution_role_name" {
  description = "Name of the Bedrock execution role"
  value       = aws_iam_role.bedrock_execution_role.name
}

output "bedrock_policy_arn" {
  description = "ARN of the Bedrock access policy"
  value       = aws_iam_policy.bedrock_model_access.arn
}

output "bedrock_log_group_name" {
  description = "Name of the Bedrock CloudWatch log group"
  value       = aws_cloudwatch_log_group.bedrock_logs.name
}
