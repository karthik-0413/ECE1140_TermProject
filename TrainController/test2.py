# braking.py
def calculate_speed(u, a, t):
    """
    Calculate the speed of the train after time t with deceleration a.

    Parameters:
    u (float): Initial speed (m/s).
    a (float): Deceleration (m/s^2).
    t (float): Time (s).

    Returns:
    float: Speed after time t.
    """
    return max(u + a * t, 0)  # Ensure speed doesn't go below 0
