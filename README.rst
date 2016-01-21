Bupectomy
-----------
Bupectomy is a Python script which assists with the handling of McAfee's .bup files. If you're unfamiliar, a nice writeup on how McAfee deactivation works within the context of these bup files can be found `here. <http://blog.opensecurityresearch.com/2012/07/unbup-mcafee-bup-extractor-for-linux.html>`_

Features
---------
* JSON output of the 'Details' file
* Bupectomy renames the detected file to its original file name
* Cross-platform


Command-Line Options
---------------------

::

    dev@computer:~/$ python bupectomy.py -h
    usage: bupectomy.py [-h] [-f FILE] [-c] [-d] [-o OUTPUT]

    Lord Of The Bups

    optional arguments:
      -h, --help            show this help message and exit
      -f FILE, --file FILE  .bup file to parse
      -c, --corrupt         Attempt to parse the Details portion of a corrupted
                            bup file
      -d, --details         Print detection details
      -o OUTPUT, --output OUTPUT
                            Specify an output directory for the decoded files

**--file**

Using the ``--file / -f`` switch provides the output below:

::

    dev@computer:~$ python bupectomy.py -f 7e011483422800.bup 
    [ + ] Successfully wrote KINDLESETUP[1].EXE
    [ + ] Successfully wrote Details

    dev@computer:~$ ls
    Details  KINDLESETUP[1].EXE

**--output**

Add the ``--output / -o`` switch to redirect the files to a location of your choice: 

::

    dev@computer:~$ python bupectomy.py -f 7e011483422800.bup -o /tmp 
    [ + ] Successfully wrote KINDLESETUP[1].EXE
    [ + ] Successfully wrote Details

    dev@computer:~$ ls /tmp
    Details KINDLESETUP[1].EXE

**--details**

Add the ``--details / -d`` flag to print the Details section to stdout:

::

    dev@computer:~/$ python bupectomy.py -f 7e011483422800.bup -d 

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

 
Corrupted .bup Files
----------------------
Every so often, McAfee (seemingly) mangles the bup file when it is created. In this case, the sector data pointers are not properly written to disk; using most "unbup" scripts against such a file will not work. Even though the data pointers are not correct, often times the data itself is still in good working order within the file. When invoked with the '-c' flag on a corrupted bup file, bupectomy will attempt to locate the Details stream and write it to disk. In this case, the Details file will not be a JSON formatted string. This feature of bupectomy works on some assumptions about the data, and may not work for every corrupt bup file. 

Python Requirements
--------------------
* argparse
* json
* ntpath
* os
* re
* sys
* olefile
