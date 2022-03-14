import random, datetime

# FOR GOOD RUNNING
# seed32_1 = int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

# FOR TESTING BLOCK0
# seed32_1 = 1647198749
# seed32_2 = 0x12345678

# FOR TESTING BLOCK1
seed32_1 = 812771879
seed32_2 = 511236490


def trunc(val):
    return val & 0xFFFFFFFF


def xrng64():
    global seed32_1, seed32_2

    t = seed32_1 ^ trunc(seed32_1 << 10)
    seed32_1 = seed32_2
    seed32_2 = (seed32_2 ^ (seed32_2 >> 10)) ^ (t ^ (t >> 13))

    return seed32_1


def sub(a, b):
    diff = a - b
    return diff % 2 ** 32

