#!/usr/bin/python

import olefile
import subprocess
import sys
import re

bupFile = sys.argv[1]

def fileCheck(bup):
    # Checks for the file in the current directory
    fileExists = subprocess.Popen('find ./{}'.format(bupFile), 
                                                     shell=True,
                                                     stdout=subprocess.PIPE,
                                                     stderr=subprocess.PIPE
                                                     )
    fileExists.communicate()
    exitCode = fileExists.wait()
    if exitCode:
        print "[+] {} not found".format(bupFile)
        exit()
    # Ensures the submitted file is OLE
    # Creates output directory for xor'd files
    isOle = olefile.isOleFile(bup)
    if isOle:
        parseBupName = re.search(r'.+\.', bupFile)
        outputDirectory = "{}d".format(parseBupName.group(0))
        subprocess.call(['mkdir', outputDirectory])
        return outputDirectory
    else:
        exit()

def extractFiles(bup):
    # Extracts Details and File_0 from the bup
    # Iterates the extracted file streams, performing binary bitwise XOR and produces the decoded output files
    ole = olefile.OleFileIO(bup)
    xord_details = ole.openstream('Details').read()
    xord_file0 = ole.openstream('File_0').read()
    return xord_details, xord_file0

def single_byte_xor(buf):
    # Borrowed from Darren's explodebup.py, which borrowed from xortools.py
    # Elegant, efficient XOR function
    key = ord('\x6a')
    out = ''
    for i in buf:
        out += chr(ord(i) ^ key)
    return out

def writeNewFiles(details, file0):
    with open('{}/Details.txt'.format(newDir), 'w') as deets:
        deets.write(details)

    with open('{}/File_0.bin'.format(newDir), 'wb') as file_0:
        file_0.write(file0)

newDir = fileCheck(bupFile)
xordFiles = extractFiles(bupFile)
detailsFinal = single_byte_xor(xordFiles[0])
file0Final = single_byte_xor(xordFiles[1])
writeNewFiles(detailsFinal, file0Final)
