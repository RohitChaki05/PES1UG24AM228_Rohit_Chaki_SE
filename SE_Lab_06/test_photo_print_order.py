import pytest
from photo_print_order import extra_print_charge, order_valid, dispatch_status

# --- extra_print_charge tests ---
def test_extra_print_charge_invalid_size():
    with pytest.raises(ValueError, match="unknown print size"):
        extra_print_charge("10x12", 10, "matte", False)

def test_extra_print_charge_invalid_copies():
    with pytest.raises(ValueError, match="invalid copies"):
        extra_print_charge("4x6", -5, "matte", False)

def test_extra_print_charge_included_or_less():
    assert extra_print_charge("4x6", 10, "matte", False) == 0

def test_extra_print_charge_member_adjustment():
    assert extra_print_charge("4x6", 30, "matte", True) == 20

def test_extra_print_charge_non_matte_and_high_extra():
    assert extra_print_charge("8x10", 70, "glossy", True) == 540

def test_extra_print_charge_canvas_high_extra():
    assert extra_print_charge("5x7", 80, "canvas", False) == 910


# --- order_valid tests ---
def test_order_valid_rush_true():
    assert order_valid(10, 40, True) is True
    assert order_valid(10, 60, True) is False

def test_order_valid_rush_false_high_file():
    assert order_valid(30, 100, False) is False

def test_order_valid_rush_false_normal_file():
    assert order_valid(10, 400, False) is True
    assert order_valid(10, 600, False) is False


# --- dispatch_status tests ---
def test_dispatch_status_scenarios():
    # On time branch
    assert dispatch_status(30, True, False) == "on_time"
    
    # Tight branch
    assert dispatch_status(33, False, True) == "tight"
    
    # Missed branch
    assert dispatch_status(5, False, False) == "missed"