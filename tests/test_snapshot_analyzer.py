from datetime import datetime, timezone, timedelta

from src.snapshot_analyzer import analyze_snapshots


def make_snapshot(
    snapshot_id,
    age_days,
    volume_id=None,
    protected=False
):
    snapshot = {
        "SnapshotId": snapshot_id,
        "StartTime": datetime.now(timezone.utc)
        - timedelta(days=age_days),
    }

    if volume_id:
        snapshot["VolumeId"] = volume_id

    if protected:
        snapshot["Tags"] = [
            {
                "Key": "Protected",
                "Value": "true"
            }
        ]

    return snapshot


def test_recent_snapshot_is_skipped():

    snapshots = [
        make_snapshot(
            snapshot_id="snap-recent",
            age_days=10
        )
    ]

    volumes = {}

    candidates, skipped = analyze_snapshots(
        snapshots,
        volumes
    )

    assert len(candidates) == 0
    assert skipped[0]["reason"] == "snapshot_not_old_enough"


def test_old_snapshot_with_existing_volume_is_skipped():

    snapshots = [
        make_snapshot(
            snapshot_id="snap-old",
            age_days=120,
            volume_id="vol-123"
        )
    ]

    volumes = {
        "vol-123": {
            "VolumeId": "vol-123"
        }
    }

    candidates, skipped = analyze_snapshots(
        snapshots,
        volumes
    )

    assert len(candidates) == 0
    assert skipped[0]["reason"] == "source_volume_still_exists"


def test_old_snapshot_with_deleted_volume_is_candidate():

    snapshots = [
        make_snapshot(
            snapshot_id="snap-orphan",
            age_days=120,
            volume_id="vol-deleted"
        )
    ]

    volumes = {}

    candidates, skipped = analyze_snapshots(
        snapshots,
        volumes
    )

    assert len(candidates) == 1
    assert candidates[0]["snapshot_id"] == "snap-orphan"


def test_protected_snapshot_is_skipped():

    snapshots = [
        make_snapshot(
            snapshot_id="snap-protected",
            age_days=120,
            protected=True
        )
    ]

    volumes = {}

    candidates, skipped = analyze_snapshots(
        snapshots,
        volumes
    )

    assert len(candidates) == 0
    assert skipped[0]["reason"] == "protected_snapshot"