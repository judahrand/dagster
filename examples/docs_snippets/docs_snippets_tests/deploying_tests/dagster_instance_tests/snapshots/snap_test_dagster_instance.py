# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_instance_yaml 1"] = [
    "auto_materialize",
    "code_servers",
    "compute_logs",
    "local_artifact_storage",
    "retention",
    "run_coordinator",
    "run_launcher",
    "run_monitoring",
    "run_retries",
    "schedules",
    "sensors",
    "storage",
    "telemetry",
]
