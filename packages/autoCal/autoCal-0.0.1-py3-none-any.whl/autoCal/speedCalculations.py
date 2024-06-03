import helperConverters
import unitConverters

def wheel_rpm_to_kmph(wheel_rpm: float, tyre_size: float) -> float:
    """Calculates speed in km/h from wheel rpm

    Args:
        wheel_rpm (float): RPM of wheel
        tyre_size (float): diameter of tyre in meters

    Returns:
        float: Speed in km/h
    """
    meters_ph = wheel_rpm * 60 * helperConverters.diameter_to_circumference(tyre_size)
    return meters_ph / 1000

def wheel_rpm_to_mph(wheel_rpm: float, tyre_size: float) -> float:
    """Calculates speed in miles per hour from wheel rpm

    Args:
        wheel_rpm (float): RPM of wheel
        tyre_size (float): diameter of tyre in meters

    Returns:
        float: speed in miles per hour
    """
    kmph = wheel_rpm_to_kmph(wheel_rpm, tyre_size)
    return unitConverters.kmph_to_mph(kmph)

def kmph_to_wheel_rpm(kmph: float, tyre_size: float) -> float:
    """Calculates wheel rpm from speed in kmph

    Args:
        kmph (float): speed in kmph
        tyre_size (float): diameter of tyre in meters

    Returns:
        float: wheel rpm
    """
    circumference = helperConverters.diameter_to_circumference(tyre_size)
    meter_per_min = (kmph * 1000) / 60
    return meter_per_min / circumference

def mph_to_wheel_rpm(mph: float, tyre_size: float) -> float:
    """Calculates wheel rpm from speed in miles per hour

    Args:
        mph (float): speed in miles per hour
        tyre_size (float): diameter of tyre in meters

    Returns:
        float: wheel rpm
    """
    kmph = unitConverters.mph_to_kmph(mph)
    return kmph_to_wheel_rpm(kmph, tyre_size)

def wheel_rpm_to_time_required_for_one_wheel_rotation(rpm: float) -> float:
    """Calculates time required for one wheel rotation from rpm

    Args:
        rpm (float): rpm of wheel

    Returns:
        float: time (seconds) required for one wheel rotation
    """
    return 60 / rpm

def kmph_to_time_required_for_one_wheel_rotation(kmph: float, tyre_size: float) -> float:
    """Calculates time required for one wheel rotation from speed in kmph

    Args:
        kmph (float): speed in kmph
        tyre_size (float): diameter of tyre in meters

    Returns:
        float: time (seconds) required for one wheel rotation
    """
    rpm = kmph_to_wheel_rpm(kmph, tyre_size)
    return wheel_rpm_to_time_required_for_one_wheel_rotation(rpm)

def mph_to_time_required_for_one_wheel_rotation(mph: float, tyre_size: float) -> float:
    """Calculates time required for one wheel rotation from speed in miles per hour

    Args:
        mph (float): speed in miles per hour
        tyre_size (float): diameter of tyre in meters

    Returns:
        float: time (seconds) required for one wheel rotation
    """
    rpm = mph_to_wheel_rpm(mph, tyre_size)
    return wheel_rpm_to_time_required_for_one_wheel_rotation(rpm)