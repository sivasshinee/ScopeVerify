"""Stand-in for a scope and a DC calibrator. No instrument is opened."""


class SimulatedCalibrator:
    def __init__(self):
        self.impedance_ohms = None
        self.dc_volts = 0.0

    def set_impedance_ohms(self, ohms):
        self.impedance_ohms = ohms

    def output_dc(self, volts):
        self.dc_volts = volts


class SimulatedScope:
    """Returns the calibrator voltage as Vavg, plus an optional gain error."""

    def __init__(self, calibrator, gain_error=0.0):
        self.calibrator = calibrator
        self.gain_error = gain_error
        self.commands = []

    def write(self, command):
        self.commands.append(command)

    def query_volts(self, command):
        self.commands.append(command)
        return self.calibrator.dc_volts * (1.0 + self.gain_error)
