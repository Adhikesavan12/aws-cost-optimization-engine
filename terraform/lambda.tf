data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda_package"
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_function" "cost_optimizer" {
  function_name = "aws-cost-optimizer"

  filename         = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256

  role    = aws_iam_role.lambda.arn
  handler = "src.handler.lambda_handler"
  runtime = "python3.11"

  timeout     = 300
  memory_size = 256

  environment {
    variables = {
      RETENTION_DAYS      = "90"
      DRY_RUN             = "true"
      PROTECTED_TAG_KEY   = "Protected"
      PROTECTED_TAG_VALUE = "true"
      AUDIT_BUCKET        = aws_s3_bucket.audit.bucket
    }
  }

  tags = {
    Project     = "aws-cost-optimization-engine"
    Environment = "dev"
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_logs
  ]
}