import lowlevel
import md5


def find_block1_stevens_10(IV):
    print("S10")
    block = 16 * [0]
    Qoff = 3

    Q = [0] * 68
    Q[0] = IV[0]
    Q[1] = IV[3]
    Q[2] = IV[2]
    Q[3] = IV[1]

    q9q10mask = []
    q9q10size = (1 << 4)
    for k in range(q9q10size):
        new = ((k << 2) ^ (k << 8) ^ (k << 11) ^ (k << 25)) & 0x08004204
        q9q10mask.append(new)

    q9mask = []
    q9size = (1 << 10)
    for k in range(q9size):
        new = ((k << 1) ^ (k << 2) ^ (k << 3) ^ (k << 7) ^ (k << 12) ^ (k << 15) ^ (k << 18) ^ (
                k << 20)) & 0x2471042a
        q9mask.append(new)

    while True:
        aa = Q[Qoff] & 0x80000000

        Q[Qoff + 2] = (lowlevel.xrng64() & 0x79b0c6ba) | 0x024c3841 | aa
        Q[Qoff + 3] = (lowlevel.xrng64() & 0x19300210) | 0x2603096d | (Q[Qoff + 2] & 0x80000082)
        Q[Qoff + 4] = (lowlevel.xrng64() & 0x10300000) | 0xe4cae30c | (Q[Qoff + 3] & 0x01000030)
        Q[Qoff + 5] = (lowlevel.xrng64() & 0x10000000) | 0x63494061 | (Q[Qoff + 4] & 0x00300000)
        Q[Qoff + 6] = 0x7deaff68
        Q[Qoff + 7] = (lowlevel.xrng64() & 0x20444000) | 0x09091ee0
        Q[Qoff + 8] = (lowlevel.xrng64() & 0x09040000) | 0xb2529f6d
        Q[Qoff + 9] = (lowlevel.xrng64() & 0x00040000) | 0x10885184
        Q[Qoff + 10] = (lowlevel.xrng64() & 0x00000080) | 0x428afb11 | (Q[Qoff + 9] & 0x00040000)
        Q[Qoff + 11] = (lowlevel.xrng64() & 0x128a8110) | 0x6571266b | (Q[Qoff + 10] & 0x0000080)
        Q[Qoff + 12] = (lowlevel.xrng64() & 0x3ef38d7f) | 0x00003080 | (~Q[Qoff + 11] & 0x00080000)
        Q[Qoff + 13] = (lowlevel.xrng64() & 0x3efb1d77) | 0x0004c008
        Q[Qoff + 14] = (lowlevel.xrng64() & 0x5fff5d77) | 0x8000a288
        Q[Qoff + 15] = (lowlevel.xrng64() & 0x1efe7ff7) | 0xe0008000 | (~Q[Qoff + 14] & 0x00010000)
        Q[Qoff + 16] = (lowlevel.xrng64() & 0x5ffdffff) | 0x20000000 | (~Q[Qoff + 15] & 0x00020000)

        # print(Q[Qoff + 2])
        # print(Q[Qoff + 3])
        # print(Q[Qoff + 4])
        # print(Q[Qoff + 5])
        # print(Q[Qoff + 6])
        # print(Q[Qoff + 7])
        # print(Q[Qoff + 8])
        # print(Q[Qoff + 9])
        # print(Q[Qoff + 10])
        # print(Q[Qoff + 11])
        # print(Q[Qoff + 12])
        # print(Q[Qoff + 13])
        # print(Q[Qoff + 14])
        # print(Q[Qoff + 15])
        # print(Q[Qoff + 16])
        # print()

        block = md5.MD5_REVERSE_STEP(5, 0x4787c62a, 12, block, Q, Qoff)
        block = md5.MD5_REVERSE_STEP(6, 0xa8304613, 17, block, Q, Qoff)
        block = md5.MD5_REVERSE_STEP(7, 0xfd469501, 22, block, Q, Qoff)
        block = md5.MD5_REVERSE_STEP(11, 0x895cd7be, 22, block, Q, Qoff)
        block = md5.MD5_REVERSE_STEP(14, 0xa679438e, 17, block, Q, Qoff)
        block = md5.MD5_REVERSE_STEP(15, 0x49b40821, 22, block, Q, Qoff)

        # print(block[15])

        tt17 = lowlevel.trunc(md5.GG(Q[Qoff + 16], Q[Qoff + 15], Q[Qoff + 14]) + Q[Qoff + 13] + 0xf61e2562)
        tt18 = lowlevel.trunc(Q[Qoff + 14] + 0xc040b340 + block[6])
        tt19 = lowlevel.trunc(Q[Qoff + 15] + 0x265e5a51 + block[11])

        tt0 = lowlevel.trunc(md5.FF(Q[Qoff + 0], Q[Qoff - 1], Q[Qoff - 2]) + Q[Qoff - 3] + 0xd76aa478)
        tt1 = lowlevel.trunc(Q[Qoff - 2] + 0xe8c7b756)

        q1a = 0x02000941 ^ (Q[Qoff + 0] & 0x80000000)

        counter = 0
        while counter < (1 << 12):
            counter += 1

            q1 = q1a | (lowlevel.xrng64() & 0x7dfdf6be)
            m1 = lowlevel.sub(Q[Qoff + 2], q1)
            m1 = lowlevel.sub(
                    lowlevel.sub(
                        md5.RR(m1, 12),
                        md5.FF(q1, Q[Qoff + 0], Q[Qoff - 1])
                    ),
                    tt1
            )

            q16 = Q[Qoff + 16]
            q17 = lowlevel.trunc(tt17 + m1)
            q17 = lowlevel.trunc(md5.RL(q17, 5) + q16)

            # print(q1a)
            # print(q1)
            # print()
            # print(m1)
            # print(q16)
            # print(q17)
            # return

            if 0x80000000 != ((q17 ^ q16) & 0x80008008): continue
            if 0 != (q17 & 0x00020000): continue

            # print(q1a)
            # print(q1)
            # print()
            # print(m1)
            # print(q16)
            # print(q17)
            # return

            q18 = lowlevel.trunc(md5.GG(q17, q16, Q[Qoff + 15]) + tt18)
            q18 = md5.RL(q18, 9)
            q18 = lowlevel.trunc(q18 + q17)
            if 0x80020000 != ((q18 ^ q17) & 0xa0020000): continue

            q19 = lowlevel.trunc(md5.GG(q18, q17, q16) + tt19)
            q19 = md5.RL(q19, 14)
            q19 = lowlevel.trunc(q19 + q18)
            if 0 != (q19 & 0x80020000): continue

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

            # print(q1a)
            # print(q1)
            # print(temp)
            # print()
            # print(Q[Qoff + 1])
            # print(Q[Qoff + 17])
            # print(Q[Qoff + 18])
            # print(Q[Qoff + 19])
            # print(Q[Qoff + 20])
            # print()
            # print(block[0])
            # print(block[1])
            # return

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

        for k10 in range(1 << 4):
            q10 = q10b | (q9q10mask[k10] & 0x08000004)
            m10 = md5.RR(lowlevel.sub(Q[Qoff + 11], q10), 17)
            q9 = q9b | (q9q10mask[k10] & 0x00004200)

            m10 = lowlevel.sub(m10, lowlevel.trunc(md5.FF(q10, q9, Q[Qoff + 8]) + tt10))

            aa = Q[Qoff + 21]
            dd = lowlevel.trunc(tt22 + m10)
            dd = lowlevel.trunc(md5.RL(dd, 9) + aa)
            if 0 != (dd & 0x80000000): continue

            bb = Q[Qoff + 20]
            cc = lowlevel.trunc(tt23 + md5.GG(dd, aa, bb))
            if 0 != (cc & 0x20000): continue
            cc = lowlevel.trunc(md5.RL(cc, 14) + dd)
            if 0 != (cc & 0x80000000): continue

            bb = lowlevel.trunc(tt24 + md5.GG(cc, dd, aa))
            bb = lowlevel.trunc(md5.RL(bb, 20) + cc)
            if 0 == (bb & 0x80000000): continue;

            block[10] = m10
            Q[Qoff + 9] = q9
            Q[Qoff + 10] = q10
            block = md5.MD5_REVERSE_STEP(13, 0xfd987193, 12, block, Q, Qoff)

            for k9 in range(1 << 10):
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
                if 0 != (c & (1 << 15)): continue
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
                d = md5.MD5_STEP(md5.II, d, a, b, c, block[7], 0x432aff97, 10)
                if 0 == ((b ^ d) >> 31): continue
                c = md5.MD5_STEP(md5.II, c, d, a, b, block[14], 0xab9423a7, 15)
                if 0 != ((a ^ c) >> 31): continue
                b = md5.MD5_STEP(md5.II, b, c, d, a, block[5], 0xfc93a039, 21)
                if 0 != ((b ^ d) >> 31): continue
                a = md5.MD5_STEP(md5.II, a, b, c, d, block[12], 0x655b59c3, 6)
                if 0 != ((a ^ c) >> 31): continue
                d = md5.MD5_STEP(md5.II, d, a, b, c, block[3], 0x8f0ccc92, 10)
                if 0 != ((b ^ d) >> 31): continue
                c = md5.MD5_STEP(md5.II, c, d, a, b, block[10], 0xffeff47d, 15)
                if 0 != ((a ^ c) >> 31): continue
                b = md5.MD5_STEP(md5.II, b, c, d, a, block[1], 0x85845dd1, 21)
                if 0 != ((b ^ d) >> 31): continue
                a = md5.MD5_STEP(md5.II, a, b, c, d, block[8], 0x6fa87e4f, 6)
                if 0 != ((a ^ c) >> 31): continue
                d = md5.MD5_STEP(md5.II, d, a, b, c, block[15], 0xfe2ce6e0, 10)
                if 0 != ((b ^ d) >> 31): continue
                c = md5.MD5_STEP(md5.II, c, d, a, b, block[6], 0xa3014314, 15)
                if 0 != ((a ^ c) >> 31): continue
                b = md5.MD5_STEP(md5.II, b, c, d, a, block[13], 0x4e0811a1, 21)
                if 0 == ((b ^ d) >> 31): continue
                a = md5.MD5_STEP(md5.II, a, b, c, d, block[4], 0xf7537e82, 6)
                if 0 != ((a ^ c) >> 31): continue
                d = md5.MD5_STEP(md5.II, d, a, b, c, block[11], 0xbd3af235, 10)
                if 0 != ((b ^ d) >> 31): continue
                c = md5.MD5_STEP(md5.II, c, d, a, b, block[2], 0x2ad7d2bb, 15)
                if 0 != ((a ^ c) >> 31): continue
                b = md5.MD5_STEP(md5.II, b, c, d, a, block[9], 0xeb86d391, 21)

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

# IV = [1569400239, 774297298, 1649500096, 436401821]
# find_block1_stevens_10(IV)
