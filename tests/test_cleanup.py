from src.cleanup import cleanup_snapshots


def test_dry_run_does_not_delete():

    class FakeEC2:
        def delete_snapshot(self, SnapshotId):
            raise AssertionError("Snapshot should not be deleted")

    candidates = [
        {"snapshot_id": "snap-123"}
    ]

    deleted, skipped, errors = cleanup_snapshots(
        FakeEC2(),
        candidates
    )

    assert deleted == []
    assert skipped == ["snap-123"]
    assert errors == []