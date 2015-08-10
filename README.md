#bupectomy

###Description

Bupectomy is a Python script which assists with the handling of McAfee's .bup files. If you're unfamiliar, a great writeup on how McAfee deactivation works within the context of these bup files can be found [here.](http://blog.opensecurityresearch.com/2012/07/unbup-mcafee-bup-extractor-for-linux.html)

###Usage

With no command-line switches set, bupectomy will extract the files of interest from the bup, decode them, and write their contents to the current working directory. The "to-do" list below outlines my future plans for the script and recent additions.

```
positional arguments:
  bup                   McAfee .bup file

optional arguments:
  -h, --help            show this help message and exit
  -d, --details         Print detection details
  -o OUTPUT, --output OUTPUT
                        Specify an output directory for the decoded files
  -v, --vt              Check VirusTotal for this file in a previous
                        submission
```

###VirusTotal

**A VirusTotal API key is required for this functionality. Define it in the VirusTotal class, under init**

I have recently added support to check the file McAfee detected as malicious against VirusTotal's public API. As of now, this functionality simply checks to see if the sample has been submitted before using the file's SHA256 hash. Example below for a file in VirusTotal's database:

```
===================
File Scan Results
===================

Scanned File: <filename>
Scan Date: 2015-07-14 11:05:19
Detection: 4 / 55
Permalink: https://www.virustotal.com/file/a1dd7c6e65232bc5336f499a37d60b1b44c19e090561056e6d7dd018c1dd4431/analysis/1436871919/

```

###Python Requirements

* argparse
* hashlib
* json
* ntpath
* olefile
* os
* requests
* sys

###To-Do

- [x] ~~Add functionality to specify an alternate output directory for the decoded files~~
- [x] ~~VirusTotal API support~~
- [ ] Malwr API support
- [x] ~~Re-write the detected file with its original file name~~
- [ ] Parse the Details text file properly
