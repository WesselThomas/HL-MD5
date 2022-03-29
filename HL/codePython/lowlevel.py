import random, datetime

# FOR GOOD RUNNING
# seed32_1 = int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
# seed32_2 = 0x12345678

# FOR TESTING BLOCK0 - PATH 10
# seed32_1 = 1647198749
# seed32_2 = 0x12345678

# FOR TESTING BLOCK1 - PATH 10
# seed32_1 = 812771879
# seed32_2 = 511236490

# FOR TESTING BLOCK0 - PATH W
# seed32_1 = 1648067483
# seed32_2 = 0x12345678

# FOR TESTING BLOCK1 - PATH W
# seed32_1 = 4263289614
# seed32_2 = 3438395266

# FOR TESTING BLOCK0 - PATH 00
# seed32_1 = 1648152120
# seed32_2 = 0x12345678

# FOR TESTING BLOCK1 - PATH 00
# seed32_1 = 3044920037
# seed32_2 = 3411837156

# FOR TESTING BLOCK0 - PATH 11
# seed32_1 = 1648199592
# seed32_2 = 0x12345678

# FOR TESTING BLOCK1 - PATH 11
# seed32_1 = 3656520534
# seed32_2 = 200389396

# FOR TESTING BLOCK0 - PATH 01
# seed32_1 = 1648219594
# seed32_2 = 0x12345678

# FOR TESTING BLOCK1 - PATH 01
seed32_1 = 60943824
seed32_2 = 947762648

def trunc(val):
    return val & 0xFFFFFFFF


def xrng64():
    global seed32_1, seed32_2

    t = seed32_1 ^ trunc(seed32_1 << 10)
    seed32_1 = seed32_2
    seed32_2 = (seed32_2 ^ (seed32_2 >> 10)) ^ (t ^ (t >> 13))

    return seed32_1
