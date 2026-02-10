# ═══════════════════════════════════════════════════════
# Terraform — MDM Lakehouse Infrastructure (AWS)
# ═══════════════════════════════════════════════════════

terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
  backend "s3" {
    bucket = "company-terraform-state"
    key    = "mdm-lakehouse/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" { region = var.region }

variable "region"      { default = "us-east-1" }
variable "environment" { default = "prod" }
variable "project"     { default = "mdm-lakehouse" }

locals {
  prefix = "${var.project}-${var.environment}"
}

# ─── S3 Lakehouse Bucket ───────────────────────────────
resource "aws_s3_bucket" "lakehouse" {
  bucket = "${local.prefix}-data"
  tags   = { Project = var.project, Environment = var.environment }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "lakehouse" {
  bucket = aws_s3_bucket.lakehouse.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.lakehouse.arn
    }
  }
}

resource "aws_s3_bucket_versioning" "lakehouse" {
  bucket = aws_s3_bucket.lakehouse.id
  versioning_configuration { status = "Enabled" }
}

# ─── KMS Key ──────────────────────────────────────────
resource "aws_kms_key" "lakehouse" {
  description = "MDM Lakehouse encryption key"
  enable_key_rotation = true
}

resource "aws_kms_alias" "lakehouse" {
  name          = "alias/${local.prefix}-key"
  target_key_id = aws_kms_key.lakehouse.key_id
}

# ─── IAM Role: Bedrock Claude Agent ───────────────────
resource "aws_iam_role" "bedrock_agent" {
  name = "${local.prefix}-bedrock-agent"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "bedrock.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "bedrock_agent_policy" {
  name = "${local.prefix}-bedrock-agent-policy"
  role = aws_iam_role.bedrock_agent.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"]
        Resource = "arn:aws:bedrock:${var.region}::foundation-model/anthropic.*"
      },
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:PutObject", "s3:ListBucket"]
        Resource = [aws_s3_bucket.lakehouse.arn, "${aws_s3_bucket.lakehouse.arn}/*"]
      },
      {
        Effect   = "Allow"
        Action   = ["glue:StartJobRun", "glue:GetJobRun", "glue:GetJob"]
        Resource = "arn:aws:glue:${var.region}:*:job/${local.prefix}-*"
      },
      {
        Effect   = "Allow"
        Action   = ["secretsmanager:GetSecretValue"]
        Resource = "arn:aws:secretsmanager:${var.region}:*:secret:mdm/*"
      },
      {
        Effect   = "Allow"
        Action   = ["kms:Decrypt", "kms:GenerateDataKey"]
        Resource = aws_kms_key.lakehouse.arn
      }
    ]
  })
}

# ─── IAM Role: Glue ETL ──────────────────────────────
resource "aws_iam_role" "glue_etl" {
  name = "${local.prefix}-glue-etl"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "glue.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

# ─── Glue Catalog Database ───────────────────────────
resource "aws_glue_catalog_database" "lakehouse" {
  name = replace(local.prefix, "-", "_")
}

# ─── Step Functions State Machine ────────────────────
resource "aws_sfn_state_machine" "pipeline" {
  name     = "${local.prefix}-pipeline"
  role_arn = aws_iam_role.step_functions.arn
  definition = file("${path.module}/step_functions.asl.json")
}

resource "aws_iam_role" "step_functions" {
  name = "${local.prefix}-stepfunctions"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "states.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

# ─── Outputs ─────────────────────────────────────────
output "lakehouse_bucket" { value = aws_s3_bucket.lakehouse.id }
output "kms_key_arn"       { value = aws_kms_key.lakehouse.arn }
output "bedrock_role_arn"  { value = aws_iam_role.bedrock_agent.arn }
output "pipeline_arn"      { value = aws_sfn_state_machine.pipeline.arn }
