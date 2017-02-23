#!/usr/bin/python
"""
Interface WS2812B led strip by SPI bus (using spidev)
"""
import spidev

# encoded byte tables
# we present each bit as 3 bits (oversampling by a factor of 3)
#   zero is represented as 0b100
#   one is represented as 0b110
# so each byte is actually represented as 3 bytes

# the following are tables to avoid repeated computations
# and are sent via spi as high, medium, low at 3* required HZ
ENCODE_H = (
    0x92,
    0x93,
    0x9a,
    0x9b,
    0xd2,
    0xd3,
    0xda,
    0xdb
)

ENCODE_M = (
    0x49,
    0x4d,
    0x69,
    0x6d
)

ENCODE_L = (
    0x24,
    0x26,
    0x34,
    0x36,
    0xa4,
    0xa6,
    0xb4,
    0xb6
)

SPI_XFER_SPEED = 2400000

def write2812(_spi, data):
    """
    Encodes list of GBR led colors and sends it thru SPI bus
    """
    tx_data = []
    for rgb in data:
        for val in rgb:
            tx_data.append(ENCODE_H[(val >> 5) & 0x07])
            tx_data.append(ENCODE_M[(val >> 3) & 0x03])
            tx_data.append(ENCODE_L[(val >> 0) & 0x07])

    _spi.xfer(tx_data, SPI_XFER_SPEED)

def __main():
    import getopt
    import sys

    def _usage():
        pass

    def test_fixed(_spi):
        """
        write fixed pattern for 8 LEDs
        This will send the following colors:
           Red, Green, Blue,
           Purple, Cyan, Yellow,
           Black(off), White
        """
        write2812(_spi, [[10, 0, 0], [0, 10, 0], [0, 0, 10],
                         [0, 10, 10], [10, 0, 10], [10, 10, 0],
                         [0, 0, 0], [10, 10, 10]])

    try:
        opts, _ = getopt.getopt(sys.argv[1:], "hn:c:t", ["help", "num_leds=", "color=", "test"])
    except getopt.GetoptError as err:
        print(str(err)) # will print something like "option -a not recognized"
        _usage()
        sys.exit(2)
    color = None
    num_leds = 8
    do_test = False
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            _usage()
            sys.exit()
        elif opt in ("-c", "--color"):
            color = eval(arg)
        elif opt in ("-n", "--num_leds"):
            num_leds = int(arg)
        elif opt in ("-t", "--test"):
            do_test = True
        else:
            assert False, "unhandled option: %s" % opt

    spi = spidev.SpiDev()
    spi.open(0, 0)

    if color != None:
        write2812(spi, color * num_leds)
    elif do_test:
        test_fixed(spi)
    else:
        _usage()

if __name__ == "__main__":
    __main()
