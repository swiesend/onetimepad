import random
import string
import base64
import argparse
from subprocess import call

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", type=str,
    choices=["encrypt", "decrypt"], required=True,
    help="mode (default: %(default)s)")
parser.add_argument("-i", "--input", type=str, required=True,
    help="input file")
parser.add_argument("-o", "--output", type=str, required=True,
    help="output file")
parser.add_argument("-k", "--key", default="key",  type=str,
    help="key file")
parser.add_argument("-s", "--shred", default="", type=str, 
    choices=["", "i","k","o","all"],
    help="shred files (default: %(default)s)")

rand = random.SystemRandom()
printable = string.digits + string.ascii_letters + string.punctuation

def shred(filename):
    call(["shred", "-n", "10", "-u", filename])

def gen_key(data):
    return "".join(rand.choice(printable) for _ in range(len(data)))

def encrypt(data, key):
    return "".join(chr(ord(i) ^ ord(j)) for (i, j) in zip(data, key))

def decrypt(data, key):
    return encrypt(data, key)

def main():
    args = parser.parse_args()    
    
    in_file = open(args.input, "r")
    out_file = open(args.output, "w")

    i = in_file.read()
    if args.mode == "encrypt":
        i = i.strip()
        key_file = open(args.key, "w")
        k = gen_key(i)
        key_file.write(k)
        o = encrypt(i, k)
        o = base64.encodebytes(bytes(o, "utf-8")).decode("utf-8")
    else:
        i = base64.decodebytes(bytes(i, "utf-8")).decode("utf-8")
        key_file = open(args.key, "r")
        k = key_file.readline().strip()
        o = decrypt(i, k)
    out_file.write(o)

    in_file.close()
    key_file.close()
    out_file.close()

    if "all" in args.shred:
        args.shred = "iok"
    if 'i' in args.shred:
        shred(args.input)
    if 'o' in args.shred:
        shred(args.output)
    if 'k' in args.shred:
        shred(args.key)

if __name__ == '__main__':
    main()
