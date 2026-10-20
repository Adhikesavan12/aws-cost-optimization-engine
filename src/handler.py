import logging
from src.metrics import publish_metrics
from src.audit import build_audit_report, upload_audit_report
import boto3

from src.config import AUDIT_BUCKET

from src.cleanup import cleanup_snapshots
from src.snapshot_analyzer import analyze_aws_snapshots


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    logger.info("Starting AWS cost optimization scan")

    ec2, candidates, skipped = analyze_aws_snapshots()

    logger.info(
        "Snapshot analysis complete: %s candidates, %s skipped",
        len(candidates),
        len(skipped)
    )

    deleted, cleanup_skipped, errors = cleanup_snapshots(
        ec2,
        candidates
    )
    
    report = build_audit_report(
        candidates,
        deleted,
        skipped + cleanup_skipped,
        errors
    )
    
    if AUDIT_BUCKET:
        s3 = boto3.client("s3")

        upload_audit_report(
            s3,
            AUDIT_BUCKET,
            report
        )

        logger.info(
            "Audit report uploaded to S3 bucket: %s",
            AUDIT_BUCKET
        )

    logger.info(
        "Cleanup complete: %s deleted, %s skipped, %s errors",
        len(deleted),
        len(cleanup_skipped),
        len(errors)
    )

    result = {
        "candidates": len(candidates),
        "deleted": len(deleted),
        "skipped": len(skipped) + len(cleanup_skipped),
        "errors": len(errors)
    }
    publish_metrics(
        snapshots_analyzed=len(candidates) + len(skipped),
        snapshots_deleted=len(deleted),
        snapshots_skipped=len(skipped) + len(cleanup_skipped),
        cleanup_errors=len(errors)
    )

    logger.info("Cost optimization result: %s", result)

    return result