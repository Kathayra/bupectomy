#bupectomy

###Description

Bupectomy is a Python script which assists with the handling of McAfee's .bup files. If you're unfamiliar, a great writeup on how McAfee deactivation works within the context of these bup files can be found [here.](http://blog.opensecurityresearch.com/2012/07/unbup-mcafee-bup-extractor-for-linux.html)

###Usage

At the time of this writeup, the usage is rather basic. With no command-line switches set, bupectomy will simply extract and decode the file_0 and Details files from McAfee's bup into the current working directory. Invoking the -d switch will print the Details file to stdout and exit. 

The "to-do" list below outlines my future plans for the script.

```
usage: bupectomy.py [-h] [-d] bup

positional arguments:
  bup            McAfee .bup file

optional arguments:
  -h, --help     show this help message and exit
  -d, --details  Print detection details
```

###Python Requirements

* argparse
* olefile
* os
* sys

###To-Do

- [x] Add functionality to specify an alternate output directory for the decoded files
- [ ] VirusTotal API support
- [ ] Malwr API support
- [ ] Re-write the detected file with its original file name
- [ ] Parse the Details text file properly
