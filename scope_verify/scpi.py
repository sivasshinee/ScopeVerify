"""SCPI strings from the MSO1000Z/DS1000Z programming guide, PGA19108-1110."""


def channel_display(channel, on):
    state = "ON" if on else "OFF"
    return ":CHANnel%d:DISPlay %s" % (channel, state)


def channel_probe(channel, ratio):
    return ":CHANnel%d:PROBe %s" % (channel, _number(ratio))


def channel_scale(channel, volts_per_div):
    return ":CHANnel%d:SCALe %s" % (channel, _number(volts_per_div))


def channel_offset(channel, volts):
    return ":CHANnel%d:OFFSet %s" % (channel, _number(volts))


def timebase_scale(seconds_per_div):
    return ":TIMebase:MAIN:SCALe %s" % _number(seconds_per_div)


def acquire_average(count):
    return (
        ":ACQuire:TYPE AVERages",
        ":ACQuire:AVERages %d" % count,
    )


def measure_vavg(channel):
    return ":MEASure:ITEM? VAVG,CHANnel%d" % channel


def _number(value):
    return format(float(value), ".12g")
