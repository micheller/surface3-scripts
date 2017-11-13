Surface3-Scripts
================

This program autorotates the screen of a Microsoft Surface Pro 3 Tablet
running Linux.  It correctly performs the autorotation for all major
pointer devices, including the stylus and eraser devices.  It also
enables palm rejection (meaning you can rest your hand on the screen
while drawing) when the stylus and eraser devices are "in use" (which is
defined by the digitizer as "within approximately 4cm of the screen").

This program is written in Python 2, which is included in all major
Linux distributions by default.  It has no additional dependencies.

It may run on other versions of the Microsoft Surface, but I haven't
tested it on anything other than my own Surface Pro 3.

Installation
-----------

To install, just copy autorotate/autorotate.py to a directory in your
$PATH.

Feel free to remove the '.py' extension; Linux doesn't use or
need it.  Also, remember to make the program executable:

```
chmod +x autorotate.py
```

(or whatever you choose to name it).

You may have to edit the first line of the autorotate script, if your
distro's Python 2 install doesn't include a link to it via the command
"python2".

Usage
-----
Start script:
```
$ python2 /path/to/autorotate.py
```

Credits
-------

The original geometry detection algorithms were written by
[Ayko Poel](https://github.com/AykoPoel/surface3-scripts).  My
contribution consists of more robust device and device driver
identification algorithms for the stylus and eraser, and a general
modernization of the transform algorithm.

