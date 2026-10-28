"""Manage warehouse assets and their maintenance schedules."""
import json
import tempfile
from datetime import datetime, timedelta

# Global state
assets = {}
SERVICE_INTERVAL_DAYS = 90


def register_asset(asset_id, machine_type, logs=None):
    """Register a warehouse asset and its maintenance history."""
    if logs is None:
        logs = []
    assets[asset_id] = {"type": machine_type,
                        "last_service": datetime.now().strftime("%Y-%m-%d")}
    logs.append(asset_id)
    print("Registered", asset_id, "- total registrations this run:", len(logs))


def update_service_date(asset_id, date):
    """Update an asset's last service date."""
    if asset_id not in assets:
        raise ValueError(f"Asset {asset_id} is not registered")

    assets[asset_id]["last_service"] = date


def due_for_inspection():
    """Return assets whose inspections are due."""
    due = []
    for a, asset in assets.items():
        last = datetime.strptime(asset["last_service"], "%Y-%m-%d")
        if datetime.now() - last > timedelta(days=SERVICE_INTERVAL_DAYS):
            due.append(a)
    return due


def change_interval(days):
    """Update the inspection interval."""
    global SERVICE_INTERVAL_DAYS
    if days <= 0:
        raise ValueError("Inspection interval must be positive")
    SERVICE_INTERVAL_DAYS = days


def export_service_report(file="maintenance.json"):
    """Export maintenance records to JSON."""
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(assets, indent=2))
    print("Report written to " + file)


def write_scratch_copy():
    """Write maintenance records to a temporary JSON file."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        delete=False,
        encoding="utf-8",
    ) as f:
        f.write(json.dumps(assets))
        path = f.name

    print("Scratch copy at", path)


def print_alerts():
    """Print alerts for assets due for inspection."""
    for a in due_for_inspection():
        print("ALERT: inspection overdue for", a, assets[a]["type"])


def main():
    """Run the warehouse maintenance system."""
    register_asset("FL-01", "Forklift")
    register_asset("CV-07", "Conveyor")
    register_asset("PJ-12", "Pallet Jack")
    register_asset("FL-01", "Crane")
    update_service_date("FL-01", "2025-01-15")
    try:
        update_service_date("XX-99", "2025-02-01")
    except ValueError as e:
        print(f"Could not update service date: {e}")
    try:
        change_interval(-30)
    except ValueError as e:
        print(f"Could not change inspection interval: {e}")
    d = input("Last service date for CV-07 (YYYY-MM-DD, Enter to skip): ")
    if d:
        update_service_date("CV-07", d)
    if not assets:
        raise ValueError("No assets registered")
    print_alerts()
    export_service_report()
    write_scratch_copy()


main()
