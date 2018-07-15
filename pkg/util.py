"""Utility functions."""

MIN_TEMPERATURE = 2700
MAX_TEMPERATURE = 6500


def kelvin_to_relative_temp(t):
    """
    Convert kelvin to relative temperature.

    t -- temperature to convert
    """
    return int((t - MIN_TEMPERATURE) * 100 /
               (MAX_TEMPERATURE - MIN_TEMPERATURE))


def relative_temp_to_kelvin(t):
    """
    Convert relative temperature to kelvin.

    t -- temperature to convert
    """
    return int(MIN_TEMPERATURE +
               (t * (MAX_TEMPERATURE - MIN_TEMPERATURE) / 100))
