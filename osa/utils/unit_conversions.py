import math


def m_to_nm(measurement: float):
    """
    Converts measurement in meters to nanometers
    :param measurement: Value in meters
    :return: Value in nanometers
    """
    return measurement * math.pow(10, 9)


def nm_to_m(measurement: float):
    """
    Converts measurement in nanometers to meters
    :param measurement: Value in nanometers
    :return: Value in nanometers
    """
    return measurement * math.pow(10, -9)


def wavelength_to_frequency(wavelength: float):
    """
    Converts a wavelength in nm to a frequency in THz,
    assuming the wave is travelling at the speed of light (c).
    :param wavelength: Wavelength in nanometers
    :return: Frequency in THz
    """
    c = 299792458
    f_in_hz = c / nm_to_m(wavelength)
    f_in_thz = f_in_hz * math.pow(10, -12)
    return f_in_thz
