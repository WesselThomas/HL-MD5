import block0
import block1
import md5

def findCollision():
    # IV = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]
    IV = [4009666844, 4185421068, 320656731, 1175793337]

    b0 = block0.find_block0(IV)

    IHV = IV
    IHV = md5.md5_compress(IHV, b0)

    b1 = block1.find_block1(IHV)

    print("block0")

findCollision()
