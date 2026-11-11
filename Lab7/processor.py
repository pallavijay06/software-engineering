
from datetime import datetime
import math


def parse_season_pass_validity(date_str):
    try:
        if not isinstance(date_str, str):
            return "Invalid date"

        date_str = date_str.strip()

        # Check the expected YYYY/MM/DD format
        parts = date_str.split('/')
        if len(parts) != 3:
            return "Invalid date"

        if not all(part.isdigit() for part in parts):
            return "Invalid date"

        if not (len(parts[0]) == 4 and
                len(parts[1]) == 2 and
                len(parts[2]) == 2):
            return "Invalid date"

        # Validate the actual calendar date
        date = datetime.strptime(date_str, "%Y/%m/%d")

        year = date.year
        month = date.month
        day = date.day

        valid = year >= 2026

        return (
            f"Pass Expiry: {year:04d}-{month:02d}-{day:02d} "
            f"({'VALID' if valid else 'EXPIRED'})"
        )

    except (ValueError, TypeError):
        return "Invalid date"


def compute_trail_gradient(elevation_str):
    try:
        if not isinstance(elevation_str, str):
            return None

        parts = elevation_str.split(':')

        if len(parts) != 2:
            return None

        drop = float(parts[0].strip())
        distance = float(parts[1].strip())

        if not math.isfinite(drop) or not math.isfinite(distance):
            return None

        if drop < 0 or distance <= 0:
            return None

        gradient_pct = (drop / distance) * 100.0

        return round(gradient_pct, 2)

    except (ValueError, TypeError, ZeroDivisionError):
        return None


def calculate_lift_access_tier(zone_code):
    try:
        if not isinstance(zone_code, str):
            return None

        prefix = zone_code.strip().upper()

        zone_rates = {
            "BEG": 35.0,
            "INT": 60.0,
            "ADV": 85.0,
            "ALL": 110.0
        }

        return zone_rates.get(prefix)

    except (ValueError, TypeError, AttributeError):
        return None


def main():
    print("==== Running parse_season_pass_validity ====")
    d_input = input("Enter pass expiry (YYYY/MM/DD): ")
    print(parse_season_pass_validity(d_input))

    print("\n==== Running compute_trail_gradient ====")
    e_input = input("Enter drop:distance (e.g. 250:1000): ")
    print("Gradient %:", compute_trail_gradient(e_input))

    print("\n==== Running calculate_lift_access_tier ====")
    z_input = input("Enter zone code (e.g. BEG, INT, ALL): ")
    print("Lift Pass Price: $", calculate_lift_access_tier(z_input))


if __name__ == "__main__":
    main()
