import ntpath
import olefile
import os
import re
import sys


class Bupectomy(object):

    def __init__(self):
        self.details = None
        self.file_0 = None
        self.orig_filename = None

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

    def parsedetails(self, detailsfile):

        # Not done
        # More to come here

        for item in self.details.splitlines():
            if "OriginalName" in item:
                self.orig_filename = ntpath.basename(item)


    def writefiles(self, buf, dirname, filename):

        details = os.path.join(dirname, filename)

        try:
            with open(os.path.join(dirname, filename), "w") as f:
                f.write(buf)
        except Exception, e:
            sys.exit(e)


if __name__ == "__main__":
    
    from argparse import ArgumentParser
    
    p = ArgumentParser()
    p.add_argument("bup", help="McAfee .bup file")
    p.add_argument("-d", "--details", help="Print detection details", action="store_true")
    p.add_argument("-o", "--output", help="Specify an output directory for the decoded files")
    args = p.parse_args()

    if args.bup:
        b = Bupectomy()
        b.filecheck(args.bup)
        b.extractfiles(args.bup)
        b.details = b.single_byte_xor(b.details)
        b.parsedetails(b.details)
        b.file_0 = b.single_byte_xor(b.file_0)
    else:
        sys.exit("[-] .bup file not specified")

    if args.details:
        print b.details

    elif args.output:
        b.writefiles(b.details, args.output, "details.txt")
        b.writefiles(b.file_0, args.output, b.orig_filename)

    else:
        with open("details.txt", "w") as f:
            f.write(b.details)
        with open(b.orig_filename, "w") as f:
            f.write(b.file_0)

else:
    pass









