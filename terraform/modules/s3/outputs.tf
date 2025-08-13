# S3 Module Outputs

output "data_bucket_name" {
  description = "Name of the investment data bucket"
  value       = aws_s3_bucket.investment_data.bucket
}

output "data_bucket_arn" {
  description = "ARN of the investment data bucket"
  value       = aws_s3_bucket.investment_data.arn
}

output "knowledge_base_bucket_name" {
  description = "Name of the knowledge base bucket"
  value       = aws_s3_bucket.knowledge_base.bucket
}

output "knowledge_base_bucket_arn" {
  description = "ARN of the knowledge base bucket"
  value       = aws_s3_bucket.knowledge_base.arn
}

output "assets_bucket_name" {
  description = "Name of the assets bucket"
  value       = aws_s3_bucket.assets.bucket
}

output "assets_bucket_arn" {
  description = "ARN of the assets bucket"
  value       = aws_s3_bucket.assets.arn
}
