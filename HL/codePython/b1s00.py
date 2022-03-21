import lowlevel
import md5


def find_block1_stevens_00(IV):
    print("S00")
    block = 16 * [0]
    Qoff = 3

    Q = [0] * 68
    Q[0] = IV[0]
    Q[1] = IV[3]
    Q[2] = IV[2]
    Q[3] = IV[1]

    q9q10mask = []
    q9q10size = (1 << 3)
    for k in range(q9q10size):
        new = ((k << 5) ^ (k << 12) ^ (k << 25)) & 0x08002020
        q9q10mask.append(new)

    q9mask = []
    q9size = (1 << 9)
    for k in range(q9size):
        new = ((k << 1) ^ (k << 3) ^ (k << 6) ^ (k << 8) ^ (k << 11) ^ (k << 14) ^ (k << 18)) & 0x04310d12
        q9mask.append(new)

    while True:
        aa = Q[Qoff] & 0x80000000

        Q[Qoff + 2] = (lowlevel.xrng64() & 0x49a0e73e) | 0x221f00c1 | aa
        Q[Qoff + 3] = (lowlevel.xrng64() & 0x0000040c) | 0x3fce1a71 | (Q[Qoff + 2] & 0x8000e000)
        Q[Qoff + 4] = (lowlevel.xrng64() & 0x00000004) | (0xa5f281a2 ^ (Q[Qoff + 3] & 0x80000008))
        Q[Qoff + 5] = (lowlevel.xrng64() & 0x00000004) | 0x67fd823b
        Q[Qoff + 6] = (lowlevel.xrng64() & 0x00001044) | 0x15e5829a
        Q[Qoff + 7] = (lowlevel.xrng64() & 0x00200806) | 0x950430b0
        Q[Qoff + 8] = (lowlevel.xrng64() & 0x60050110) | 0x1bd29ca2 | (Q[Qoff + 7] & 0x00000004)
        Q[Qoff + 9] = (lowlevel.xrng64() & 0x40044000) | 0xb8820004
        Q[Qoff + 10] = 0xf288b209 | (Q[Qoff + 9] & 0x00044000)
        Q[Qoff + 11] = (lowlevel.xrng64() & 0x12888008) | 0x85712f57
        Q[Qoff + 12] = (lowlevel.xrng64() & 0x1ed98d7f) | 0xc0023080 | (~Q[Qoff + 11] & 0x00200000)
        Q[Qoff + 13] = (lowlevel.xrng64() & 0x0efb1d77) | 0x1000c008
        Q[Qoff + 14] = (lowlevel.xrng64() & 0x0fff5d77) | 0xa000a288
        Q[Qoff + 15] = (lowlevel.xrng64() & 0x0efe7ff7) | 0xe0008000 | (~Q[Qoff + 14] & 0x00010000)
        Q[Qoff + 16] = (lowlevel.xrng64() & 0x0ffdffff) | 0xf0000000 | (~Q[Qoff + 15] & 0x00020000)

        block = md5.MD5_REVERSE_STEP(5, 0x4787c62a, 12, block, Q, Qoff)
        block = md5.MD5_REVERSE_STEP(6, 0xa8304613, 17, block, Q, Qoff)
        block = md5.MD5_REVERSE_STEP(7, 0xfd469501, 22, block, Q, Qoff)
        block = md5.MD5_REVERSE_STEP(11, 0x895cd7be, 22, block, Q, Qoff)
        block = md5.MD5_REVERSE_STEP(14, 0xa679438e, 17, block, Q, Qoff)
        block = md5.MD5_REVERSE_STEP(15, 0x49b40821, 22, block, Q, Qoff)

        tt17 = lowlevel.trunc(md5.GG(Q[Qoff + 16], Q[Qoff + 15], Q[Qoff + 14]) + Q[Qoff + 13] + 0xf61e2562)
        tt18 = lowlevel.trunc(Q[Qoff + 14] + 0xc040b340 + block[6])
        tt19 = lowlevel.trunc(Q[Qoff + 15] + 0x265e5a51 + block[11])

        tt0 = lowlevel.trunc(md5.FF(Q[Qoff + 0], Q[Qoff - 1], Q[Qoff - 2]) + Q[Qoff - 3] + 0xd76aa478)
        tt1 = lowlevel.trunc(Q[Qoff - 2] + 0xe8c7b756)
        q1a = 0x02020801 | (Q[Qoff + 0] & 0x80000000)

        counter = 0
        while counter < (1 << 12):
            counter += 1

            q1 = q1a | (lowlevel.xrng64() & 0x7dfdf7be)
            m1 = lowlevel.sub(Q[Qoff + 2], q1)
            m1 = md5.RR(m1, 12) - md5.FF(q1, Q[Qoff + 0], Q[Qoff - 1]) - tt1
            m1 = lowlevel.sub(
                lowlevel.sub(md5.RR(m1, 12), md5.FF(q1, Q[Qoff + 0], Q[Qoff - 1])),
                tt1)

            q16 = Q[Qoff + 16]
            q17 = lowlevel.trunc(tt17 + m1)
            q17 = lowlevel.trunc(md5.RL(q17, 5) + q16)
            if 0x80000000 != ((q17 ^ q16) & 0x80008008): continue
            if 0 != (q17 & 0x00020000): continue

            q18 = lowlevel.trunc(md5.GG(q17, q16, Q[Qoff + 15]) + tt18)
            q18 = md5.RL(q18, 9)
            q18 = lowlevel.trunc(q18 + q17)
            if 0x80020000 != ((q18 ^ q17) & 0xa0020000): continue

            q19 = lowlevel.trunc(md5.GG(q18, q17, q16) + tt19)
            q19 = md5.RL(q19, 14)
            q19 = lowlevel.trunc(q19 + q18)
            if 0x80000000 != (q19 & 0x80020000): continue

            m0 = lowlevel.sub(q1, Q[Qoff + 0])
            m0 = lowlevel.sub(md5.RR(m0, 7), tt0)

            q20 = lowlevel.trunc(md5.GG(q19, q18, q17) + q16 + 0xe9b6c7aa + m0)
            q20 = md5.RL(q20, 20)
            q20 = lowlevel.trunc(q20 + q19)
            if 0x00040000 != ((q20 ^ q19) & 0x80040000): continue

            Q[Qoff + 1] = q1
            Q[Qoff + 17] = q17
            Q[Qoff + 18] = q18
            Q[Qoff + 19] = q19
            Q[Qoff + 20] = q20

            block[0] = m0
            block[1] = m1

            block = md5.MD5_REVERSE_STEP(5, 0x4787c62a, 12, block, Q, Qoff)
            q21 = lowlevel.trunc(
                md5.GG(Q[Qoff + 20], Q[Qoff + 19], Q[Qoff + 18]) + Q[Qoff + 17] + 0xd62f105d + block[5])
            q21 = md5.RL(q21, 5)
            q21 = lowlevel.trunc(q21 + Q[Qoff + 20])
            if 0 != ((q21 ^ Q[Qoff + 20]) & 0x80020000): continue
            Q[Qoff + 21] = q21

            counter = 0
            break

        if counter != 0:
            continue

        q9b = Q[Qoff + 9]
        q10b = Q[Qoff + 10]

        block = md5.MD5_REVERSE_STEP(2, 0x242070db, 17, block, Q, Qoff)
        block = md5.MD5_REVERSE_STEP(3, 0xc1bdceee, 22, block, Q, Qoff)
        block = md5.MD5_REVERSE_STEP(4, 0xf57c0faf, 7, block, Q, Qoff)
        block = md5.MD5_REVERSE_STEP(7, 0xfd469501, 22, block, Q, Qoff)

        tt10 = lowlevel.trunc(Q[Qoff + 7] + 0xffff5bb1)
        tt22 = lowlevel.trunc(md5.GG(Q[Qoff + 21], Q[Qoff + 20], Q[Qoff + 19]) + Q[Qoff + 18] + 0x02441453)
        tt23 = lowlevel.trunc(Q[Qoff + 19] + 0xd8a1e681 + block[15])
        tt24 = lowlevel.trunc(Q[Qoff + 20] + 0xe7d3fbc8 + block[4])

        for k10 in range(1 << 3):
            q10 = q10b | (q9q10mask[k10] & 0x08000020)
            m10 = md5.RR(lowlevel.sub(Q[Qoff + 11], q10), 17)
            q9 = q9b | (q9q10mask[k10] & 0x00002000)

            m10 = lowlevel.sub(m10, lowlevel.trunc(md5.FF(q10, q9, Q[Qoff + 8]) + tt10))

            aa = Q[Qoff + 21]
            dd = lowlevel.trunc(tt22 + m10)
            dd = lowlevel.trunc(md5.RL(dd, 9) + aa)
            if 0 == (dd & 0x80000000): continue

            bb = Q[Qoff + 20]
            cc = lowlevel.trunc(tt23 + md5.GG(dd, aa, bb))
            if 0 != (cc & 0x20000): continue
            cc = lowlevel.trunc(md5.RL(cc, 14) + dd)
            if 0 != (cc & 0x80000000): continue

            bb = lowlevel.trunc(tt24 + md5.GG(cc, dd, aa))
            bb = lowlevel.trunc(md5.RL(bb, 20) + cc)
            if 0 == (bb & 0x80000000): continue

            block[10] = m10
            Q[Qoff + 9] = q9
            Q[Qoff + 10] = q10
            block = md5.MD5_REVERSE_STEP(13, 0xfd987193, 12, block, Q, Qoff)

            for k9 in range(1 << 9):
                a = aa
                b = bb
                c = cc
                d = dd
                Q[Qoff + 9] = q9 ^ q9mask[k9]
                block = md5.MD5_REVERSE_STEP(8, 0x698098d8, 7, block, Q, Qoff)
                block = md5.MD5_REVERSE_STEP(9, 0x8b44f7af, 12, block, Q, Qoff)
                block = md5.MD5_REVERSE_STEP(12, 0x6b901122, 7, block, Q, Qoff)

                a = md5.MD5_STEP(md5.GG, a, b, c, d, block[9], 0x21e1cde6, 5)
                d = md5.MD5_STEP(md5.GG, d, a, b, c, block[14], 0xc33707d6, 9)
                c = md5.MD5_STEP(md5.GG, c, d, a, b, block[3], 0xf4d50d87, 14)
                b = md5.MD5_STEP(md5.GG, b, c, d, a, block[8], 0x455a14ed, 20)
                a = md5.MD5_STEP(md5.GG, a, b, c, d, block[13], 0xa9e3e905, 5)
                d = md5.MD5_STEP(md5.GG, d, a, b, c, block[2], 0xfcefa3f8, 9)
                c = md5.MD5_STEP(md5.GG, c, d, a, b, block[7], 0x676f02d9, 14)
                b = md5.MD5_STEP(md5.GG, b, c, d, a, block[12], 0x8d2a4c8a, 20)
                a = md5.MD5_STEP(md5.HH, a, b, c, d, block[5], 0xfffa3942, 4)
                d = md5.MD5_STEP(md5.HH, d, a, b, c, block[8], 0x8771f681, 11)

                c = lowlevel.trunc(c + md5.HH(d, a, b) + block[11] + 0x6d9d6122)
                if 0 != (c & (1 << 15)):
                    continue
                c = lowlevel.trunc((lowlevel.trunc(c << 16) | c >> 16) + d)

                b = md5.MD5_STEP(md5.HH, b, c, d, a, block[14], 0xfde5380c, 23)
                a = md5.MD5_STEP(md5.HH, a, b, c, d, block[1], 0xa4beea44, 4)
                d = md5.MD5_STEP(md5.HH, d, a, b, c, block[4], 0x4bdecfa9, 11)
                c = md5.MD5_STEP(md5.HH, c, d, a, b, block[7], 0xf6bb4b60, 16)
                b = md5.MD5_STEP(md5.HH, b, c, d, a, block[10], 0xbebfbc70, 23)
                a = md5.MD5_STEP(md5.HH, a, b, c, d, block[13], 0x289b7ec6, 4)
                d = md5.MD5_STEP(md5.HH, d, a, b, c, block[0], 0xeaa127fa, 11)
                c = md5.MD5_STEP(md5.HH, c, d, a, b, block[3], 0xd4ef3085, 16)
                b = md5.MD5_STEP(md5.HH, b, c, d, a, block[6], 0x04881d05, 23)
                a = md5.MD5_STEP(md5.HH, a, b, c, d, block[9], 0xd9d4d039, 4)
                d = md5.MD5_STEP(md5.HH, d, a, b, c, block[12], 0xe6db99e5, 11)
                c = md5.MD5_STEP(md5.HH, c, d, a, b, block[15], 0x1fa27cf8, 16)
                b = md5.MD5_STEP(md5.HH, b, c, d, a, block[2], 0xc4ac5665, 23)
                if 0 != ((b ^ d) & 0x80000000):
                    continue

                a = md5.MD5_STEP(md5.II, a, b, c, d, block[0], 0xf4292244, 6)
                if 0 != ((a ^ c) >> 31): continue
                a = md5.MD5_STEP(md5.II, d, a, b, c, block[7], 0x432aff97, 10)
                if 0 == ((b ^ d) >> 31): continue
                a = md5.MD5_STEP(md5.II, c, d, a, b, block[14], 0xab9423a7, 15)
                if 0 != ((a ^ c) >> 31): continue
                a = md5.MD5_STEP(md5.II, b, c, d, a, block[5], 0xfc93a039, 21)
                if 0 != ((b ^ d) >> 31): continue
                a = md5.MD5_STEP(md5.II, a, b, c, d, block[12], 0x655b59c3, 6)
                if 0 != ((a ^ c) >> 31): continue
                a = md5.MD5_STEP(md5.II, d, a, b, c, block[3], 0x8f0ccc92, 10)
                if 0 != ((b ^ d) >> 31): continue
                a = md5.MD5_STEP(md5.II, c, d, a, b, block[10], 0xffeff47d, 15)
                if 0 != ((a ^ c) >> 31): continue
                a = md5.MD5_STEP(md5.II, b, c, d, a, block[1], 0x85845dd1, 21)
                if 0 != ((b ^ d) >> 31): continue
                a = md5.MD5_STEP(md5.II, a, b, c, d, block[8], 0x6fa87e4f, 6)
                if 0 != ((a ^ c) >> 31): continue
                a = md5.MD5_STEP(md5.II, d, a, b, c, block[15], 0xfe2ce6e0, 10)
                if 0 != ((b ^ d) >> 31): continue
                a = md5.MD5_STEP(md5.II, c, d, a, b, block[6], 0xa3014314, 15)
                if 0 != ((a ^ c) >> 31): continue
                a = md5.MD5_STEP(md5.II, b, c, d, a, block[13], 0x4e0811a1, 21)
                if 0 == ((b ^ d) >> 31): continue
                a = md5.MD5_STEP(md5.II, a, b, c, d, block[4], 0xf7537e82, 6)
                if 0 != ((a ^ c) >> 31): continue
                a = md5.MD5_STEP(md5.II, d, a, b, c, block[11], 0xbd3af235, 10)
                if 0 != ((b ^ d) >> 31): continue
                a = md5.MD5_STEP(md5.II, c, d, a, b, block[2], 0x2ad7d2bb, 15)
                if 0 != ((a ^ c) >> 31): continue
                a = md5.MD5_STEP(md5.II, b, c, d, a, block[9], 0xeb86d391, 21)

                print(".")

                block2 = [0] * 16
                IV1 = [0] * 4
                IV2 = [0] * 4
                for t in range(4):
                    IV1[t] = IV[t]
                    IV2[t] = lowlevel.trunc(IV[t] + (1 << 31))

                IV2[1] = lowlevel.sub(IV2[1], (1 << 25))
                IV2[2] = lowlevel.sub(IV2[2], (1 << 25))
                IV2[3] = lowlevel.sub(IV2[3], (1 << 25))

                for t in range(16):
                    block2[t] = block[t]
                block2[4] = lowlevel.trunc(block2[4] + (1 << 31))
                block2[11] = lowlevel.trunc(block2[11] + (1 << 15))
                block2[14] = lowlevel.trunc(block2[14] + (1 << 31))

                IV1 = md5.md5_compress(IV1, block)
                IV2 = md5.md5_compress(IV2, block2)
                if IV2[0] == IV1[0] and IV2[1] == IV1[1] and IV2[2] == IV1[2] and IV2[3] == IV1[3]:
                    return block
                if IV2[0] != IV1[0]:
                    print("!")
