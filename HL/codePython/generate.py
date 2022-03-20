import block0
import block1
import md5
import lowlevel


def findCollision():
    # IV = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]
    IV = [4009666844, 4185421068, 320656731, 1175793337]

    msg1block0 = block0.find_block0(IV)

    IHV = IV
    IHV = md5.md5_compress(IHV, msg1block0)

    msg1block1 = block1.find_block1(IHV)

    msg2block0 = [0] * 16
    msg2block1 = [0] * 16
    for i in range(16):
        msg2block0[i] = msg1block0[i]
        msg2block1[i] = msg1block1[i]

    msg2block0[4] = lowlevel.trunc(msg2block0[4] + (1 << 31))
    msg2block0[11] = lowlevel.trunc(msg2block0[11] + (1 << 15))
    msg2block0[14] = lowlevel.trunc(msg2block0[14] + (1 << 31))
    msg2block1[4] = lowlevel.trunc(msg2block1[4] + (1 << 31))
    msg2block1[11] = lowlevel.sub(msg2block1[11], (1 << 15))
    msg2block1[14] = lowlevel.trunc(msg2block1[14] + (1 << 31))

    print("FINISHED!")

findCollision()
