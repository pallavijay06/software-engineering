import pytest
from ski_resort_pass import process_resort_bookings, check_chairlift_anemometer


# --- Input validation ---

def test_invalid_groups_not_list():
    with pytest.raises(ValueError):
        process_resort_bookings("not_a_list", 10.0)


def test_invalid_negative_facility_fee():
    with pytest.raises(ValueError):
        process_resort_bookings([], -1.0)


# --- Inactive group is skipped ---

def test_inactive_group_zero_sales():
    groups = [{"is_active": False, "duration": "full_day", "skiers": [{"age": 30}]}]
    result = process_resort_bookings(groups, 10.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


# --- Pass durations ---

def test_full_day_adult():
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": False,
               "skiers": [{"age": 30, "gear_rental": False, "blackout_override": False}]}]
    result = process_resort_bookings(groups, 15.0)
    assert result == {"total_revenue": 80.0, "status": "COMPLETED"}


def test_half_day_adult():
    groups = [{"is_active": True, "duration": "half_day", "includes_lodge_locker": False,
               "skiers": [{"age": 30, "gear_rental": False, "blackout_override": False}]}]
    result = process_resort_bookings(groups, 15.0)
    assert result == {"total_revenue": 50.0, "status": "COMPLETED"}


def test_season_adult():
    groups = [{"is_active": True, "duration": "season", "includes_lodge_locker": False,
               "skiers": [{"age": 30, "gear_rental": False, "blackout_override": False}]}]
    result = process_resort_bookings(groups, 15.0)
    assert result == {"total_revenue": 300.0, "status": "COMPLETED"}


def test_invalid_duration_rejected():
    # invalid duration increments rejected_passes and continues
    groups = [{"is_active": True, "duration": "weekly", "includes_lodge_locker": False,
               "skiers": [{"age": 30}]}]
    result = process_resort_bookings(groups, 10.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


# --- Age categories ---

def test_child_age_full_day():
    # age 8 < 12 → 80 * 0.60 = 48.0
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": False,
               "skiers": [{"age": 8, "gear_rental": False, "blackout_override": False}]}]
    result = process_resort_bookings(groups, 15.0)
    assert result == {"total_revenue": 48.0, "status": "COMPLETED"}


def test_senior_age_full_day():
    # age 70 >= 65 → 80 * 0.70 = 56.0
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": False,
               "skiers": [{"age": 70, "gear_rental": False, "blackout_override": False}]}]
    result = process_resort_bookings(groups, 15.0)
    assert result == {"total_revenue": 56.0, "status": "COMPLETED"}


def test_invalid_age_zero_rejected():
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": False,
               "skiers": [{"age": 0, "gear_rental": False, "blackout_override": False}]}]
    result = process_resort_bookings(groups, 15.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_invalid_age_negative_rejected():
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": False,
               "skiers": [{"age": -5, "gear_rental": False, "blackout_override": False}]}]
    result = process_resort_bookings(groups, 15.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


# --- Gear rental ---

def test_gear_rental_adds_35():
    # adult full_day + gear: 80 + 35 = 115.0
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": False,
               "skiers": [{"age": 30, "gear_rental": True, "blackout_override": False}]}]
    result = process_resort_bookings(groups, 15.0)
    assert result == {"total_revenue": 115.0, "status": "COMPLETED"}


# --- Blackout override ---

def test_blackout_override_full_day():
    # blackout on full_day: 80 * 0.50 = 40.0, rejected_passes += 1
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": False,
               "skiers": [{"age": 30, "gear_rental": False, "blackout_override": True}]}]
    result = process_resort_bookings(groups, 15.0)
    assert result == {"total_revenue": 40.0, "status": "COMPLETED"}


def test_blackout_override_half_day_zeroes_group():
    # blackout on half_day: group_total set to 0 and break
    groups = [{"is_active": True, "duration": "half_day", "includes_lodge_locker": False,
               "skiers": [{"age": 30, "gear_rental": False, "blackout_override": True}]}]
    result = process_resort_bookings(groups, 15.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


# --- Lodge locker fee ---

def test_lodge_locker_adds_facility_fee():
    # adult full_day + lodge locker (fee=20): 80 + 20 = 100.0
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": True,
               "skiers": [{"age": 30, "gear_rental": False, "blackout_override": False}]}]
    result = process_resort_bookings(groups, 20.0)
    assert result == {"total_revenue": 100.0, "status": "COMPLETED"}


# --- Status: ZERO_SALES ---

def test_empty_groups_zero_sales():
    result = process_resort_bookings([], 10.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


# --- Status: AUDIT_REVIEW (rejected_passes > 4) ---

def test_audit_review_triggered():
    # 5 skiers with age=0 → 5 rejections → AUDIT_REVIEW
    skiers = [{"age": 0, "gear_rental": False, "blackout_override": False}] * 5
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": False,
               "skiers": skiers}]
    result = process_resort_bookings(groups, 10.0)
    assert result["status"] == "AUDIT_REVIEW"


# --- check_chairlift_anemometer ---

def test_anemometer_no_data_empty_list():
    assert check_chairlift_anemometer([]) == "NO_DATA"


def test_anemometer_safe_operation():
    assert check_chairlift_anemometer([[30, 40, 44]]) == "SAFE_OPERATION"


def test_anemometer_suspend_lift():
    # two consecutive readings > 45
    assert check_chairlift_anemometer([[46, 47]]) == "SUSPEND_LIFT"


def test_anemometer_single_gust_then_safe():
    # one gust then drops — streak resets, no suspension
    assert check_chairlift_anemometer([[46, 30, 46]]) == "SAFE_OPERATION"
