# Investment Advisor - Terraform Variables

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "investment-advisor"
}

# VPC Configuration
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

# ECS Configuration
variable "streamlit_image" {
  description = "Docker image for Streamlit application"
  type        = string
  default     = "investment-advisor-streamlit:latest"
}

variable "ecs_cpu" {
  description = "CPU units for ECS task"
  type        = number
  default     = 512
}

variable "ecs_memory" {
  description = "Memory for ECS task"
  type        = number
  default     = 1024
}

variable "desired_count" {
  description = "Desired number of ECS tasks"
  type        = number
  default     = 2
}

# RDS Configuration
variable "enable_rds" {
  description = "Enable RDS database"
  type        = bool
  default     = false
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "investment_advisor"
}

variable "db_username" {
  description = "Database username"
  type        = string
  default     = "admin"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
  default     = ""
}

# Bedrock Configuration
variable "bedrock_models" {
  description = "List of Bedrock models to enable"
  type        = list(string)
  default = [
    "amazon.titan-text-express-v1",
    "amazon.nova-pro-v1:0",
    "anthropic.claude-3-haiku-20240307-v1:0"
  ]
}

# MCP Configuration
variable "mcp_servers" {
  description = "MCP server configurations"
  type = map(object({
    command = string
    args    = list(string)
    env     = map(string)
  }))
  default = {
    aws = {
      command = "npx"
      args    = ["@modelcontextprotocol/server-aws"]
      env     = {}
    }
    bedrock = {
      command = "python"
      args    = ["-m", "mcp_server_bedrock"]
      env     = {}
    }
  }
}

# Monitoring
variable "enable_monitoring" {
  description = "Enable CloudWatch monitoring"
  type        = bool
  default     = true
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 30
}
