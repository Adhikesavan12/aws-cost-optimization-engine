from unittest.mock import Mock, patch

from src.metrics import publish_metrics


@patch("src.metrics.cloudwatch")
def test_publish_metrics(mock_cloudwatch):

    publish_metrics(
        snapshots_analyzed=10,
        snapshots_deleted=3,
        snapshots_skipped=7,
        cleanup_errors=0
    )

    mock_cloudwatch.put_metric_data.assert_called_once()

    call_args = mock_cloudwatch.put_metric_data.call_args

    assert call_args.kwargs["Namespace"] == "AWS/CostOptimizer"

    metrics = call_args.kwargs["MetricData"]

    assert len(metrics) == 4

    assert metrics[0]["MetricName"] == "SnapshotsAnalyzed"
    assert metrics[0]["Value"] == 10

    assert metrics[1]["MetricName"] == "SnapshotsDeleted"
    assert metrics[1]["Value"] == 3

    assert metrics[2]["MetricName"] == "SnapshotsSkipped"
    assert metrics[2]["Value"] == 7

    assert metrics[3]["MetricName"] == "CleanupErrors"
    assert metrics[3]["Value"] == 0