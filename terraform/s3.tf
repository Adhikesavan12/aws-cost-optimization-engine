resource "aws_s3_bucket" "audit" {
  bucket_prefix = "aws-cost-optimizer-audit-"

  tags = {
    Name        = "AWS Cost Optimizer Audit"
    Project     = "aws-cost-optimization-engine"
    Environment = "dev"
  }
}

# Block all public access to the audit bucket
resource "aws_s3_bucket_public_access_block" "audit" {
  bucket = aws_s3_bucket.audit.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Encrypt objects at rest using S3-managed SSE
resource "aws_s3_bucket_server_side_encryption_configuration" "audit" {
  bucket = aws_s3_bucket.audit.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Keep previous versions of audit reports
resource "aws_s3_bucket_versioning" "audit" {
  bucket = aws_s3_bucket.audit.id

  versioning_configuration {
    status = "Enabled"
  }
}