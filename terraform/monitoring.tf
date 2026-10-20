resource "aws_sns_topic" "alerts" {
  name = "aws-cost-optimizer-alerts"

  tags = {
    Project     = "aws-cost-optimization-engine"
    Environment = "dev"
  }
}



resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

resource "aws_cloudwatch_metric_alarm" "cleanup_errors" {
  alarm_name        = "aws-cost-optimizer-cleanup-errors"
  alarm_description = "Alerts when snapshot cleanup encounters errors"

  namespace   = "AWS/CostOptimizer"
  metric_name = "CleanupErrors"

  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  threshold           = 0
  comparison_operator = "GreaterThanThreshold"

  alarm_actions = [
    aws_sns_topic.alerts.arn
  ]

  treat_missing_data = "notBreaching"
}