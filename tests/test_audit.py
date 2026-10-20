from src.audit import build_audit_report, upload_audit_report


def test_build_audit_report():

    candidates = [
        {"snapshot_id": "snap-123"},
        {"snapshot_id": "snap-456"}
    ]

    deleted = [
        "snap-123"
    ]

    skipped = [
        {"snapshot_id": "snap-789"}
    ]

    errors = []

    report = build_audit_report(
        candidates,
        deleted,
        skipped,
        errors
    )

    assert report["summary"]["candidates"] == 2
    assert report["summary"]["deleted"] == 1
    assert report["summary"]["skipped"] == 1
    assert report["summary"]["errors"] == 0

    assert report["deleted_snapshots"] == [
        "snap-123"
    ]

    assert report["errors"] == []


def test_upload_audit_report():

    class FakeS3:

        def __init__(self):
            self.uploaded = None

        def put_object(self, **kwargs):
            self.uploaded = kwargs

    s3 = FakeS3()

    report = {
        "summary": {
            "deleted": 2
        }
    }

    key = upload_audit_report(
        s3,
        "cost-optimizer-audit",
        report
    )

    assert key.startswith("reports/")

    assert s3.uploaded["Bucket"] == (
        "cost-optimizer-audit"
    )

    assert s3.uploaded["ContentType"] == (
        "application/json"
    )

    assert '"deleted": 2' in s3.uploaded["Body"]