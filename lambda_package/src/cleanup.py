from src.config import DRY_RUN


def cleanup_snapshots(ec2, candidates):
    deleted = []
    skipped = []
    errors = []

    for snapshot in candidates:
        snapshot_id = snapshot["snapshot_id"]

        if DRY_RUN:
            print(f"[DRY RUN] Would delete {snapshot_id}")
            skipped.append(snapshot_id)
            continue

        try:
            ec2.delete_snapshot(SnapshotId=snapshot_id)

            print(f"Deleted snapshot {snapshot_id}")
            deleted.append(snapshot_id)

        except Exception as error:
            print(f"Failed to delete {snapshot_id}: {error}")
            errors.append({
                "snapshot_id": snapshot_id,
                "error": str(error)
            })

    return deleted, skipped, errors