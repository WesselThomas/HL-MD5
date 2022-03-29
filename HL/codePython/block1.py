import lowlevel
import b1s11
import b1s10
import b1s01
import b1s00
import b1wang


def find_block1(IV):
    if ((IV[1] ^ IV[2]) & (1 << 31)) == 0 and ((IV[1] ^ IV[3]) & (1 << 31)) == 0 and (IV[3] & (1 << 25)) == 0 and (
            IV[2] & (1 << 25)) == 0 and (IV[1] & (1 << 25)) == 0 and ((IV[2] ^ IV[1]) & 1) == 0:

        IV2 = [lowlevel.trunc(IV[0] + (1 << 31)), lowlevel.trunc(IV[1] + (1 << 31) + (1 << 25)),
               lowlevel.trunc(IV[2] + (1 << 31) + (1 << 25)), lowlevel.trunc(IV[3] + (1 << 31) + (1 << 25))]

        b1 = [0] * 16

        if (IV[1] & (1 << 6)) != 0 and (IV[1] & 1) != 0:
            print("S11")
            b1 = b1s11.find_block1_stevens_11(IV2)
        elif (IV[1] & (1 << 6)) != 0 and (IV[1] & 1) == 0:
            print("S10")
            b1 = b1s10.find_block1_stevens_10(IV2)
        elif (IV[1] & (1 << 6)) == 0 and (IV[1] & 1) != 0:
            print("S01")
            b1 = b1s01.find_block1_stevens_01(IV2)
        else:
            print("S00")
            b1 = b1s00.find_block1_stevens_00(IV2)

        b1[4] = lowlevel.trunc(b1[4] + (1 << 31))
        b1[11] = lowlevel.trunc(b1[11] + (1 << 15))
        b1[14] = lowlevel.trunc(b1[14] + (1 << 31))
    else:
        print("W")
        b1 = b1wang.find_block1_wang(IV)

    return b1

# HARDCODED FOR 10
# IHV = [3716883887, 2888226514, 3763429312, 2550331037]
# find_block1(IHV)
