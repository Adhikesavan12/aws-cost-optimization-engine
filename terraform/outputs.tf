output "audit_bucket_name" {
  description = "S3 bucket used for cost optimization audit reports"
  value       = aws_s3_bucket.audit.bucket
}