#bupectomy

###Description

Bupectomy is a Python script which assists with the handling of McAfee's .bup files. If you're unfamiliar, a great writeup on how McAfee deactivation works within the context of these bup files can be found [here.](http://blog.opensecurityresearch.com/2012/07/unbup-mcafee-bup-extractor-for-linux.html)

###Usage

At the time of this writeup, the usage is rather basic. With no command-line switches set, bupectomy will extract the files of interest from the bup, decode them, and write their contents to the current working directory. The "to-do" list below outlines my future plans for the script and recent additions.

```
usage: bupectomy.py [-h] [-d] [-o OUTPUT] bup

positional arguments:
  bup                   McAfee .bup file

optional arguments:
  -h, --help            show this help message and exit
  -d, --details         Print detection details
  -o OUTPUT, --output OUTPUT
                        Specify an output directory for the decoded files
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
