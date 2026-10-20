from datetime import datetime, timezone, timedelta

import boto3

from src.config import (
    RETENTION_DAYS,
    PROTECTED_TAG_KEY,
    PROTECTED_TAG_VALUE
)

def get_ec2_client():
    return boto3.client("ec2")


def get_all_snapshots(ec2):
    snapshots = []

    paginator = ec2.get_paginator("describe_snapshots")

    for page in paginator.paginate(OwnerIds=["self"]):
        snapshots.extend(page["Snapshots"])

    return snapshots


def get_all_volumes(ec2):
    volumes = {}

    paginator = ec2.get_paginator("describe_volumes")

    for page in paginator.paginate():
        for volume in page["Volumes"]:
            volumes[volume["VolumeId"]] = volume

    return volumes


def is_snapshot_old(snapshot):
    cutoff_date = datetime.now(timezone.utc) - timedelta(
        days=RETENTION_DAYS
    )

    snapshot_date = snapshot["StartTime"]

    return snapshot_date < cutoff_date


def get_snapshot_tags(snapshot):
    tags = {}

    for tag in snapshot.get("Tags", []):
        tags[tag["Key"]] = tag["Value"]

    return tags


def analyze_snapshots(snapshots, volumes):
    candidates = []
    skipped = []

    for snapshot in snapshots:

        snapshot_id = snapshot["SnapshotId"]
        volume_id = snapshot.get("VolumeId")

        # Rule 1: Snapshot must be older than retention period
        if not is_snapshot_old(snapshot):
            skipped.append({
                "snapshot_id": snapshot_id,
                "reason": "snapshot_not_old_enough"
            })
            continue

        # Rule 2: Protected snapshots must never be deleted
        tags = get_snapshot_tags(snapshot)

        if tags.get(PROTECTED_TAG_KEY, "").lower() == PROTECTED_TAG_VALUE.lower():
            skipped.append({
                "snapshot_id": snapshot_id,
                "reason": "protected_snapshot"
            })
            continue

        # Rule 3: Source volume must no longer exist
        if volume_id and volume_id in volumes:
            skipped.append({
                "snapshot_id": snapshot_id,
                "reason": "source_volume_still_exists"
            })
            continue

        candidates.append({
            "snapshot_id": snapshot_id,
            "volume_id": volume_id,
            "start_time": snapshot["StartTime"]
        })

    return candidates, skipped


def analyze_aws_snapshots():
    ec2 = get_ec2_client()

    snapshots = get_all_snapshots(ec2)
    volumes = get_all_volumes(ec2)

    candidates, skipped = analyze_snapshots(
        snapshots,
        volumes
    )

    return ec2, candidates, skipped