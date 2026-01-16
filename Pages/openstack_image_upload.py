#!/usr/bin/env python3
"""
openstack_auto_error_image_upload.py
------------------------------------
Automatically marks instances stuck in image upload (snapshot)
state for too long as ERROR.

Author: SARAN Service Error Automation
"""

import subprocess
import json
from datetime import datetime, timedelta

# ---------- CONFIG ----------
TIMEOUT_MINUTES = 3  # How long to wait before forcing ERROR
TASK_STATE_TARGET = "image_uploading"
# ----------------------------

def run(cmd):
    """Run a shell command and return its output."""
    try:
        return subprocess.check_output(cmd, shell=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f" Command failed: {e.cmd}")
        return ""

def mark_instance_error(server_id, name, task_state):
    """Force instance to ERROR."""
    print(f"[ACTION] Instance '{name}' ({server_id}) stuck in {task_state} → setting ERROR")
    run(f"openstack server set --state error {server_id}")

def main():
    print("=== OpenStack Auto-Error Monitor (Image Upload Tasks) ===")
    now = datetime.utcnow()

    # Get all instances (in all projects)
    server_list_json = run("openstack server list --all-projects -f json")
    if not server_list_json.strip():
        print("No instances found.")
        return

    try:
        servers = json.loads(server_list_json)
    except json.JSONDecodeError:
        print(" Failed to parse server list JSON.")
        return

    for server in servers:
        server_id = server["ID"]
        name = server["Name"]

        # Get full details of the instance
        details_json = run(f"openstack server show {server_id} -f json")
        if not details_json.strip():
            continue

        try:
            details = json.loads(details_json)
        except json.JSONDecodeError:
            print(f" Failed to parse JSON for {server_id}")
            continue

        task_state = details.get("OS-EXT-STS:task_state")
        updated_time_str = details.get("updated")

        if not updated_time_str:
            continue

        # Parse timestamp (UTC)
        try:
            updated_time = datetime.strptime(updated_time_str, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            continue

        # Calculate how long it’s been stuck
        age_min = (now - updated_time).total_seconds() / 60

        if task_state == TASK_STATE_TARGET:
            if age_min > TIMEOUT_MINUTES:
                mark_instance_error(server_id, name, task_state)
            else:
                print(f"Instance '{name}' ({server_id}) still uploading ({age_min:.1f} min) → OK")
        else:
            print(f"Instance '{name}' task={task_state} → skip")

if __name__ == "__main__":
    main()
