import lowlevel
import b1s11
import b1s10
import b1s01
import b1s00
import b1wang


def find_block1(IV, q, i):
    for k in range(5*i):
        lowlevel.xrng64()

    if ((IV[1] ^ IV[2]) & (1 << 31)) == 0 and ((IV[1] ^ IV[3]) & (1 << 31)) == 0 and (IV[3] & (1 << 25)) == 0 and (
            IV[2] & (1 << 25)) == 0 and (IV[1] & (1 << 25)) == 0 and ((IV[2] ^ IV[1]) & 1) == 0:

        IV2 = [(IV[0] + (1 << 31)) & 0xFFFFFFFF, (IV[1] + (1 << 31) + (1 << 25)) & 0xFFFFFFFF,
               (IV[2] + (1 << 31) + (1 << 25)) & 0xFFFFFFFF, (IV[3] + (1 << 31) + (1 << 25)) & 0xFFFFFFFF]

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

        b1[4] = (b1[4] + (1 << 31)) & 0xFFFFFFFF
        b1[11] = (b1[11] + (1 << 15)) & 0xFFFFFFFF
        b1[14] = (b1[14] + (1 << 31)) & 0xFFFFFFFF

    else:
        print("W")
        b1 = b1wang.find_block1_wang(IV)

    q.put(b1)
    return b1
