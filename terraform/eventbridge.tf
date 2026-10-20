resource "aws_cloudwatch_event_rule" "cost_optimizer" {
  name                = "aws-cost-optimizer-schedule"
  description         = "Runs AWS cost optimization engine monthly"
  schedule_expression = "rate(30 days)"

  tags = {
    Project     = "aws-cost-optimization-engine"
    Environment = "dev"
  }
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule = aws_cloudwatch_event_rule.cost_optimizer.name
  arn  = aws_lambda_function.cost_optimizer.arn
}

resource "aws_lambda_permission" "eventbridge" {
  statement_id  = "AllowEventBridgeInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cost_optimizer.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.cost_optimizer.arn
}