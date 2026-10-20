import os


RETENTION_DAYS = int(
    os.getenv("RETENTION_DAYS", "90")
)

AUDIT_BUCKET = os.getenv(
    "AUDIT_BUCKET",
    ""
)
DRY_RUN = (
    os.getenv("DRY_RUN", "true").lower() == "true"
)

PROTECTED_TAG_KEY = os.getenv(
    "PROTECTED_TAG_KEY",
    "Protected"
)

PROTECTED_TAG_VALUE = os.getenv(
    "PROTECTED_TAG_VALUE",
    "true"
)