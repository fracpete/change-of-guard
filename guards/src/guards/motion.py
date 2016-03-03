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

# motion.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import config as cfg
import os
import cv2
import numpy as np


def load_img(img_file):
    """
    Reads the specified image, converts it to binary and returns it.
    :param img_file: the file to load
    :type img_file: str
    :return: the image
    """
    config = cfg.load_config()
    image = cv2.imread(img_file)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
        config['general']['threshold']['blocksize'], config['general']['threshold']['C'])
    # remote some noise
    size = config['general']['noise']['kernel']
    kernel = np.ones((size, size), np.uint8)
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    return opening


def diff_img(t0, t1):
    """
    Computes the absolute difference between two images.
    :param t0: the first image
    :param t1: the second image
    """
    return cv2.absdiff(t0, t1)


def count_diff(img):
    """
    Counts the non-zero pixels in the image.
    param img: the image to process
    :return: the count
    :rtype: int
    """
    return cv2.countNonZero(img)


def detect_motion(t0, t1, threshold):
    """
    Returns true if there was motion detected between the two images.
    :param t0: the first image (image/filename)
    :param t1: the second image (image/filename)
    :param threshold: the threshold in percent (0-1)
    :type threshold: float
    :return: the detected ratio, whether motion was detected
    :rtype threshold: (float, bool)
    """
    if isinstance(t0, basestring):
        t0 = load_img(t0)
    if isinstance(t1, basestring):
        t1 = load_img(t1)
    size = t0.size
    count = count_diff(diff_img(t0, t1))
    ratio = float(count) / float(size)
    return ratio, ratio > threshold


def main():
    # load config
    config = cfg.load_config()

    # motion?
    monitors = cfg.get_monitors(config)
    for monitor in monitors:
        print monitor
        l = []
        d = monitors[monitor]['output']
        for f in os.listdir(d):
            full = os.path.join(d, f)
            if os.path.isfile(full):
                l.append(full)
        l.sort()
        if len(l) > 1:
            t_now = None
            for i in xrange(len(l)):
                t_minus = t_now
                t_now = load_img(l[i])
                if not (t_minus is None) and not (t_now is None):
                    value, motion = detect_motion(t_minus, t_now, monitors[monitor]['threshold'])
                    print("  %s %s %0.3f %s" % (os.path.basename(l[i-1]), os.path.basename(l[i]), value, motion))

if __name__ == '__main__':
    main()
