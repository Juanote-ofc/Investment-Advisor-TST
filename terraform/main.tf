# Investment Advisor - Main Terraform Configuration

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
  
  backend "s3" {
    bucket = "investment-advisor-terraform-state"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region  = var.aws_region
  profile = "Juanelo"
  
  default_tags {
    tags = {
      Project     = "InvestmentAdvisor"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Owner       = "Juanelo"
    }
  }
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_caller_identity" "current" {}

# Local values
locals {
  name_prefix = "${var.project_name}-${var.environment}"
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# VPC Module
module "vpc" {
  source = "./modules/vpc"
  
  name_prefix         = local.name_prefix
  cidr_block         = var.vpc_cidr
  availability_zones = data.aws_availability_zones.available.names
  
  tags = local.common_tags
}

# S3 Module
module "s3" {
  source = "./modules/s3"
  
  name_prefix = local.name_prefix
  
  tags = local.common_tags
}

# ECS Module for Streamlit
module "ecs" {
  source = "./modules/ecs"
  
  name_prefix    = local.name_prefix
  vpc_id         = module.vpc.vpc_id
  subnet_ids     = module.vpc.private_subnet_ids
  alb_subnet_ids = module.vpc.public_subnet_ids
  
  # Streamlit configuration
  streamlit_image = var.streamlit_image
  cpu             = var.ecs_cpu
  memory          = var.ecs_memory
  
  # Environment variables for Streamlit
  environment_variables = {
    AWS_REGION                = var.aws_region
    S3_BUCKET                = module.s3.data_bucket_name
    KNOWLEDGE_BASE_BUCKET    = module.s3.knowledge_base_bucket_name
    BEDROCK_REGION          = var.aws_region
    MCP_CONFIG_PATH         = "/app/mcp-config.json"
  }
  
  tags = local.common_tags
}

# Bedrock Module
module "bedrock" {
  source = "./modules/bedrock"
  
  name_prefix = local.name_prefix
  
  tags = local.common_tags
}

# RDS Module (Optional - for user data persistence)
module "rds" {
  source = "./modules/rds"
  count  = var.enable_rds ? 1 : 0
  
  name_prefix    = local.name_prefix
  vpc_id         = module.vpc.vpc_id
  subnet_ids     = module.vpc.private_subnet_ids
  
  db_name     = var.db_name
  db_username = var.db_username
  db_password = var.db_password
  
  tags = local.common_tags
}
