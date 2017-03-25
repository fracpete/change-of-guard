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

# config.py
# Copyright (C) 2017 Fracpete (fracpete at gmail dot com)

import yaml


def load_config(config=None):
    """
    Loads the configuration.
    :param config: the configuration file to load, uses default it None
    :type config: str
    :return: yaml dictionary
    :rtype: dict
    """
    if config is None:
        config = 'palace/config.yaml'
    f = open(config)
    config = yaml.safe_load(f)
    f.close()
    return config


def get_monitors(config):
    """
    Returns a list of available monitors, i.e., all the enabled ones.
    :param config: the configuration to use
    :type config: dict
    :return: dictionary of monitors
    :rtype: dict
    """
    result = {}
    for monitor in config['monitors']:
        result[monitor] = config['monitors'][monitor]
    return result
