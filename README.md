Surface3-Scripts
================

Originally derived from surface3-scripts, this program is just the same
but with regular expressions changed to match yoga 920 UHD devices.

It also enables palm rejection (meaning you can rest your hand on the screen
while drawing) when the stylus and eraser devices are "in use" (which is
defined by the digitizer as "within approximately 4cm of the screen").

This program is written in Python 2, which is included in all major
Linux distributions by default.  It has no additional dependencies.

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

Gratefully forked from https://github.com/elfsternberg/surface3-scripts
link obtained from https://www.reddit.com/r/linux/comments/6xuv7v/yoga_920_and_gnulinux/dt881bk/
