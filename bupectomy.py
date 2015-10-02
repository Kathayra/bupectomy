#!/usr/bin/python

from argparse import ArgumentParser
import getpass
import json
import ntpath
import os
import re
import requests
import sys
import tempfile

try:
    import olefile
except:
    sys.exit("[-] The 'olefile' module is required for bupectomy to run")

try:
    from smb.SMBConnection import SMBConnection
except:
    sys.exit("[-] The 'pysmb' module is required for bupectomy to run")


class Bupectomy(object):

    def __init__(self):

        self.streams = {}
        self.details_dict = {}

    def file_exists(self, bup):
        # Returns True if the file can be found

        file_exists = os.path.exists(bup)

        if file_exists:
                return True
        else:
            return False

    def isole(self, bup):
        # Returns True if the provided file is an OLE file

        olecheck = olefile.isOleFile(bup)

        if olecheck:
            return True
        else:
            return False

    def extractfiles(self, bup):

        ole = olefile.OleFileIO(bup)

        for item in ole.listdir():
            if ole.get_size(item[0]):
                encoded_stream = ole.openstream(item[0]).read()
                self.streams[item[0]] = encoded_stream
            else:
                print "[ - ] Cannot extract {} stream: Corrupt bup?".format(item[0])
                sys.exit()


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



    class Getbups(object):

        def __init__(self, host):

            self.domain = None

            if not self.domain:
                sys.exit("[-] No domain name provided. " \
                         "Edit the script to include " \
                         "your domain name")

            self.user = raw_input("Username: ")
            self.password = getpass.getpass("Password: ")
            self.host = host

            self.conn = SMBConnection(
                                      self.user,
                                      self.password,
                                      "Security",
                                      self.host,
                                      self.domain,
                                      use_ntlm_v2=True,
                                      sign_options=SMBConnection.SIGN_WHEN_SUPPORTED,
                                      is_direct_tcp=True
                                     )
            try:

                self.connection = self.conn.connect(
                                                    self.host,
                                                    port=445,
                                                    timeout=30
                                                   )
                
                if self.connection:
                    print "[+] Connected to {}".format(self.host)
                else:
                    sys.exit("[-] Unable to connect with {}".format(self.host))

            except Exception, e:
                sys.exit(e)

        def getbups(self):
            try:
                self.quarantine_file_list = self.conn.listPath(
                                                               'C$',
                                                               '/Quarantine',
                                                               pattern="*.bup"
                                                              )

            except Exception, e:
                self.conn.close()
                sys.exit("[-] Unable to find bup files at the location specified")

        def download_bups(self):

            if self.quarantine_file_list:
                print "[+] Found bup files"
            else:
                self.conn.close()
                sys.exit("No bups found on {}".format(host))

            try:
                os.mkdir("{}".format(self.host))

            except Exception, e:
                sys.exit(e)
                self.conn.close()

            try:
                for i in self.quarantine_file_list:
                    f = tempfile.NamedTemporaryFile()
                    file_attributes, filesize = self.conn.retrieveFile(
                                                                       "C$", 
                                                                       "/Quarantine/{}".format(i.filename),
                                                                       f
                                                                      )
                    f.seek(0)

                    with open("{0}/{1}".format(self.host, i.filename), "wb+") as newfile:
                        for i in f.read():
                            newfile.write(i)

                print "[+] Copied bup files succesfully"
                self.conn.close()

            except Exception, e:
                self.conn.close()
                sys.exit(e)


def main():
    
    p = ArgumentParser(description="Lord of the bups")
    p.add_argument("positional", help="McAfee .bup file for bup extraction, or system IP/name for downloading bups over SMB")
    p.add_argument("-c", "--corrupt", help="Attempt to parse the Details portion of a corrupted bup file", action="store_true")
    p.add_argument("-d", "--details", help="Print detection details", action="store_true")
    p.add_argument("-o", "--output", help="Specify an output directory for the decoded files")
    p.add_argument("-s", "--smb", help="Using SMB, extract all bup files from a workstation", action="store_true")
    args = p.parse_args()

    if args.smb:
        g = Bupectomy.Getbups(args.positional)
        g.getbups()
        g.download_bups()

    else:

        b = Bupectomy()

        if b.file_exists(args.positional):
            if b.isole(args.positional):

                if args.details:
                    b.extractfiles(args.positional)
                    b.details_to_json()
                    sys.exit(b.details)

                elif args.output:
                    b.extractfiles(args.positional)
                    b.details_to_json()
                    b.writefiles(args.output)

                elif args.corrupt:
                    b.corrupted_bup(args.positional)

                else:
                    b.extractfiles(args.positional)
                    b.details_to_json()
                    b.writefiles()

            else:
                sys.exit("[-] Not an OLE file")

        else:
            sys.exit("[-] File not found")


if __name__ == "__main__":
    main()
else:
    pass
