from hypothesis import given, strategies as st
from photo_print_order_L7 import parse_order, file_size_average, payable_amount

@given(st.text() | st.none())
def test_parse_order_no_crash(s):
    try:
        parse_order(s)
    except (ValueError, TypeError, AttributeError):
        pass  # Expected exceptions for malformed fuzz inputs

@given(st.text() | st.none())
def test_file_size_average_no_crash(s):
    try:
        file_size_average(s)
    except (ValueError, TypeError, AttributeError, ZeroDivisionError):
        pass  # Expected exceptions for malformed CSV / empty inputs

@given(st.text() | st.none())
def test_payable_amount_no_crash(s):
    try:
        payable_amount(s)
    except (ValueError, TypeError, AttributeError):
        pass  # Expected exceptions for malformed amount|discount strings