import block0
import block1
import md5
import lowlevel

fileName = "prefix.txt"


def findCollision():
    # IV = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]
    IV = [4009666844, 4185421068, 320656731, 1175793337]

    # msg1block0 = block0.find_block0(IV)
    msg1block0 = [4283288562, 656939853, 2106128531, 573736039, 1971245164, 3224215086, 2054686251, 3634841136,
                  3421764953, 1238117710, 2478663659, 2011068342, 3314879358, 166074220, 1909976678, 3880091990]

    IHV = IV
    IHV = md5.md5_compress(IHV, msg1block0)

    # msg1block1 = block1.find_block1(IHV)
    msg1block1 = [2341741213, 1654785416, 1272051245, 1543617655, 2735747523, 3883016052, 1862321035, 3599261579,
                  880334291, 467469207, 986188088, 2835778531, 1421249962, 2805981121, 1288019170, 4214318262]

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
    return msg1block0, msg1block1, msg2block0, msg2block1


def write_to_file(array, f):
    for num in array:
        b = num.to_bytes(4, 'little')
        f.write(b)


m1b0, m1b1, m2b0, m2b1 = findCollision()
with open('prefix.txt', 'rb') as f1, open('prefix_msg1.txt', 'wb') as f2, open('prefix_msg2.txt', 'wb') as f3:
    # TODO: add padding after prefix and strip newline
    # for line in f1:
    #     f2.write(bytes(line))
    #     f3.write(bytes(line))
    write_to_file(m1b0, f2)
    write_to_file(m1b1, f2)
    write_to_file(m2b0, f3)
    write_to_file(m2b1, f3)

# MD5IV = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]
