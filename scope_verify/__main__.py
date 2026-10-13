"""Run the channel 1 DC gain sequence on the simulator.

python -m scope_verify
python -m scope_verify --gain-error 0.05
"""

import argparse
import sys

from scope_verify.sequence import run_dc_gain_channel1
from scope_verify.sim import SimulatedCalibrator, SimulatedScope


def main(argv=None):
    parser = argparse.ArgumentParser(description="DS1000Z channel 1 DC gain sequence")
    parser.add_argument(
        "--gain-error",
        type=float,
        default=0.0,
        help="Fractional error added by the simulated scope, for example 0.05",
    )
    args = parser.parse_args(argv)

    calibrator = SimulatedCalibrator()
    scope = SimulatedScope(calibrator, gain_error=args.gain_error)
    results = run_dc_gain_channel1(scope, calibrator)

    failed = 0
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        if not result.passed:
            failed += 1
        print(
            "%s  CH1  %s  error %6.2f%%  limit %.0f%%"
            % (status, _scale(result.volts_per_div), result.error_percent, result.limit)
        )
    print("%d of %d scales passed" % (len(results) - failed, len(results)))
    return 1 if failed else 0


def _scale(volts_per_div):
    if volts_per_div < 1:
        return "%g mV/div" % (volts_per_div * 1000.0)
    return "%g V/div" % volts_per_div


if __name__ == "__main__":
    sys.exit(main())
