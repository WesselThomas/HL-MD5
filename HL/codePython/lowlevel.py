import random, datetime

seed32_1 = int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
seed32_2 = 0x12345678;

def trunc(val, numbits=32):
    return val & (2 ** numbits - 1)


def xrng64():

    global seed32_1, seed32_2

    seed32_1 = trunc(seed32_1)
    seed32_1 = trunc(seed32_1)

    t = seed32_1 ^ trunc(seed32_1 << 10)
    seed32_1 = seed32_2
    seed32_2 = (seed32_2 ^ (seed32_2 >> 10)) ^ (t ^ (t >> 13))

    return seed32_1


def sub(a, b):
    diff = a - b
    return diff % 2**32

# 4294967296
