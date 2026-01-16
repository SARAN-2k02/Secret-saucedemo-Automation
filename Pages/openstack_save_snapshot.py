#!/usr/bin/env python3
import subprocess
import json
from datetime import datetime, timezone

# === CONFIG ===
MAX_ALLOWED_TIME = 5    # minutes
LOG_FILE = "/var/log/openstack_auto_error_image_save.log"

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(msg)

def run_cmd(cmd):
    """Run shell command and return stdout"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            log(f"[ERROR] Command failed: {cmd}\n{result.stderr}")
            return None
    except Exception as e:
        log(f"[EXCEPTION] {cmd}: {e}")
        return None

def get_all_images():
    """Return all images with their ID, Name, and Status"""
    output = run_cmd("openstack image list --all -f json")
    if not output:
        return []
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        log("[ERROR] Failed to parse JSON output of image list.")
        return []

def get_image_created_at(image_id):
    """Fetch the Created At timestamp for a single image"""
    output = run_cmd(f"openstack image show {image_id} -f json")
    if not output:
        return None
    try:
        data = json.loads(output)
        # Handle both 'created_at' and 'Created At'
        return data.get("created_at") or data.get("Created At")
    except Exception as e:
        log(f"[ERROR] Cannot parse created_at for {image_id}: {e}")
        return None

def check_and_deactivate_stuck_images():
    images = get_all_images()
    now = datetime.now(timezone.utc)

    for img in images:
        img_id = img.get("ID")
        img_name = img.get("Name")
        status = img.get("Status", "").lower()

        # only process 'saving' state
        if status != "saving":
            continue

        created_at_str = get_image_created_at(img_id)
        if not created_at_str:
            log(f"[WARN] No created_at for '{img_name}' ({img_id}) — skipping")
            continue

        try:
            # Format example: 2025-10-06T09:12:45Z
            if created_at_str.endswith("Z"):
                created_at_str = created_at_str.replace("Z", "+0000")
            created_dt = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            log(f"[WARN] Invalid date format for {img_name}: {created_at_str}")
            continue

        elapsed_minutes = (now - created_dt).total_seconds() / 60

        if elapsed_minutes > MAX_ALLOWED_TIME:
            log(f"[ACTION] Image '{img_name}' ({img_id}) stuck in '{status}' for {elapsed_minutes:.1f} min → deactivating")
            run_cmd(f"openstack image set --deactivate {img_id}")
        else:
            log(f"[INFO] Image '{img_name}' in '{status}' for {elapsed_minutes:.1f} min → OK")

if __name__ == "__main__":
    log("=== OpenStack Auto-Error (Snapshot Image Monitor) ===")
    check_and_deactivate_stuck_images()
