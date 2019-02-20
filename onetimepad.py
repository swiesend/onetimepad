import gc
import secrets
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

rand = secrets.SystemRandom()
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
    
    try:
        with open(args.input, "r") as in_file, \
             open(args.output, "w") as out_file:
            i = in_file.read()
            if args.mode == "encrypt":
                i = i.strip()
                key = gen_key(i)
                o = encrypt(i, key)
                o = base64.encodebytes(bytes(o, "utf-8")).decode("utf-8")
                k = base64.encodebytes(bytes(key, "utf-8")).decode("utf-8")
                with open(args.key, "w") as key_file:
                    key_file.write(k)
            else:
                with open(args.key, "r") as key_file:
                    k = key_file.read()
                i = base64.decodebytes(bytes(i, "utf-8")).decode("utf-8")
                key = base64.decodebytes(bytes(k, "utf-8")).decode("utf-8")
                o = decrypt(i, key)
            out_file.write(o)
    finally:
        gc.collect()

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
