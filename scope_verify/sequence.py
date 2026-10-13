"""Channel 1 DC gain accuracy sequence.

The steps and limits come from sequences/dc_gain_ch1.yaml.
Only channel 1 is run. Channels 2 to 4 are the same steps later.
"""

from pathlib import Path

import yaml

from scope_verify.limits import relative_error_percent
from scope_verify.scpi import (
    acquire_average,
    channel_display,
    channel_offset,
    channel_probe,
    channel_scale,
    measure_vavg,
    timebase_scale,
)

SEQUENCE_PATH = Path(__file__).resolve().parents[1] / "sequences" / "dc_gain_ch1.yaml"


def load_sequence(path=None):
    with open(path or SEQUENCE_PATH, encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def limit_percent(plan, volts_per_div):
    for rule in plan["limits"]:
        below = rule.get("below_v_per_div")
        if below is None or volts_per_div < below:
            return float(rule["max_error_percent"])
    raise ValueError("No limit rule matched %s V/div" % volts_per_div)


class ScaleResult:
    def __init__(self, volts_per_div, vavg_positive, vavg_negative, error_percent, limit, passed):
        self.volts_per_div = volts_per_div
        self.vavg_positive = vavg_positive
        self.vavg_negative = vavg_negative
        self.error_percent = error_percent
        self.limit = limit
        self.passed = passed


def run_dc_gain_channel1(scope, calibrator, plan=None):
    plan = plan or load_sequence()
    setup = plan["setup"]
    channel = int(plan["channel"])
    factor = float(plan["measurement"]["stimulus_times_scale"])
    divisions = float(plan["measurement"]["full_scale_divisions"])

    calibrator.set_impedance_ohms(setup["impedance_ohms"])
    scope.write(channel_display(channel, True))
    scope.write(channel_probe(channel, setup["probe_ratio"]))
    scope.write(channel_offset(channel, setup["vertical_offset_v"]))
    scope.write(timebase_scale(setup["horizontal_s_per_div"]))
    for command in acquire_average(setup["averages"]):
        scope.write(command)

    results = []
    for volts_per_div in plan["scales_v_per_div"]:
        volts_per_div = float(volts_per_div)
        scope.write(channel_scale(channel, volts_per_div))
        vout_positive = factor * volts_per_div
        vout_negative = -vout_positive

        calibrator.output_dc(vout_positive)
        vavg_positive = scope.query_volts(measure_vavg(channel))
        calibrator.output_dc(vout_negative)
        vavg_negative = scope.query_volts(measure_vavg(channel))

        error = relative_error_percent(
            vavg_positive,
            vavg_negative,
            vout_positive,
            vout_negative,
            volts_per_div,
            divisions,
        )
        limit = limit_percent(plan, volts_per_div)
        results.append(
            ScaleResult(volts_per_div, vavg_positive, vavg_negative, error, limit, error <= limit)
        )

    scope.write(channel_display(channel, False))
    return results
