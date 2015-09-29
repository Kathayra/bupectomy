#bupectomy

###Description

Bupectomy is a Python script which assists with the handling of McAfee's .bup files. If you're unfamiliar, a great writeup on how McAfee deactivation works within the context of these bup files can be found [here.](http://blog.opensecurityresearch.com/2012/07/unbup-mcafee-bup-extractor-for-linux.html)

#Usage

With no command-line switches set, bupectomy will extract the files of interest from the bup, decode them, and write their contents to the current working directory.

###Alternate output directory

With the -o or --ouput command-line flags set, bupectomy will write the decoded files to your directory of choice:

```
dev@computer:$ bupectomy.py -o /tmp 7df9fc10c2760.bup
[ + ] Successfully wrote Details
[ + ] Successfully wrote index[1].htm
dev@computer:$ cd /tmp
dev@computer:/tmp$ ls
Details  index[1].htm
```

...something recently added, bupectomy now always writes/prints a JSON-formatted Details file. A sanitized example of this is below:

```
dev@computer:$ cat Details

{
    "Details": {
        "CreationDay": "day", 
        "CreationHour": "hour", 
        "CreationMinute": "minute", 
        "CreationMonth": "month", 
        "CreationSecond": "second", 
        "CreationYear": "year", 
        "DATMajor": "major", 
        "DATMinor": "minor", 
        "DATType": "dat", 
        "DetectionName": "name", 
        "DetectionType": "type", 
        "EngineMajor": "engine", 
        "EngineMinor": "engine", 
        "NumberOfFiles": "number", 
        "NumberOfValues": "number", 
        "ProductID": "id", 
        "TimeZoneName": "timezonename", 
        "TimeZoneOffset": "offset"
    }, 
    "File_0": {
        "ObjectType": "type", 
        "OriginalName": "\\driveletter:\\Path\\\\To\\File", 
        "WasAdded": "number"
    }

```

###Details File Only

Executing bupectomy with the '-d' flag set simply prints the contents of the Details stream and exits. This functionality also pretty-prints a JSON-formatted string.

###Corrupted Bup Files

Every once in a while, McAfee (seemingly) mangles the bup file when it is created. In this case, the sector data pointers are not properly written to disk; using most "unbup" scripts against such a file will not work. Even though the data pointers are not correct, often times the data itself is still in good working order within the file. When invoked with the '-c' flag on a corrupted bup file, bupectomy will attempt to locate the Details stream and write it to disk. In this case, the Details file will not be a JSON formatted string. This feature of bupectomy works on some assumptions about the data, and may not work for every corrupt bup file. 

###Automated Bup Collection

Another new addition is the ability to collect bup files from a given hostname via SMB. This feature also makes some assumptions and may not work out-of-the-box in every environment. Though with a little tweaking it should be helpful.

Bupectomy's Getbups() class is assuming that: A workstation's C drive accessible via SMB, and that McAfee's Quarantine directory (containing the bup files) is sitting in the root of C. Next, you'll have to add your NT user account's domain name to the Getbups() class in the bupectomy script:

 class Getbups(object):

        def __init__(self, host):

            self.domain = Your-Domain-Goes-Here

...ensure that you wrap the domain name in quotes, making it a string object. Once that has been completed, a successful utilization of this feature looks like this:

```
dev@computer:~$ bupectomy.py -s <HostnameOrIP>
Username: username
Password: password
[+] Connected to <HostnameOrIP>
[+] Found bup files
[+] Copied bup files succesfully

```
...the bup files in question will be written into a new directory. The new directory name is the name of the workstation hostname or workstation IP address entered during the command's execution.

```

```
usage: bupectomy.py [-h] [-c] [-d] [-o OUTPUT] [-s] positional

Lord of the bups

positional arguments:
  positional            McAfee .bup file for bup extraction, or system IP/name
                        for downloading bups over SMB with the -s flag

optional arguments:
  -h, --help            show this help message and exit
  -c, --corrupt         Attempt to parse the Details portion of a corrupted
                        bup file
  -d, --details         Print detection details
  -o OUTPUT, --output OUTPUT
                        Specify an output directory for the decoded files
  -s, --smb             Using SMB, extract all bup files from a workstation

```

#Python Requirements

*argparse
*getpass
*json
*ntpath
*os
*re
*requests
*sys
*tempfile
*olefile
*pysmb

#To-Do

- [x] ~~Add functionality to specify an alternate output directory for the decoded files~~
- [x] ~~Re-write the detected file with its original file name~~
- [x] ~~Parse the Details text file properly~~
- [x] ~~Use SMB to automate the fetching of bup files from a given workstation~~

###Removed Functionality

Recently, bupectomy went through somewhat of a re-write to provide more accuracy and include features such as --corrupt and --smb. During this re-write, the VirusTotal submission functionality was removed.
