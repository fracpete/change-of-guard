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
import os
import urllib
from datetime import datetime

# load config
config = cfg.load_config()
monitors = cfg.get_monitors(config)

# create output dirs if necessary
for monitor in monitors:
    outDir = monitors[monitor]['output']
    if not os.path.exists(outDir):
        os.makedirs(outDir)

# create timestamp
ts = datetime.now()
filename = ts.strftime(config['general']['timestamp'])

# retrieve images
for monitor in monitors:
    urllib.urlretrieve(monitors[monitor]['url'], monitors[monitor]['output'] + os.sep + filename)
