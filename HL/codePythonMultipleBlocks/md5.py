import lowlevel


def MD5_STEP(f, a, b, c, d, m, ac, rc):
    a = lowlevel.trunc(a + f(b, c, d) + m + ac)
    a = lowlevel.trunc((lowlevel.trunc(a << rc) | a >> (32-rc)) + b)
    return a


def MD5_REVERSE_STEP(t, AC, RC, block, Q, Qoff):
    block[t] = lowlevel.sub(Q[Qoff + t + 1], Q[Qoff + t])
    block[t] = lowlevel.sub(
        lowlevel.sub(
            lowlevel.sub(
                RR(block[t], RC),
                FF(Q[Qoff + t], Q[Qoff + t - 1], Q[Qoff + t - 2])
            ),
            Q[Qoff + t - 3]),
        AC)
    return block


def FF(b, c, d):
    return d ^ (b & (c ^ d))


def GG(b, c, d):
    return c ^ (d & (b ^ c))


def HH(b, c, d):
    return b ^ c ^ d


def II(b, c, d):
    return c ^ (b | ~d)


def RL(x, n):
    return lowlevel.trunc(x << n) | (x >> (32 - n))


def RR(x, n):
    return (x >> n) | lowlevel.trunc(x << (32 - n))


def md5_compress(ihv, block):
    a = ihv[0]
    b = ihv[1]
    c = ihv[2]
    d = ihv[3]

    a = MD5_STEP(FF, a, b, c, d, block[0], 0xd76aa478, 7)
    d = MD5_STEP(FF, d, a, b, c, block[1], 0xe8c7b756, 12)
    c = MD5_STEP(FF, c, d, a, b, block[2], 0x242070db, 17)
    b = MD5_STEP(FF, b, c, d, a, block[3], 0xc1bdceee, 22)
    a = MD5_STEP(FF, a, b, c, d, block[4], 0xf57c0faf, 7)
    d = MD5_STEP(FF, d, a, b, c, block[5], 0x4787c62a, 12)
    c = MD5_STEP(FF, c, d, a, b, block[6], 0xa8304613, 17)
    b = MD5_STEP(FF, b, c, d, a, block[7], 0xfd469501, 22)
    a = MD5_STEP(FF, a, b, c, d, block[8], 0x698098d8, 7)
    d = MD5_STEP(FF, d, a, b, c, block[9], 0x8b44f7af, 12)
    c = MD5_STEP(FF, c, d, a, b, block[10], 0xffff5bb1, 17)
    b = MD5_STEP(FF, b, c, d, a, block[11], 0x895cd7be, 22)
    a = MD5_STEP(FF, a, b, c, d, block[12], 0x6b901122, 7)
    d = MD5_STEP(FF, d, a, b, c, block[13], 0xfd987193, 12)
    c = MD5_STEP(FF, c, d, a, b, block[14], 0xa679438e, 17)
    b = MD5_STEP(FF, b, c, d, a, block[15], 0x49b40821, 22)
    a = MD5_STEP(GG, a, b, c, d, block[1], 0xf61e2562, 5)
    d = MD5_STEP(GG, d, a, b, c, block[6], 0xc040b340, 9)
    c = MD5_STEP(GG, c, d, a, b, block[11], 0x265e5a51, 14)
    b = MD5_STEP(GG, b, c, d, a, block[0], 0xe9b6c7aa, 20)
    a = MD5_STEP(GG, a, b, c, d, block[5], 0xd62f105d, 5)
    d = MD5_STEP(GG, d, a, b, c, block[10], 0x02441453, 9)
    c = MD5_STEP(GG, c, d, a, b, block[15], 0xd8a1e681, 14)
    b = MD5_STEP(GG, b, c, d, a, block[4], 0xe7d3fbc8, 20)
    a = MD5_STEP(GG, a, b, c, d, block[9], 0x21e1cde6, 5)
    d = MD5_STEP(GG, d, a, b, c, block[14], 0xc33707d6, 9)
    c = MD5_STEP(GG, c, d, a, b, block[3], 0xf4d50d87, 14)
    b = MD5_STEP(GG, b, c, d, a, block[8], 0x455a14ed, 20)
    a = MD5_STEP(GG, a, b, c, d, block[13], 0xa9e3e905, 5)
    d = MD5_STEP(GG, d, a, b, c, block[2], 0xfcefa3f8, 9)
    c = MD5_STEP(GG, c, d, a, b, block[7], 0x676f02d9, 14)
    b = MD5_STEP(GG, b, c, d, a, block[12], 0x8d2a4c8a, 20)
    a = MD5_STEP(HH, a, b, c, d, block[5], 0xfffa3942, 4)
    d = MD5_STEP(HH, d, a, b, c, block[8], 0x8771f681, 11)
    c = MD5_STEP(HH, c, d, a, b, block[11], 0x6d9d6122, 16)
    b = MD5_STEP(HH, b, c, d, a, block[14], 0xfde5380c, 23)
    a = MD5_STEP(HH, a, b, c, d, block[1], 0xa4beea44, 4)
    d = MD5_STEP(HH, d, a, b, c, block[4], 0x4bdecfa9, 11)
    c = MD5_STEP(HH, c, d, a, b, block[7], 0xf6bb4b60, 16)
    b = MD5_STEP(HH, b, c, d, a, block[10], 0xbebfbc70, 23)
    a = MD5_STEP(HH, a, b, c, d, block[13], 0x289b7ec6, 4)
    d = MD5_STEP(HH, d, a, b, c, block[0], 0xeaa127fa, 11)
    c = MD5_STEP(HH, c, d, a, b, block[3], 0xd4ef3085, 16)
    b = MD5_STEP(HH, b, c, d, a, block[6], 0x04881d05, 23)
    a = MD5_STEP(HH, a, b, c, d, block[9], 0xd9d4d039, 4)
    d = MD5_STEP(HH, d, a, b, c, block[12], 0xe6db99e5, 11)
    c = MD5_STEP(HH, c, d, a, b, block[15], 0x1fa27cf8, 16)
    b = MD5_STEP(HH, b, c, d, a, block[2], 0xc4ac5665, 23)
    a = MD5_STEP(II, a, b, c, d, block[0], 0xf4292244, 6)
    d = MD5_STEP(II, d, a, b, c, block[7], 0x432aff97, 10)
    c = MD5_STEP(II, c, d, a, b, block[14], 0xab9423a7, 15)
    b = MD5_STEP(II, b, c, d, a, block[5], 0xfc93a039, 21)
    a = MD5_STEP(II, a, b, c, d, block[12], 0x655b59c3, 6)
    d = MD5_STEP(II, d, a, b, c, block[3], 0x8f0ccc92, 10)
    c = MD5_STEP(II, c, d, a, b, block[10], 0xffeff47d, 15)
    b = MD5_STEP(II, b, c, d, a, block[1], 0x85845dd1, 21)
    a = MD5_STEP(II, a, b, c, d, block[8], 0x6fa87e4f, 6)
    d = MD5_STEP(II, d, a, b, c, block[15], 0xfe2ce6e0, 10)
    c = MD5_STEP(II, c, d, a, b, block[6], 0xa3014314, 15)
    b = MD5_STEP(II, b, c, d, a, block[13], 0x4e0811a1, 21)
    a = MD5_STEP(II, a, b, c, d, block[4], 0xf7537e82, 6)
    d = MD5_STEP(II, d, a, b, c, block[11], 0xbd3af235, 10)
    c = MD5_STEP(II, c, d, a, b, block[2], 0x2ad7d2bb, 15)
    b = MD5_STEP(II, b, c, d, a, block[9], 0xeb86d391, 21)

    ihv[0] = lowlevel.trunc(ihv[0] + a)
    ihv[1] = lowlevel.trunc(ihv[1] + b)
    ihv[2] = lowlevel.trunc(ihv[2] + c)
    ihv[3] = lowlevel.trunc(ihv[3] + d)

    return ihv
