"""Limits from the DS1000Z/MSO1000Z performance verification guide.

DC Gain Accuracy, channel 1. Full scale is 8 times the vertical scale.
Below 10 mV/div the limit is 4 percent. At 10 mV/div and above it is 3 percent.
"""

SCALES_V_PER_DIV = (
    0.001,
    0.002,
    0.005,
    0.01,
    0.02,
    0.05,
    0.1,
    0.2,
    0.5,
    1.0,
    2.0,
    5.0,
    10.0,
)

HORIZONTAL_S_PER_DIV = 100e-6
AVERAGES = 32


def full_scale_volts(volts_per_div):
    return 8.0 * volts_per_div


def limit_percent(volts_per_div):
    if volts_per_div < 0.01:
        return 4.0
    return 3.0


def stimulus_volts(volts_per_div):
    """The guide uses +3 and -3 times the current vertical scale."""
    return 3.0 * volts_per_div


def relative_error_percent(
    vavg_positive,
    vavg_negative,
    vout_positive,
    vout_negative,
    volts_per_div,
    divisions=8.0,
):
    numerator = abs((vavg_positive - vavg_negative) - (vout_positive - vout_negative))
    return numerator / (divisions * volts_per_div) * 100.0
