import block0
import block1
import md5
import lowlevel
import sys
import time

def findCollision(IV):
    # IV = [4009666844, 4185421068, 320656731, 1175793337]

    # FOR ACTUAL RUN
    msg1block0 = block0.find_block0(IV)
    IHV = IV
    IHV = md5.md5_compress(IHV, msg1block0)
    msg1block1 = block1.find_block1(IHV)

    # HARDCODED FOR 10
    # msg1block0 = [4283288562, 656939853, 2106128531, 573736039, 1971245164, 3224215086, 2054686251, 3634841136,
    #               3421764953, 1238117710, 2478663659, 2011068342, 3314879358, 166074220, 1909976678, 3880091990]
    # IHV = [3716883887, 2888226514, 3763429312, 2550331037]
    # msg1block1 = [2341741213, 1654785416, 1272051245, 1543617655, 588263875, 3883016052, 1862321035, 3599261579,
                  # 880334291, 467469207, 986188088, 2835811299, 1421249962, 2805981121, 3435502818, 4214318262]

    # HARDCODED FOR 01
    # msg1block0 = [2013948231,1100188993,1150280251,3820876210,3326249745,3400395898,3527046745,3971200583,3218273462,574802764,483393163,368692219,741454220,1526520087,1889375045,3605100003]
    # IV = [4009666844, 4185421068, 320656731, 1175793337]
    # IHV = [921813089,281889063,404168029,1343466289]
    # msg1block1 = [1636006431,4146171485,2592053891,2209556185,2202599374,4078323237,3354270417,1876854508,3558753632,33066994,793601930,4005954808,1407879520,2342312471,832988010,958760270]

    # HARDCODED FOR W
    # msg1block0 = [1004478221,498660495,1073369603,3262149724,3425996254,2253043969,3510169079,159908712,3943695245,2190705354,993847371,3012710939,2714574053,88374297,1726245718,2364527097]
    # IV: [4009666844, 4185421068, 320656731, 1175793337]
    # IHV: [495396472, 546865752, 1243140724, 763317780]
    # msg1block1 = [4168519128,1045482030,880655466,387457486,925489744,1011254659,107441434,3999087569,2063458165,3858569142,1910069934,2674316425,86541523,2352206723,1497114445,2815041586]

    # HARDCODED FOR 00
    # IV: [4009666844, 4185421068, 320656731, 1175793337]
    # IHV: [645931391, 2041334452, 1891395636, 1006984622]
    # msg1block0 = [1587831170,2407663402,2050105544,1545459550,2022369407,1512403318,1447258638,3392574034,4121275873,2927478492,425133707,455426538,1824907455,4248609522,2303053960,2856196139]
    # msg1block1 = [780114698,154689933,2555505235,765639477,2511132524,1621130036,3304496077,2925093341,3130417973,327113500,2411554169,1685145198,398512303,2963696612,2354089451,1578689204]

    # HARDCODED FOR 11
    # IV: [4009666844, 4185421068, 320656731, 1175793337]
    # IHV: [2568592575, 3227331703, 4097730979, 4228964337]
    # msg1block0 = [1162291197,1712752916,1927984936,4288887403,2135265002,680411416,1182227021,136221931,247648504,821291344,80988655,1177156576,2656474741,457986861,1122267213,4042400599]
    # msg1block1 = [1439282729,1993958379,236539107,384933320,77971305,2073009966,1470080884,1097829711,1841352308,4286294900,955237340,4048520234,127427580,3036002804,1163835464,2795102405]

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


def loadprefix(filename):
    prefixblock = [0] * 16
    with open('prefix.txt', 'rb') as f1, open('prefix_msg1.txt', 'wb') as f2, open('prefix_msg2.txt', 'wb') as f3:
        for line in f1:
            line = bytes(filter(lambda x: x != 0XD, list(line)))
            for k in range(16):
                for c in range(4):
                    if k * 4 + c <= len(line) - 1:
                        prefixblock[k] += (line[k * 4 + c] << c * 8)

            f2.write(bytes(line))
            f2.write(bytes([0] * (64 - len(line))))
            f3.write(bytes(line))
            f3.write(bytes([0] * (64 - len(line))))
    return prefixblock


def main():
    fileName = "prefix.txt"
    MD5IV = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]

    prefixblock = loadprefix(fileName)
    IV = md5.md5_compress(MD5IV, prefixblock)

    m1b0, m1b1, m2b0, m2b1 = findCollision(IV)
    with open('prefix_msg1.txt', 'ab') as f2, open('prefix_msg2.txt', 'ab') as f3:
        write_to_file(m1b0, f2)
        write_to_file(m1b1, f2)
        write_to_file(m2b0, f3)
        write_to_file(m2b1, f3)


start_time = time.time()
main()
print("TOTAL TIME:")
print(time.time() - start_time)

