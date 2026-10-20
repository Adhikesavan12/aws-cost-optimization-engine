import json
from datetime import datetime, timezone


def build_audit_report(
    candidates,
    deleted,
    skipped,
    errors
):
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "candidates": len(candidates),
            "deleted": len(deleted),
            "skipped": len(skipped),
            "errors": len(errors)
        },
        "deleted_snapshots": deleted,
        "errors": errors
    }


def upload_audit_report(s3, bucket_name, report):
    timestamp = datetime.now(timezone.utc)

    key = (
        f"reports/"
        f"{timestamp.strftime('%Y/%m/%d')}/"
        f"cost-optimization-"
        f"{timestamp.strftime('%Y%m%d-%H%M%S')}.json"
    )

    s3.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=json.dumps(report, indent=2),
        ContentType="application/json"
    )

    return key