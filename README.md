# HL-MD5
This project contains a recreation of the MD5 attack published by Marc Stevens in his paper 'Fast Collision Attack on MD5' (https://eprint.iacr.org/2006/104.pdf)
This version is implemented in Python and uses multiple processes to speed up the collision rate.

## How to run:
Go to folder HL/MultiProcess
Create a .txt file with your chosen prefix (e.g. prefix.txt)
Run 'python3 main.py prefix.txt'.
After running, it should have created two files "prefix_msgX_1" and "prefix_msgX_2".
Calculating the MD5 sum of those files yields the same values.
Congratulations, you just created a MD5 collision!
