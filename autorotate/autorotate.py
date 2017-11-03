#!/usr/bin/env python2
import os
import os.path
import re
import subprocess
import sys
import time

from collections import namedtuple

devicename = 'NTRG0001:01 1B96:1B05'
freq = 5.0

MONITOR_CONNECTED_RE = re.compile(r'\bconnected\b')
DIGITIZER_RE = re.compile(r'NTRG0001\:01\s+1B96\:1B05')
PEN_RE = re.compile(r'\bPen (stylus|eraser)\b')
PROXIMITY_RE = re.compile(r'\bProximity\=(\w+)', re.M)

current_orientation = ''
currently_proximate = False
xinput_statemap = {True: 'disable', False: 'enable'}


def find_accelerometers():
    spath = '/sys/bus/iio/devices/'
    dpath = [os.path.join(spath, p) for p in os.listdir('/sys/bus/iio/devices/')
             if re.match('iio\:device\d', p) and os.path.exists(os.path.join(spath, p, 'in_accel_scale'))]
    if not dpath:
        sys.stderr.write("Could not find iio device to monitor.")
        sys.exit(1)

    return (os.path.join(dpath[0], 'in_accel_x_raw'),
            os.path.join(dpath[0], 'in_accel_y_raw'))

x_accel_path, y_accel_path = find_accelerometers()


def refreshtouch():
    os.system('xinput disable "NTRG0001:01 1B96:1B05"')
    os.system('xinput enable "NTRG0001:01 1B96:1B05"')


def countdisplays():
    return int(len([l for l in subprocess.check_output(['xrandr', '--current']).splitlines()
                            if MONITOR_CONNECTED_RE.search(l)]))


# Landscape
def lsx(thex): return thex >= 65000 or thex <= 650


# Portrait
def ptx(thex): return not lsx(thex)


# Left
def lfy(they): return they <= 65000 and they >= 64000


# Right
def rgy(they): return not lfy(they)


# It's a little odd that X labels it 'left' when you've just turned
# the tablet to the right, and vice versa, but that's the convention,
# I guess.
Transform = namedtuple('Tranform', ['name', 'mode', 'matrix', 'xrule', 'yrule'])
transforms = [
    Transform('normal',   0, '1 0 0 0 1 0 0 0 1',   lsx, lfy),
    Transform('inverted', 1, '-1 0 1 0 -1 1 0 0 1', lsx, rgy),
    Transform('left',     2, '0 -1 1 1 0 0 0 0 1',  ptx, rgy),
    Transform('right',    3, '0 1 0 -1 0 1 0 0 1',  ptx, lfy)
]


def is_in(pen):
    res = PROXIMITY_RE.search(subprocess.check_output(['xinput', 'query-state', pen]))
    return (res and res.group(1).lower() == 'in')


while True:
    int_displays = countdisplays()
    time.sleep(1.0/freq)
    if int_displays == 1:

        # Check accelerometers
        # Do we need to check the touch_devices list every time?  I
        # think we do; the list will change dynamically if we
        # dynamically load the stylus driver after the system has
        # booted.
        touch_devices = filter(lambda n: DIGITIZER_RE.match(n),
                               subprocess.check_output(['xinput', '--list', '--name-only']).splitlines()) 
        with open(x_accel_path, 'r') as fx:
            with open(y_accel_path, 'r') as fy:
                thex = float(fx.readline())
                they = float(fy.readline())
                for check in transforms:
                    if check.xrule(thex) and check.yrule(they):
                        if current_orientation != check.name:
                            print "Switching to orientation %s" % check.name
                            os.system('xrandr -o %s' % check.name)
                            for device in touch_devices:
                                os.system("xinput set-prop '%s' 'Coordinate Transformation Matrix' %s" %
                                          (device, check.matrix))
                            current_orientation = check.name
                            refreshtouch()

        # Palm rejection (sort-of):
        pen_devices = [p for p in touch_devices if PEN_RE.search(p)]
        pen_status = bool([p for p in pen_devices if is_in(p)])
        if pen_status != currently_proximate:
            print "%s palm rejection" % ("Activating" if pen_status else "Deactivating")
            currently_proximate = pen_status
            os.system("xinput %s '%s'" % (xinput_statemap[pen_status], devicename))
