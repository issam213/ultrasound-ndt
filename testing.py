import numpy as np
from ultrasound import time_of_flight, echo_amplitude, calculate_depth

def test_time_of_flight():
    t = time_of_flight(0.1, 5920)
    expected = 2 * 0.1 / 5920
    assert abs(t - expected) < 1e-10
    print("test_time_of_flight passed")

def test_time_of_flight_positive():
    t = time_of_flight(0.1, 5920)
    assert t > 0
    print("test_time_of_flight_positive passed")

def test_echo_amplitude_decreases_with_depth():
    amp1 = echo_amplitude(0.1, 5920, 5e6)
    amp2 = echo_amplitude(0.2, 5920, 5e6)
    assert amp2 < amp1
    print("test_echo_amplitude_decreases_with_depth passed")

def test_calculate_depth():
    depth_original = 0.1
    t = time_of_flight(depth_original, 5920)
    depth_calculated = calculate_depth(t, 5920)
    assert abs(depth_calculated - depth_original) < 1e-10
    print("test_calculate_depth passed")

def test_amplitude_between_zero_and_one():
    amp = echo_amplitude(0.1, 5920, 5e6)
    assert 0 <= amp <= 1
    print("test_amplitude_between_zero_and_one passed")

if __name__ == "__main__":
    test_time_of_flight()
    test_time_of_flight_positive()
    test_echo_amplitude_decreases_with_depth()
    test_calculate_depth()
    test_amplitude_between_zero_and_one()
    print("\n All tests passed!")
