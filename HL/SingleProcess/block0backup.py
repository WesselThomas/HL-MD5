import lowlevel
import md5
import time
import queue


def find_block0(IV):
    block = 16 * [0]
    Qoff = 3

    Q = [0] * 68
    Q[0] = IV[0]
    Q[1] = IV[3]
    Q[2] = IV[2]
    Q[3] = IV[1]

    q4mask = []
    q4size = (1 << 4)
    for k in range(q4size):
        new = ((k << 2) ^ (k << 26)) & 0x38000004
        q4mask.append(new)

    q9q10mask = []
    q9q10size = (1 << 3)
    for k in range(q9q10size):
        new = ((k << 13) ^ (k << 4)) & 0x2060
        q9q10mask.append(new)

    q9mask = []
    q9size = (1 << 16)
    for k in range(q9size):
        new = ((k << 1) ^ (k << 2) ^ (k << 5) ^ (k << 7) ^ (k << 8) ^ (k << 10)
               ^ (k << 11) ^ (k << 13)) & 0x0eb94f16
        q9mask.append(new)

    while True:
        Q[Qoff + 1] = lowlevel.xrng64()
        Q[Qoff + 3] = (lowlevel.xrng64() & 0xfe87bc3f) | 0x017841c0
        Q[Qoff + 4] = (lowlevel.xrng64() & 0x44000033) | 0x000002c0 | (Q[Qoff + 3] & 0x0287bc00)
        Q[Qoff + 5] = 0x41ffffc8 | (Q[Qoff + 4] & 0x04000033)
        Q[Qoff + 6] = 0xb84b82d6
        Q[Qoff + 7] = (lowlevel.xrng64() & 0x68000084) | 0x02401b43
        Q[Qoff + 8] = (lowlevel.xrng64() & 0x2b8f6e04) | 0x005090d3 | (~Q[Qoff + 7] & 0x40000000)
        Q[Qoff + 9] = 0x20040068 | (Q[Qoff + 8] & 0x00020000) | (~Q[Qoff + 8] & 0x40000000)
        Q[Qoff + 10] = (lowlevel.xrng64() & 0x40000000) | 0x1040b089
        Q[Qoff + 11] = (lowlevel.xrng64() & 0x10408008) | 0x0fbb7f16 | (~Q[Qoff + 10] & 0x40000000)
        Q[Qoff + 12] = (lowlevel.xrng64() & 0x1ed9df7f) | 0x00022080 | (~Q[Qoff + 11] & 0x40200000)
        Q[Qoff + 13] = (lowlevel.xrng64() & 0x5efb4f77) | 0x20049008
        Q[Qoff + 14] = (lowlevel.xrng64() & 0x1fff5f77) | 0x0000a088 | (~Q[Qoff + 13] & 0x40000000)
        Q[Qoff + 15] = (lowlevel.xrng64() & 0x5efe7ff7) | 0x80008000 | (~Q[Qoff + 14] & 0x00010000)
        Q[Qoff + 16] = (lowlevel.xrng64() & 0x1ffdffff) | 0xa0000000 | (~Q[Qoff + 15] & 0x40020000)

        md5.MD5_REVERSE_STEP(0, 0xd76aa478, 7, block, Q, Qoff)
        md5.MD5_REVERSE_STEP(6, 0xa8304613, 17, block, Q, Qoff)
        md5.MD5_REVERSE_STEP(7, 0xfd469501, 22, block, Q, Qoff)
        md5.MD5_REVERSE_STEP(11, 0x895cd7be, 22, block, Q, Qoff)
        md5.MD5_REVERSE_STEP(14, 0xa679438e, 17, block, Q, Qoff)
        md5.MD5_REVERSE_STEP(15, 0x49b40821, 22, block, Q, Qoff)

        tt1 = lowlevel.trunc(md5.FF(Q[Qoff + 1], Q[Qoff + 0], Q[Qoff - 1]) + Q[Qoff - 2] + 0xe8c7b756)
        tt17 = lowlevel.trunc(md5.GG(Q[Qoff + 16], Q[Qoff + 15], Q[Qoff + 14]) + Q[Qoff + 13] + 0xf61e2562)
        tt18 = lowlevel.trunc(Q[Qoff + 14] + 0xc040b340 + block[6])
        tt19 = lowlevel.trunc(Q[Qoff + 15] + 0x265e5a51 + block[11])
        tt20 = lowlevel.trunc(Q[Qoff + 16] + 0xe9b6c7aa + block[0])
        tt5 = lowlevel.trunc(md5.RR(lowlevel.trunc(Q[Qoff + 6] - Q[Qoff + 5]), 12) - md5.FF(Q[Qoff + 5], Q[Qoff + 4], Q[Qoff + 3]) - 0x4787c62a)

        # change q17 until conditions are met on q18, q19 and q20
        counter = 0
        while counter < (1 << 7):
            q16 = Q[Qoff + 16]
            q17 = ((lowlevel.xrng64() & 0x3ffd7ff7) | (q16 & 0xc0008008)) ^ 0x40000000
            counter += 1

            q18 = lowlevel.trunc(md5.GG(q17, q16, Q[Qoff + 15]) + tt18)
            q18 = md5.RL(q18, 9)
            q18 = lowlevel.trunc(q18 + q17)

            if 0x00020000 != ((q18 ^ q17) & 0xa0020000): continue

            q19 = lowlevel.trunc(md5.GG(q18, q17, q16) + tt19)
            q19 = md5.RL(q19, 14)
            q19 = lowlevel.trunc(q19 + q18)
            if 0x80000000 != (q19 & 0x80020000): continue

            q20 = lowlevel.trunc(md5.GG(q19, q18, q17) + tt20)
            q20 = md5.RL(q20, 20)
            q20 = lowlevel.trunc(q20 + q19)
            if 0x00040000 != ((q20 ^ q19) & 0x80040000): continue

            block[1] = lowlevel.trunc(q17 - q16)
            block[1] = md5.RR(block[1], 5)
            block[1] = lowlevel.trunc(block[1] - tt17)
            q2 = lowlevel.trunc(block[1] + tt1)
            q2 = md5.RL(q2, 12)
            q2 = lowlevel.trunc(q2 + Q[Qoff + 1])
            block[5] = lowlevel.trunc(tt5 - q2)

            Q[Qoff + 2] = q2
            Q[Qoff + 17] = q17
            Q[Qoff + 18] = q18
            Q[Qoff + 19] = q19
            Q[Qoff + 20] = q20

            md5.MD5_REVERSE_STEP(2, 0x242070db, 17, block, Q, Qoff)

            counter = 0
            break

        if counter != 0: continue

        q4 = Q[Qoff + 4]
        q9backup = Q[Qoff + 9]
        tt21 = lowlevel.trunc(md5.GG(Q[Qoff + 20], Q[Qoff + 19], Q[Qoff + 18]) + Q[Qoff + 17] + 0xd62f105d)

        # iterate over possible changes of q4
        # while keeping all conditions on q1-q20 intact
        # this changes m3, m4, m5 and m7
        counter2 = 0
        while counter2 < (1 << 4):
            Q[Qoff + 4] = q4 ^ q4mask[counter2]
            counter2 += 1
            md5.MD5_REVERSE_STEP(5, 0x4787c62a, 12, block, Q, Qoff)
            q21 = lowlevel.trunc(tt21 + block[5])
            q21 = md5.RL(q21, 5)
            q21 = lowlevel.trunc(q21 + Q[Qoff + 20])
            if 0 != ((q21 ^ Q[Qoff + 20]) & 0x80020000): continue

            Q[Qoff + 21] = q21
            md5.MD5_REVERSE_STEP(3, 0xc1bdceee, 22, block, Q, Qoff)
            md5.MD5_REVERSE_STEP(4, 0xf57c0faf, 7, block, Q, Qoff)
            md5.MD5_REVERSE_STEP(7, 0xfd469501, 22, block, Q, Qoff)

            tt22 = lowlevel.trunc(md5.GG(Q[Qoff + 21], Q[Qoff + 20], Q[Qoff + 19]) + Q[Qoff + 18] + 0x02441453)
            tt23 = lowlevel.trunc(Q[Qoff + 19] + 0xd8a1e681 + block[15])
            tt24 = lowlevel.trunc(Q[Qoff + 20] + 0xe7d3fbc8 + block[4])

            tt9 = lowlevel.trunc(Q[Qoff + 6] + 0x8b44f7af)
            tt10 = lowlevel.trunc(Q[Qoff + 7] + 0xffff5bb1)
            tt8 = lowlevel.trunc(md5.FF(Q[Qoff + 8], Q[Qoff + 7], Q[Qoff + 6]) + Q[Qoff + 5] + 0x698098d8)
            tt12 = lowlevel.trunc(md5.RR(lowlevel.trunc(Q[Qoff + 13] - Q[Qoff + 12]), 7) - 0x6b901122)
            tt13 = lowlevel.trunc(
                    md5.RR(lowlevel.trunc(Q[Qoff + 14] - Q[Qoff + 13]), 12) -
                    md5.FF(Q[Qoff + 13], Q[Qoff + 12], Q[Qoff + 11]) - 0xfd987193)

            # iterate over possible changes of q9 and q10
            # while keeping conditions on q1-q21 intact
            # this changes m8, m9, m10, m12 and m13 (and not m11!)
            # the possible changes of q9 that also do not change m10 are used below
            counter3 = 0
            while counter3 < lowlevel.trunc(1 << 3):
                q10 = Q[Qoff + 10] ^ (q9q10mask[counter3] & 0x60)
                Q[Qoff + 9] = q9backup ^ (q9q10mask[counter3] & 0x2000)
                counter3 += 1
                m10 = md5.RR(lowlevel.trunc(Q[Qoff + 11] - q10), 17)
                m10 = lowlevel.trunc(m10 - (md5.FF(q10, Q[Qoff + 9], Q[Qoff + 8]) + tt10))

                aa = Q[Qoff + 21]
                dd = lowlevel.trunc(tt22 + m10)
                dd = lowlevel.trunc(md5.RL(dd, 9) + aa)
                if 0x80000000 != (dd & 0x80000000): continue
                bb = Q[Qoff + 20]
                cc = lowlevel.trunc(tt23 + md5.GG(dd, aa, bb))
                if 0 != (cc & 0x20000): continue
                cc = lowlevel.trunc(md5.RL(cc, 14) + dd)
                if 0 != (cc & 0x80000000): continue
                bb = lowlevel.trunc(tt24 + md5.GG(cc, dd, aa))
                bb = lowlevel.trunc(md5.RL(bb, 20) + cc)
                if 0 == (bb & 0x80000000): continue

                block[10] = m10
                block[13] = lowlevel.trunc(tt13 - q10)

                # iterate over possible changes of q9
                # while keeping intact conditions on q1-q24
                # this changes m8, m9 and m12 (but not m10!)
                for counter4 in range(1 << 16):
                    q9 = Q[Qoff + 9] ^ q9mask[counter4]
                    block[12] = lowlevel.trunc(tt12 - md5.FF(Q[Qoff + 12], Q[Qoff + 11], q10) - q9)
                    m8 = lowlevel.trunc(q9 - Q[Qoff + 8])
                    block[8] = lowlevel.trunc(md5.RR(m8, 7) - tt8)
                    m9 = lowlevel.trunc(q10 - q9)
                    block[9] = lowlevel.trunc(md5.RR(m9, 12) - md5.FF(q9, Q[Qoff + 8], Q[Qoff + 7]) - tt9)

                    a = aa
                    b = bb
                    c = cc
                    d = dd
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

                    c = lowlevel.trunc(((c << 16) | lowlevel.trunc(c >> 16)) + d)

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

                    if 0 != ((b ^ d) & 0x80000000): continue

                    a = md5.MD5_STEP(md5.II, a, b, c, d, block[0], 0xf4292244, 6)
                    if 0 != (a ^ c) >> 31: continue
                    d = md5.MD5_STEP(md5.II, d, a, b, c, block[7], 0x432aff97, 10)
                    if 0 == (b ^ d) >> 31: continue
                    c = md5.MD5_STEP(md5.II, c, d, a, b, block[14], 0xab9423a7, 15)
                    if 0 != (a ^ c) >> 31: continue
                    b = md5.MD5_STEP(md5.II, b, c, d, a, block[5], 0xfc93a039, 21)
                    if 0 != (b ^ d) >> 31: continue
                    a = md5.MD5_STEP(md5.II, a, b, c, d, block[12], 0x655b59c3, 6)
                    if 0 != (a ^ c) >> 31: continue
                    d = md5.MD5_STEP(md5.II, d, a, b, c, block[3], 0x8f0ccc92, 10)
                    if 0 != (b ^ d) >> 31: continue
                    c = md5.MD5_STEP(md5.II, c, d, a, b, block[10], 0xffeff47d, 15)
                    if 0 != (a ^ c) >> 31: continue
                    b = md5.MD5_STEP(md5.II, b, c, d, a, block[1], 0x85845dd1, 21)
                    if 0 != (b ^ d) >> 31: continue
                    a = md5.MD5_STEP(md5.II, a, b, c, d, block[8], 0x6fa87e4f, 6)
                    if 0 != (a ^ c) >> 31: continue
                    d = md5.MD5_STEP(md5.II, d, a, b, c, block[15], 0xfe2ce6e0, 10)
                    if 0 != (b ^ d) >> 31: continue
                    c = md5.MD5_STEP(md5.II, c, d, a, b, block[6], 0xa3014314, 15)
                    if 0 != (a ^ c) >> 31: continue
                    b = md5.MD5_STEP(md5.II, b, c, d, a, block[13], 0x4e0811a1, 21)
                    if 0 == (b ^ d) >> 31: continue
                    a = md5.MD5_STEP(md5.II, a, b, c, d, block[4], 0xf7537e82, 6)
                    if 0 != (a ^ c) >> 31: continue
                    d = md5.MD5_STEP(md5.II, d, a, b, c, block[11], 0xbd3af235, 10)
                    if 0 != (b ^ d) >> 31: continue
                    c = md5.MD5_STEP(md5.II, c, d, a, b, block[2], 0x2ad7d2bb, 15)
                    if 0 != (a ^ c) >> 31: continue
                    b = md5.MD5_STEP(md5.II, b, c, d, a, block[9], 0xeb86d391, 21)

                    IHV1 = lowlevel.trunc(b + IV[1])
                    IHV2 = lowlevel.trunc(c + IV[2])
                    IHV3 = lowlevel.trunc(d + IV[3])

                    wang = True
                    if 0x02000000 != ((IHV2 ^ IHV1) & 0x86000000): wang = False
                    if 0 != ((IHV1 ^ IHV3) & 0x82000000): wang = False
                    if 0 != (IHV1 & 0x06000020): wang = False

                    stevens = True
                    if ((IHV1 ^ IHV2) >> 31) != 0 or ((IHV1 ^ IHV3) >> 31) != 0:
                        stevens = False
                    if ((IHV3 & (1 << 25)) != 0 or (IHV2 & (1 << 25)) != 0 or (
                            IHV1 & (1 << 25)) != 0
                            or ((IHV2 ^ IHV1) & 1) != 0):
                        stevens = False

                    if not (stevens or wang):
                        continue

                    print(".")

                    IV1 = [0] * 4
                    IV2 = [0] * 4
                    for t in range(4):
                        IV2[t] = IV[t]
                        IV1[t] = IV[t]

                    block2 = [0] * 16
                    for t in range(16):
                        block2[t] = block[t]

                    block2[4] = lowlevel.trunc(block2[4] + (1 << 31))
                    block2[11] = lowlevel.trunc(block2[11] + (1 << 15))
                    block2[14] = lowlevel.trunc(block2[14] + (1 << 31))

                    IV1 = md5.md5_compress(IV1, block)
                    IV2 = md5.md5_compress(IV2, block2)

                    if IV2[0] == lowlevel.trunc(IV1[0] + (1 << 31)) \
                            and IV2[1] == lowlevel.trunc(IV1[1] + (1 << 31) + (1 << 25)) \
                            and IV2[2] == lowlevel.trunc(IV1[2] + (1 << 31) + (1 << 25)) and \
                            IV2[3] == lowlevel.trunc(IV1[3] + (1 << 31) + (1 << 25)):
                        return block

                    if IV2[0] != lowlevel.trunc(IV1[0] + (1 << 31)):
                        print("!")
