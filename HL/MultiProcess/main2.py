import block0
import block1
import md5
import time
import sys
import multiprocessing
from os import path


def findallblocks(IV):

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
    msg2block1[11] = (msg2block1[11] - (1 << 15)) & 0xFFFFFFFF
    msg2block1[14] = (msg2block1[14] + (1 << 31)) & 0xFFFFFFFF

    print("FINISHED: Found 2 messages!")
    return msg1block0, msg1block1, msg2block0, msg2block1


def write_to_file(array, f):
    for num in array:
        b = num.to_bytes(4, 'little')
        f.write(b)


def loadprefix(filename, i):
    prefixblock = [0] * 16
    with open(filename, 'rb') as f1, open(f"prefix_msg{i}_1.txt", 'wb') as f2, open(f"prefix_msg{i}_2.txt", 'wb') as f3:
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
    i = 0
    stop = False
    while not stop:
        if path.exists(f"prefix_msg{i}_1.txt") and path.exists(f"prefix_msg{i}_2.txt"):
            i += 1
            stop = True

    fileName = sys.argv[1]
    MD5IV = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]
    prefixblock = loadprefix(fileName, i)
    IV = md5.md5_compress(MD5IV, prefixblock)

    m1b0, m1b1, m2b0, m2b1 = findallblocks(IV)
    with open(f"prefix_msg{i}_1.txt", 'ab') as f2, open(f"prefix_msg{i}_2.txt", 'ab') as f3:
        write_to_file(m1b0, f2)
        write_to_file(m1b1, f2)
        write_to_file(m2b0, f3)
        write_to_file(m2b1, f3)
    print(f"Created collisions in prefix_msg{i}_1.txt and prefix_msg{i}_2.txt")

def main():
    start = time.time()
    createcollision()
    end = time.time()
    print('This collision took {:.4f} seconds'.format(end-start))
    with open("timelog.txt", 'a') as file:
        file.write(f"Collision {i}: {end-start} seconds\n")

main()

# 2677 seconds
