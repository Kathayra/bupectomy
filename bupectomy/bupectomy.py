#!/usr/bin/python

from argparse import ArgumentParser
import json
import ntpath
import os
import re
import requests
import sys
import olefile



class Bupectomy(object):

    def __init__(self):

        self.streams = {}
        self.details_dict = {}

    def extractfiles(self, bup):

        ole = olefile.OleFileIO(bup)

        for item in ole.listdir():
            if ole.get_size(item[0]):
                encoded_stream = ole.openstream(item[0]).read()
                self.streams[item[0]] = encoded_stream
            else:
                sys.exit("[ - ] Cannot extract {} stream: Corrupt bup?".format(item[0]))


    def single_byte_xor(self, buf):
        # taken from xortools.py

        for item in self.streams:
            key = ord('\x6a')
            out = ''
            for i in buf:
                out += chr(ord(i) ^ key)
            return out


    def details_to_json(self):

        current_header = None
        unencoded_details_file = self.single_byte_xor(self.streams["Details"])

        for line in unencoded_details_file.splitlines():
            parse_header = re.search("\[([a-zA-Z0-9_]{3,})\]", line)
            
            if parse_header:
                current_header = parse_header.group(1)
                self.details_dict[current_header] = {}

            if "=" in line:
                values = line.split("=")
                self.details_dict[current_header][values[0]] = values[1]

        self.details = json.dumps(self.details_dict, indent=4, sort_keys=True)


    def writefiles(self, outputdir=False):
    
        for keyname in self.details_dict:
            for streamname in self.streams:

                if keyname == streamname:
    
                    if "File_" in keyname:
                        original_filepath = self.details_dict[keyname]["OriginalName"]
                        original_filename = ntpath.basename(original_filepath)
                        streamdata = self.single_byte_xor(self.streams[streamname])

                        if outputdir:
                            with open(os.path.join(outputdir, original_filename), "w+") as f:
                                f.write(streamdata)
                                print "[ + ] Successfully wrote {}".format(original_filename)
                        else:
                            with open(original_filename, "w+") as f:
                                f.write(streamdata)
                                print "[ + ] Successfully wrote {}".format(original_filename)

                    if keyname == "Details":
                        if outputdir:
                            with open(os.path.join(outputdir, "Details"), "w+") as f:
                                f.write(self.details)
                                print "[ + ] Successfully wrote Details"
                        else:
                            with open("Details", "w+") as f:
                                f.write(self.details)
                                print "[ + ] Successfully wrote Details"


    def corrupted_bup(self, bup):

        count = 0
        key = ord('\x6a')
        out = ''
        details = "\x44\x65\x74\x61\x69\x6c\x73"
        end = "\x0d\x0a\x6a"
        
        f = open(bup, "rb").read()

        for i in f:
            out += chr(ord(i) ^ key)

        start_indexes = [i.start() for i in re.finditer(details, out)]
        end_indexes = [i.end()-1 for i in re.finditer(end, out)]

        while count < len(start_indexes):
            with open("Details-{}".format(count), "w") as f:
                f.write(out[start_indexes[count]:end_indexes[count]])
                count += 1



def main():
    
    p = ArgumentParser(description="Lord Of The Bups")
    p.add_argument("-f", "--file", help=".bup file to parse")
    p.add_argument("-c", "--corrupt", help="Attempt to parse the Details portion of a corrupted bup file", action="store_true")
    p.add_argument("-d", "--details", help="Print detection details", action="store_true")
    p.add_argument("-o", "--output", help="Specify an output directory for the decoded files")
    args = p.parse_args()

    if args.file:
        if os.path.isfile(args.file):
            if olefile.isOleFile(args.file):
                b = Bupectomy()
            else:
                sys.exit("[ - ] Not an OLE file")
        else:
            sys.exit("[ - ] {} not found".format(args.file))

        if args.details:
            b.extractfiles(args.file)
            b.details_to_json()
            print b.details

        elif args.output:
            b.extractfiles(args.file)
            b.details_to_json()
            b.writefiles(args.output)

        elif args.corrupt:
            b.corrupted_bup(args.file)

        else:
            b.extractfiles(args.file)
            b.details_to_json()
            b.writefiles()



if __name__ == "__main__":
    main()
