#!/usr/bin/python

import olefile
import os
import sys


class Bupectomy(object):

    def __init__(self):
        self.details = None
        self.file_0 = None

    def filecheck(self, bup):
        file_exists = os.path.exists(bup)

        if file_exists:
            olecheck = olefile.isOleFile(bup)
        else:
            sys.exit("\n[-] File not found\n")

        if olecheck:
            return True
        else:
            return False

    def extractfiles(self, bup):
        ole = olefile.OleFileIO(bup)
        
        try:
            self.details = ole.openstream('Details').read()
            self.file_0 = ole.openstream('File_0').read()

        except Exception, e:
            print "[-] Unable to extract files from the bup"
            print e

    def single_byte_xor(self, buf):
        # taken from xortools.py

        key = ord('\x6a')
        out = ''
        for i in buf:
            out += chr(ord(i) ^ key)
        return out

    def writefiles(self, buf, filename):

        try:
            with open(filename, "w") as f:
                f.write(buf)
        except Exception, e:
            print e


if __name__ == "__main__":
    
    from argparse import ArgumentParser
    
    p = ArgumentParser()
    p.add_argument("bup", help="McAfee .bup file")
    args = p.parse_args()

    if args.bup:
        b = Bupectomy()
        filecheck = b.filecheck(sys.argv[1])

        if filecheck:
            b.extractfiles(sys.argv[1])
        else:
            sys.exit("[-] Not a valid OLE file")

        details = b.single_byte_xor(b.details)
        file_0 = b.single_byte_xor(b.file_0)

        print details
else:
    pass










