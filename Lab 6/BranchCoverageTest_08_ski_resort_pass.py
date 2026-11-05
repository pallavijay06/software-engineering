import pytest
from ski_resort_pass import process_resort_bookings, check_chairlift_anemometer


# ============================================================
# process_resort_bookings — branch coverage
# ============================================================

# Branch: invalid input (both sides)
def test_invalid_groups_raises():
    with pytest.raises(ValueError):
        process_resort_bookings("bad", 10.0)


def test_invalid_fee_raises():
    with pytest.raises(ValueError):
        process_resort_bookings([], -5.0)


def test_valid_input_no_error():
    result = process_resort_bookings([], 0.0)
    assert result["status"] == "ZERO_SALES"


# Branch: group is_active True / False
def test_group_active_processed():
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": False,
               "skiers": [{"age": 25, "gear_rental": False, "blackout_override": False}]}]
    result = process_resort_bookings(groups, 10.0)
    assert result["total_revenue"] == 80.0


def test_group_inactive_skipped():
    groups = [{"is_active": False, "duration": "full_day", "skiers": [{"age": 25}]}]
    result = process_resort_bookings(groups, 10.0)
    assert result["status"] == "ZERO_SALES"


# Branch: duration == "season"
def test_duration_season():
    groups = [{"is_active": True, "duration": "season", "includes_lodge_locker": False,
               "skiers": [{"age": 30, "gear_rental": False, "blackout_override": False}]}]
    assert process_resort_bookings(groups, 0.0)["total_revenue"] == 300.0


# Branch: duration == "full_day"
def test_duration_full_day():
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": False,
               "skiers": [{"age": 30, "gear_rental": False, "blackout_override": False}]}]
    assert process_resort_bookings(groups, 0.0)["total_revenue"] == 80.0


# Branch: duration == "half_day"
def test_duration_half_day():
    groups = [{"is_active": True, "duration": "half_day", "includes_lodge_locker": False,
               "skiers": [{"age": 30, "gear_rental": False, "blackout_override": False}]}]
    assert process_resort_bookings(groups, 0.0)["total_revenue"] == 50.0


# Branch: duration is invalid → rejected_passes += 1, continue
def test_duration_invalid_continue():
    groups = [{"is_active": True, "duration": "monthly", "includes_lodge_locker": False,
               "skiers": [{"age": 30}]}]
    result = process_resort_bookings(groups, 0.0)
    assert result["status"] == "ZERO_SALES"


# Branch: age <= 0 (True and False)
def test_age_zero_rejected():
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": False,
               "skiers": [{"age": 0, "gear_rental": False, "blackout_override": False}]}]
    result = process_resort_bookings(groups, 0.0)
    assert result["status"] == "ZERO_SALES"


def test_age_positive_not_rejected():
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": False,
               "skiers": [{"age": 1, "gear_rental": False, "blackout_override": False}]}]
    # age 1 < 12 → child rate: 80 * 0.60 = 48.0
    assert process_resort_bookings(groups, 0.0)["total_revenue"] == 48.0


# Branch: blackout_override True — full_day (adds 50% rate, no break)
def test_blackout_full_day_adds_half_rate():
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": False,
               "skiers": [{"age": 30, "gear_rental": False, "blackout_override": True}]}]
    # 80 * 0.50 = 40.0
    assert process_resort_bookings(groups, 0.0)["total_revenue"] == 40.0


# Branch: blackout_override True — half_day (zeroes group_total and breaks)
def test_blackout_half_day_zeroes_and_breaks():
    groups = [{"is_active": True, "duration": "half_day", "includes_lodge_locker": False,
               "skiers": [
                   {"age": 30, "gear_rental": False, "blackout_override": True},
                   {"age": 25, "gear_rental": False, "blackout_override": False},  # never reached
               ]}]
    result = process_resort_bookings(groups, 0.0)
    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_SALES"


# Branch: blackout_override False — age < 12 (child)
def test_no_blackout_child():
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": False,
               "skiers": [{"age": 10, "gear_rental": False, "blackout_override": False}]}]
    # 80 * 0.60 = 48.0
    assert process_resort_bookings(groups, 0.0)["total_revenue"] == 48.0


# Branch: blackout_override False — age >= 65 (senior)
def test_no_blackout_senior():
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": False,
               "skiers": [{"age": 65, "gear_rental": False, "blackout_override": False}]}]
    # 80 * 0.70 = 56.0
    assert process_resort_bookings(groups, 0.0)["total_revenue"] == 56.0


# Branch: blackout_override False — adult (12 <= age < 65)
def test_no_blackout_adult():
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": False,
               "skiers": [{"age": 30, "gear_rental": False, "blackout_override": False}]}]
    assert process_resort_bookings(groups, 0.0)["total_revenue"] == 80.0


# Branch: gear_rental True / False
def test_gear_rental_true():
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": False,
               "skiers": [{"age": 30, "gear_rental": True, "blackout_override": False}]}]
    # 80 + 35 = 115.0
    assert process_resort_bookings(groups, 0.0)["total_revenue"] == 115.0


def test_gear_rental_false():
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": False,
               "skiers": [{"age": 30, "gear_rental": False, "blackout_override": False}]}]
    assert process_resort_bookings(groups, 0.0)["total_revenue"] == 80.0


# Branch: includes_lodge_locker True / False
def test_lodge_locker_true():
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": True,
               "skiers": [{"age": 30, "gear_rental": False, "blackout_override": False}]}]
    # 80 + 25 = 105.0
    assert process_resort_bookings(groups, 25.0)["total_revenue"] == 105.0


def test_lodge_locker_false():
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": False,
               "skiers": [{"age": 30, "gear_rental": False, "blackout_override": False}]}]
    assert process_resort_bookings(groups, 25.0)["total_revenue"] == 80.0


# Branch: rejected_passes > 4 → AUDIT_REVIEW
def test_audit_review_five_rejections():
    # 5 invalid-age skiers → 5 rejections
    skiers = [{"age": 0, "gear_rental": False, "blackout_override": False}] * 5
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": False,
               "skiers": skiers}]
    result = process_resort_bookings(groups, 0.0)
    assert result["status"] == "AUDIT_REVIEW"


def test_audit_review_not_triggered_four_rejections():
    # exactly 4 rejections → not AUDIT_REVIEW
    skiers = [{"age": 0, "gear_rental": False, "blackout_override": False}] * 4
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": False,
               "skiers": skiers}]
    result = process_resort_bookings(groups, 0.0)
    assert result["status"] == "ZERO_SALES"


# Branch: total_revenue == 0.0 → ZERO_SALES
def test_zero_sales_empty_groups():
    assert process_resort_bookings([], 10.0)["status"] == "ZERO_SALES"


# Branch: total_revenue > 0 → COMPLETED
def test_completed_status():
    groups = [{"is_active": True, "duration": "full_day", "includes_lodge_locker": False,
               "skiers": [{"age": 30, "gear_rental": False, "blackout_override": False}]}]
    assert process_resort_bookings(groups, 0.0)["status"] == "COMPLETED"


# ============================================================
# check_chairlift_anemometer — branch coverage
# ============================================================

# Branch: wind_streams is falsy → NO_DATA
def test_no_data_empty_list():
    assert check_chairlift_anemometer([]) == "NO_DATA"


# Branch: wind_streams is truthy, all readings safe → SAFE_OPERATION
def test_safe_all_below_45():
    assert check_chairlift_anemometer([[20, 30, 44]]) == "SAFE_OPERATION"


# Branch: speed_mph > 45 True, streak reaches 2 → SUSPEND_LIFT
def test_suspend_two_consecutive_gusts():
    assert check_chairlift_anemometer([[50, 60]]) == "SUSPEND_LIFT"


# Branch: speed_mph > 45 True but streak < 2 (only one gust then resets)
def test_single_gust_resets_no_suspend():
    assert check_chairlift_anemometer([[50, 30, 50]]) == "SAFE_OPERATION"


# Branch: speed_mph > 45 False → streak resets to 0
def test_gust_streak_resets_on_safe_reading():
    # 50 → streak=1, 30 → streak=0, 50 → streak=1, 30 → streak=0
    assert check_chairlift_anemometer([[50, 30, 50, 30]]) == "SAFE_OPERATION"


# Branch: multiple lift arrays, suspension in second array
def test_suspend_in_second_lift():
    assert check_chairlift_anemometer([[30, 40], [46, 47]]) == "SUSPEND_LIFT"


# Branch: multiple lift arrays, all safe
def test_multiple_lifts_all_safe():
    assert check_chairlift_anemometer([[30, 40], [44, 20]]) == "SAFE_OPERATION"


# Branch: exactly at boundary (speed == 45 is NOT > 45, so safe)
def test_boundary_exactly_45_is_safe():
    assert check_chairlift_anemometer([[45, 45]]) == "SAFE_OPERATION"


# Branch: speed just above boundary (46 > 45)
def test_boundary_46_counts_as_gust():
    assert check_chairlift_anemometer([[46, 46]]) == "SUSPEND_LIFT"
