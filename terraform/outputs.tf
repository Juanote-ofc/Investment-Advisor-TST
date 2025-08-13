# Terraform Outputs

# VPC Outputs
output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

# S3 Outputs
output "s3_data_bucket" {
  description = "Name of the investment data S3 bucket"
  value       = module.s3.data_bucket_name
}

output "s3_knowledge_base_bucket" {
  description = "Name of the knowledge base S3 bucket"
  value       = module.s3.knowledge_base_bucket_name
}

output "s3_assets_bucket" {
  description = "Name of the assets S3 bucket"
  value       = module.s3.assets_bucket_name
}

# ECS Outputs
output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = module.ecs.cluster_name
}

output "ecs_service_name" {
  description = "Name of the ECS service"
  value       = module.ecs.service_name
}

output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = module.ecs.alb_dns_name
}

# Bedrock Outputs
output "bedrock_execution_role_arn" {
  description = "ARN of the Bedrock execution role"
  value       = module.bedrock.bedrock_execution_role_arn
}

# RDS Outputs (if enabled)
output "db_endpoint" {
  description = "RDS instance endpoint"
  value       = var.enable_rds ? module.rds[0].db_instance_endpoint : null
}

# Application URL
output "application_url" {
  description = "URL to access the Investment Advisor application"
  value       = "http://${module.ecs.alb_dns_name}"
}
