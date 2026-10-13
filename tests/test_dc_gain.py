import unittest

from scope_verify.sequence import load_sequence, run_dc_gain_channel1
from scope_verify.sim import SimulatedCalibrator, SimulatedScope


class DcGainChannel1Tests(unittest.TestCase):
    def test_ideal_scope_passes_every_scale(self):
        calibrator = SimulatedCalibrator()
        results = run_dc_gain_channel1(SimulatedScope(calibrator), calibrator)

        self.assertEqual(len(results), len(load_sequence()["scales_v_per_div"]))
        self.assertTrue(all(result.passed for result in results))
        self.assertEqual(results[0].limit, 4.0)
        self.assertEqual(results[-1].limit, 3.0)

    def test_five_percent_gain_error_fails_the_three_percent_scales(self):
        calibrator = SimulatedCalibrator()
        scope = SimulatedScope(calibrator, gain_error=0.05)
        results = run_dc_gain_channel1(scope, calibrator)

        small = [result for result in results if result.volts_per_div < 0.01]
        large = [result for result in results if result.volts_per_div >= 0.01]
        self.assertTrue(all(result.passed for result in small))
        self.assertTrue(all(not result.passed for result in large))


if __name__ == "__main__":
    unittest.main()
