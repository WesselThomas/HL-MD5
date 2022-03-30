import block0
import block1
import md5
import lowlevel
import time
import sys
import multiprocessing


def findallblocks(IV):

    # # FOR ACTUAL RUN
    # msg1block0 = block0.find_block0(IV, i)
    # print("Found first block!")
    # print(msg1block0)
    # IV = md5.md5_compress(IV, msg1block0)
    # msg1block1 = block1.find_block1(IV)
    # print("Found second block!")
    # print(msg1block0)

    q = multiprocessing.Queue()
    processes = [multiprocessing.Process(target=block0.find_block0, args=(IV, q, i)) for i in range(5)]
    for pr in processes:
        pr.daemon = True
        pr.start()
        time.sleep(1)

    print("Looking for first block...")
    msg1block0 = q.get()
    print(f"FOUND: {msg1block0}")
    for pr in processes:
        print("Terminating other block0 process!")
        pr.terminate()

    IV = md5.md5_compress(IV, msg1block0)

    processes = [multiprocessing.Process(target=block1.find_block1, args=(IV, q, i)) for i in range(5)]
    for pr in processes:
        pr.daemon = True
        pr.start()
        time.sleep(1)

    print("Looking for second block...")
    msg1block1 = q.get()
    print(f"FOUND: {msg1block1}")
    for pr in processes:
        print("Terminating other block1 process!")
        pr.terminate()

    msg2block0 = [0] * 16
    msg2block1 = [0] * 16
    for i in range(16):
        msg2block0[i] = msg1block0[i]
        msg2block1[i] = msg1block1[i]

    msg2block0[4] = (msg2block0[4] + (1 << 31)) & 0xFFFFFFFF
    msg2block0[11] = (msg2block0[11] + (1 << 15)) & 0xFFFFFFFF
    msg2block0[14] = (msg2block0[14] + (1 << 31)) & 0xFFFFFFFF
    msg2block1[4] = (msg2block1[4] + (1 << 31)) & 0xFFFFFFFF
    msg2block1[11] = (msg2block1[11], (1 << 15)) & 0xFFFFFFFF
    msg2block1[14] = (msg2block1[14] + (1 << 31)) & 0xFFFFFFFF

    print("FINISHED: Found 2 messages!")
    return msg1block0, msg1block1, msg2block0, msg2block1


def write_to_file(array, f):
    for num in array:
        b = num.to_bytes(4, 'little')
        f.write(b)


def loadprefix(filename):
    prefixblock = [0] * 16
    with open(filename, 'rb') as f1, open('prefix_msg1.txt', 'wb') as f2, open('prefix_msg2.txt', 'wb') as f3:
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


def createcollision():
    fileName = sys.argv[1]
    MD5IV = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]
    prefixblock = loadprefix(fileName)
    IV = md5.md5_compress(MD5IV, prefixblock)

    m1b0, m1b1, m2b0, m2b1 = findallblocks(IV)
    with open("prefix_msg1.txt", 'ab') as f2, open("prefix_msg2.txt", 'ab') as f3:
        write_to_file(m1b0, f2)
        write_to_file(m1b1, f2)
        write_to_file(m2b0, f3)
        write_to_file(m2b1, f3)
    print(f"Created collisions in prefix_msg1.txt and prefix_msg2.txt")

def main():
    tic = time.time()
    createcollision()
    toc = time.time()
    print(f"Functions called: {lowlevel.count}")
    print('Done in {:.4f} seconds'.format(toc-tic))

main()
