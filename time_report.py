"""
Run timing report on functions

New implementation (numpy-free):

Raspberry Pi 2:
write2812(num_leds=  8):   0.51 ms
write2812(num_leds= 64):   3.29 ms
write2812(num_leds=144):   7.74 ms
write2812(num_leds=300):  16.14 ms

Previous implementation:

Raspberry Pi Zero:
write2812_numpy4    (nLED=  8):   3.45 ms
write2812_numpy4    (nLED= 64):   6.24 ms
write2812_numpy4    (nLED=144):  10.15 ms
write2812_numpy4    (nLED=300):  17.53 ms
write2812_numpy8    (nLED=  8):   4.03 ms
write2812_numpy8    (nLED= 64):   7.31 ms
write2812_numpy8    (nLED=144):  11.83 ms
write2812_pylist4   (nLED=  8):   1.41 ms
write2812_pylist4   (nLED= 64):   9.80 ms
write2812_pylist4   (nLED=144):  21.03 ms
write2812_pylist4   (nLED=300):  44.20 ms
write2812_pylist8   (nLED=  8):   1.75 ms
write2812_pylist8   (nLED= 64):  12.47 ms
write2812_pylist8   (nLED=144):  27.21 ms


Raspberry Pi 3:
write2812_numpy4    (nLED=  8):   1.57 ms
write2812_numpy4    (nLED= 64):   4.98 ms
write2812_numpy4    (nLED=144):   9.75 ms
write2812_numpy4    (nLED=300):  19.01 ms
write2812_numpy8    (nLED=  8):   1.81 ms
write2812_numpy8    (nLED= 64):   5.66 ms
write2812_numpy8    (nLED=144):  11.07 ms
write2812_pylist4   (nLED=  8):   0.96 ms
write2812_pylist4   (nLED= 64):   6.97 ms
write2812_pylist4   (nLED=144):  15.51 ms
write2812_pylist4   (nLED=300):  32.12 ms
write2812_pylist8   (nLED=  8):   1.08 ms
write2812_pylist8   (nLED= 64):   7.87 ms
write2812_pylist8   (nLED=144):  17.57 ms

"""

import timeit

_SETUP = """import spidev, ws2812; spi=spidev.SpiDev();
spi.open(0,0)
n=[[i%30,4*(i%3),i%7] for i in range({num_leds})]
ws2812.write2812(spi, n)
"""
_STMT = "ws2812.write2812(spi, n)"
_NUM_CALLS = 200

for num_leds in [8, 64, 144, 300]:
    _timeit = timeit.timeit(stmt=_STMT,
                            setup=_SETUP.format(num_leds=num_leds),
                            number=_NUM_CALLS)
    print("write2812(num_leds={num_leds:3d}): {ms:6.2f} ms".format(num_leds=num_leds,
                                                                   ms=1000 * _timeit / _NUM_CALLS))
