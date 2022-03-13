#include <iostream>
using namespace std;
#include <fstream>
#include <time.h>
#include "main.hpp"

const uint32 MD5IV[] = { 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476 };

void find_collision(const uint32 IV[], uint32 msg1block0[], uint32 msg1block1[], uint32 msg2block0[], uint32 msg2block1[], bool verbose = false);

int main(int argc, char** argv)
{
    cout << "Hello World!";
    
    uint32 IV[4] = { MD5IV[0], MD5IV[1], MD5IV[2], MD5IV[3] };
    uint32 msg1block0[16];
    uint32 msg1block1[16];
    uint32 msg2block0[16];
    uint32 msg2block1[16];
    find_collision(IV, msg1block0, msg1block1, msg2block0, msg2block1, true);
}

void find_collision(const uint32 IV[], uint32 msg1block0[], uint32 msg1block1[], uint32 msg2block0[], uint32 msg2block1[], bool verbose)
{
	if (verbose)
		cout << "Generating first block: " << flush;
	find_block0(msg1block0, IV);
    cout << msg1block0 << flush;
	// uint32 IHV[4] = { IV[0], IV[1], IV[2], IV[3] };
	// md5_compress(IHV, msg1block0);

	// if (verbose)
	// 	cout << endl << "Generating second block: " << flush;
	// find_block1(msg1block1, IHV);

	// for (int t = 0; t < 16; ++t)
	// {
	// 	msg2block0[t] = msg1block0[t];
	// 	msg2block1[t] = msg1block1[t];
	// }
	// msg2block0[4] += 1 << 31; msg2block0[11] += 1 << 15; msg2block0[14] += 1 << 31;
	// msg2block1[4] += 1 << 31; msg2block1[11] -= 1 << 15; msg2block1[14] += 1 << 31;
	// if (verbose)
	// 	cout << endl;
}