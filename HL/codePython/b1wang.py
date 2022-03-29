import lowlevel
import md5


def find_block1_wang(IV):
    block = 16 * [0]
    Qoff = 3

    Q = [0] * 68
    Q[0] = IV[0]
    Q[1] = IV[3]
    Q[2] = IV[2]
    Q[3] = IV[1]

    q4mask = []
    q4masksize = (1 << 6)
    for k in range(q4masksize):
        new = ((k << 13) ^ (k << 19)) & 0x01c0e000
        q4mask.append(new)

    q9mask = []
    q10mask = []
    q9masksize = (1 << 5)
    for k in range(q9masksize):
        new = (k << 5) ^ (k << 13) ^ (k << 17) ^ (k << 24)
        q9mask.append(new & 0x00084000)
        q10mask.append(new & 0x18000020)

    q9mask2 = []
    q9mask2size = (1 << 10)
    for k in range(q9mask2size):
        new = ((k << 1) ^ (k << 7) ^ (k << 14) ^ (k << 15) ^ (k << 22)) & 0x6074041c
        q9mask2.append(new)

    while True:
        aa = Q[Qoff] & 0x80000000
        bb = 0x80000000 ^ aa

        Q[Qoff + 2] = (lowlevel.xrng64() & 0x71de7799) | 0x0c008840 | bb
        Q[Qoff + 3] = (lowlevel.xrng64() & 0x01c06601) | 0x3e1f0966 | (Q[Qoff + 2] & 0x80000018)
        Q[Qoff + 4] = 0x3a040010 | (Q[Qoff + 3] & 0x80000601)
        Q[Qoff + 5] = (lowlevel.xrng64() & 0x03c0e000) | 0x482f0e50 | aa
        Q[Qoff + 6] = (lowlevel.xrng64() & 0x600c0000) | 0x05e2ec56 | aa
        Q[Qoff + 7] = (lowlevel.xrng64() & 0x604c203e) | 0x16819e01 | bb | (Q[Qoff + 6] & 0x01000000)
        Q[Qoff + 8] = (lowlevel.xrng64() & 0x604c7c1c) | 0x043283e0 | (Q[Qoff + 7] & 0x80000002)
        Q[Qoff + 9] = (lowlevel.xrng64() & 0x00002800) | 0x1c0101c1 | (Q[Qoff + 8] & 0x80001000)
        Q[Qoff + 10] = 0x078bcbc0 | bb
        Q[Qoff + 11] = (lowlevel.xrng64() & 0x07800000) | 0x607dc7df | bb
        Q[Qoff + 12] = (lowlevel.xrng64() & 0x00f00f7f) | 0x00081080 | (Q[Qoff + 11] & 0xe7000000)
        Q[Qoff + 13] = (lowlevel.xrng64() & 0x00701f77) | 0x3f0fe008 | aa
        Q[Qoff + 14] = (lowlevel.xrng64() & 0x00701f77) | 0x408be088 | aa
        Q[Qoff + 15] = (lowlevel.xrng64() & 0x00ff3ff7) | 0x7d000000
        Q[Qoff + 16] = (lowlevel.xrng64() & 0x4ffdffff) | 0x20000000 | (~Q[Qoff + 15] & 0x00020000)

        md5.MD5_REVERSE_STEP(5, 0x4787c62a, 12, block, Q, Qoff)
        md5.MD5_REVERSE_STEP(6, 0xa8304613, 17, block, Q, Qoff)
        md5.MD5_REVERSE_STEP(7, 0xfd469501, 22, block, Q, Qoff)
        md5.MD5_REVERSE_STEP(11, 0x895cd7be, 22, block, Q, Qoff)
        md5.MD5_REVERSE_STEP(14, 0xa679438e, 17, block, Q, Qoff)
        md5.MD5_REVERSE_STEP(15, 0x49b40821, 22, block, Q, Qoff)

        tt17 = lowlevel.trunc(md5.GG(Q[Qoff + 16], Q[Qoff + 15], Q[Qoff + 14]) + Q[Qoff + 13] + 0xf61e2562)
        tt18 = lowlevel.trunc(Q[Qoff + 14] + 0xc040b340 + block[6])
        tt19 = lowlevel.trunc(Q[Qoff + 15] + 0x265e5a51 + block[11])

        tt0 = lowlevel.trunc(md5.FF(Q[Qoff + 0], Q[Qoff - 1], Q[Qoff - 2]) + Q[Qoff - 3] + 0xd76aa478)
        tt1 = lowlevel.trunc(Q[Qoff - 2] + 0xe8c7b756)

        q1a = 0x04200040 | (Q[Qoff + 2] & 0xf01e1080)

        counter = 0
        while counter < (1 << 12):
            counter += 1

            q1 = q1a | (lowlevel.xrng64() & 0x01c0e71f)
            m1 = lowlevel.trunc(Q[Qoff + 2] - q1)
            m1 = lowlevel.trunc(md5.RR(m1, 12) - md5.FF(q1, Q[Qoff + 0], Q[Qoff - 1]) - tt1)

            q16 = Q[Qoff + 16]
            q17 = lowlevel.trunc(tt17 + m1)
            q17 = lowlevel.trunc(md5.RL(q17, 5) + q16)
            if 0x40000000 != ((q17 ^ q16) & 0xc0008008): continue
            if 0 != (q17 & 0x00020000): continue

            q18 = lowlevel.trunc(md5.GG(q17, q16, Q[Qoff + 15]) + tt18)
            q18 = md5.RL(q18, 9)
            q18 = lowlevel.trunc(q18 + q17)
            if 0x00020000 != ((q18 ^ q17) & 0xa0020000): continue

            q19 = lowlevel.trunc(md5.GG(q18, q17, q16) + tt19)
            q19 = md5.RL(q19, 14)
            q19 = lowlevel.trunc(q19 + q18)
            if 0 != (q19 & 0x80020000): continue

            m0 = lowlevel.trunc(q1 - Q[Qoff + 0])
            m0 = lowlevel.trunc(md5.RR(m0, 7) - tt0)

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
            md5.MD5_REVERSE_STEP(2, 0x242070db, 17, block, Q, Qoff)

            counter = 0
            break
        if counter != 0:
            continue

        q4b = Q[Qoff + 4]
        q9b = Q[Qoff + 9]
        q10b = Q[Qoff + 10]
        tt21 = lowlevel.trunc(md5.GG(Q[Qoff + 20], Q[Qoff + 19], Q[Qoff + 18]) + Q[Qoff + 17] + 0xd62f105d)

        counter = 0
        while counter < (1 << 6):
            Q[Qoff + 4] = q4b ^ q4mask[counter]
            counter += 1
            md5.MD5_REVERSE_STEP(5, 0x4787c62a, 12, block, Q, Qoff)
            q21 = lowlevel.trunc(tt21 + block[5])
            q21 = md5.RL(q21, 5)
            q21 = lowlevel.trunc(q21 + Q[Qoff + 20])
            if 0 != ((q21 ^ Q[Qoff + 20]) & 0x80020000): continue

            Q[Qoff + 21] = q21
            md5.MD5_REVERSE_STEP(3, 0xc1bdceee, 22, block, Q, Qoff)
            md5.MD5_REVERSE_STEP(4, 0xf57c0faf, 7, block, Q, Qoff)
            md5.MD5_REVERSE_STEP(7, 0xfd469501, 22, block, Q, Qoff)

            tt10 = lowlevel.trunc(Q[Qoff + 7] + 0xffff5bb1)
            tt22 = lowlevel.trunc(md5.GG(Q[Qoff + 21], Q[Qoff + 20], Q[Qoff + 19]) + Q[Qoff + 18] + 0x02441453)
            tt23 = lowlevel.trunc(Q[Qoff + 19] + 0xd8a1e681 + block[15])
            tt24 = lowlevel.trunc(Q[Qoff + 20] + 0xe7d3fbc8 + block[4])

            counter2 = 0
            while counter2 < (1 << 5):
                q10 = q10b ^ q10mask[counter2]
                m10 = md5.RR(lowlevel.trunc(Q[Qoff + 11] - q10), 17)
                q9 = q9b ^ q9mask[counter2]
                counter2 += 1

                m10 = lowlevel.trunc(m10 - (md5.FF(q10, q9, Q[Qoff + 8]) + tt10))

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
                if 0 == (bb & 0x80000000): continue

                block[10] = m10
                Q[Qoff + 9] = q9
                Q[Qoff + 10] = q10
                md5.MD5_REVERSE_STEP(13, 0xfd987193, 12, block, Q, Qoff)

                for k9 in range(1 << 10):
                    a = aa
                    b = bb
                    c = cc
                    d = dd
                    Q[Qoff + 9] = q9 ^ q9mask2[k9]
                    k9 += 1
                    md5.MD5_REVERSE_STEP(8, 0x698098d8, 7, block, Q, Qoff)
                    md5.MD5_REVERSE_STEP(9, 0x8b44f7af, 12, block, Q, Qoff)
                    md5.MD5_REVERSE_STEP(12, 0x6b901122, 7, block, Q, Qoff)

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

                    if 0 == (c & (1 << 15)):
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

                    IV2[1] = lowlevel.trunc(IV2[1] + (1 << 25))
                    IV2[2] = lowlevel.trunc(IV2[2] + (1 << 25))
                    IV2[3] = lowlevel.trunc(IV2[3] + (1 << 25))

                    for t in range(16):
                        block2[t] = block[t]
                    block2[4] = lowlevel.trunc(block2[4] + (1 << 31))
                    block2[11] = lowlevel.trunc(block2[11] - (1 << 15))
                    block2[14] = lowlevel.trunc(block2[14] + (1 << 31))

                    IV1 = md5.md5_compress(IV1, block)
                    IV2 = md5.md5_compress(IV2, block2)
                    if IV2[0] == IV1[0] and IV2[1] == IV1[1] and IV2[2] == IV1[2] and IV2[3] == IV1[3]:
                        return block

                    if IV2[0] != IV1[0]:
                        print("!")
