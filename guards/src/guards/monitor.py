# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# monitor.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import config as cfg
import sys
import os
import urllib
import daemon
from datetime import datetime
from threading import Timer
import motion


""" the configuration """
config = None

""" the monitors """
monitors = None

""" recent image list per monitor """
recent_images = {}


def get_image(monitor):
    """
    Retrieves the image for the defined monitor.
    :param monitor: the monitor
    :type monitor: str
    """
    global config, monitors, recent_images
    ts = datetime.now()
    filename = ts.strftime(config['general']['timestamp'])
    # paused?
    out_dir = monitors[monitor]['output']
    out_file = out_dir + os.sep + filename
    if not os.path.exists(out_dir + os.sep + "PAUSED"):
        urllib.urlretrieve(monitors[monitor]['url'], out_file)
        recent_images[monitor].insert(0, out_file)
        recent_images[monitor] = recent_images[monitor][:2]
        # detect motion?
        if monitors[monitor]['detect_motion'] and (len(recent_images[monitor]) == 2):
            detected = motion.detect_motion(recent_images[monitor][0], recent_images[monitor][1], monitors[monitor]['threshold'])
            # delete old file?
            if not detected:
                os.remove(recent_images[monitor][1])
    Timer(monitors[monitor]['interval'], get_image, args=[monitor]).start()


def main():
    # load config
    global config, monitors, recent_images
    config = cfg.load_config()
    monitors = cfg.get_monitors(config)

    # create output dirs if necessary
    for monitor in monitors:
        out_dir = monitors[monitor]['output']
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

    # retrieve images
    for monitor in monitors:
        print "Starting monitor:", monitor
        recent_images[monitor] = []
        Timer(monitors[monitor]['interval'], get_image, args=[monitor]).start()

if __name__ == '__main__':
    if "-d" in sys.argv:
        with daemon.DaemonContext():
            main()
    else:
        main()
