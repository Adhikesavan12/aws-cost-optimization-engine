variable "aws_region" {
  description = "AWS region for the cost optimization engine"
  type        = string
  default     = "us-east-1"
}
variable "alert_email" {
  description = "Email address for cost optimizer alerts"
  type        = string
}