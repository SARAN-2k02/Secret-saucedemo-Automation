#!/usr/bin/env python3
import subprocess
import json
import time

# ========== CONFIG ==========
CHECK_INTERVAL = 5  # in minutes
TASK_STATES_TO_ERROR = ["extending"]  # states to auto-error
# ============================

def get_all_volumes():
    try:
        output = subprocess.check_output(
            ["openstack", "volume", "list", "--all-projects", "-f", "json"],
            stderr=subprocess.DEVNULL
        )
        return json.loads(output)
    except Exception:
        return []

def get_volume_details(volume_id):
    try:
        output = subprocess.check_output(
            ["openstack", "volume", "show", volume_id, "-f", "json"],
            stderr=subprocess.DEVNULL
        )
        return json.loads(output)
    except Exception:
        return None

def set_volume_error(volume_id):
    subprocess.run(
        ["openstack", "volume", "set", "--state", "error", volume_id],
        stderr=subprocess.DEVNULL
    )

def main():
    print("=== OpenStack Auto-Error Monitor (Volume Extend Tasks) ===")
    volumes = get_all_volumes()

    for vol in volumes:
        vol_id = vol.get("ID")
        vol_name = vol.get("Name", "N/A")
        details = get_volume_details(vol_id)
        if not details:
            continue

        status = details.get("status")
        updated_at = details.get("updated_at")

        # Example: 2025-10-06T07:35:10.000000
        if not updated_at:
            continue

        # Convert to epoch time
        try:
            last_update = time.mktime(time.strptime(updated_at.split('.')[0], "%Y-%m-%dT%H:%M:%S"))
        except Exception:
            continue

        # Time difference in minutes
        time_diff_min = (time.time() - last_update) / 60

        if status in TASK_STATES_TO_ERROR and time_diff_min > CHECK_INTERVAL:
            print(f"[ACTION] Volume '{vol_name}' ({vol_id}) stuck in {status} → setting ERROR")
            set_volume_error(vol_id)
        else:
            print(f"Volume '{vol_name}' status={status} (last updated {int(time_diff_min)} mins ago) → skip")

if __name__ == "__main__":
    main()
