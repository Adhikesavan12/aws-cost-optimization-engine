resource "aws_s3_bucket" "audit" {
  bucket_prefix = "aws-cost-optimizer-audit-"

  tags = {
    Name        = "AWS Cost Optimizer Audit"
    Project     = "aws-cost-optimization-engine"
    Environment = "dev"
  }
}