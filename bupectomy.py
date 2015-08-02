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

        if olecheck == False:
            sys.exit("[-] Not a valid .bup file")

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
    p.add_argument("-d", "--details", help="Print detection details", action="store_true")
    args = p.parse_args()

    if args.bup:
        b = Bupectomy()
        filecheck = b.filecheck(args.bup)
    else:
        print "[-] .bup file not provided"

    if args.details:
        b.extractfiles(args.bup)
        details = b.single_byte_xor(b.details)
        print details

    else:
        pass
        #will write both files to the file system

else:
    pass









