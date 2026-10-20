import boto3


cloudwatch = boto3.client("cloudwatch")


NAMESPACE = "AWS/CostOptimizer"


def publish_metrics(
    snapshots_analyzed,
    snapshots_deleted,
    snapshots_skipped,
    cleanup_errors
):
    metrics = [
        {
            "MetricName": "SnapshotsAnalyzed",
            "Value": snapshots_analyzed,
            "Unit": "Count"
        },
        {
            "MetricName": "SnapshotsDeleted",
            "Value": snapshots_deleted,
            "Unit": "Count"
        },
        {
            "MetricName": "SnapshotsSkipped",
            "Value": snapshots_skipped,
            "Unit": "Count"
        },
        {
            "MetricName": "CleanupErrors",
            "Value": cleanup_errors,
            "Unit": "Count"
        }
    ]

    cloudwatch.put_metric_data(
        Namespace=NAMESPACE,
        MetricData=metrics
    )   