"""
data_handlers.py: Data handler interface for render hooks

Copyright (C) 2017 Isaac Weaver
Author: Isaac Weaver <wisaac407@gmail.com>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""


class DataHandler:
    """Base class for all data handlers"""

    def __init__(self, *data):
        self._data = data

    @property
    def data(self):
        if len(self._data) == 1:
            return self._data[0]
        return self._data

    @data.setter
    def data(self, data):
        if isinstance(data, (tuple, list, set)):
            self._data = data
        else:
            self._data = (data,)

    def load(self, raw):
        """Read in the data from the raw string"""
        raise NotImplementedError

    def dump(self):
        """Return the formatted data"""
        raise NotImplementedError


class StringHandler(DataHandler):
    """String interface"""

    def dump(self):
        return self.data

    def load(self, raw):
        self._data = raw


class NullStringHandler(DataHandler):
    """Writes string but doesn't read anything (used for time hook etc.)"""

    def dump(self):
        """Write the data; format it if more than one argument was given to __init__"""
        if len(self._data) > 1:
            return self._data[0].format(self._data[1:])
        # If it's just one argument than make sure it's a string
        return str(self._data[0])

    def load(self, raw):
        """Do nothing here"""
        pass


class NumberHandler(DataHandler):
    """Handles numbers"""
    default = 0.0
    number_type = float

    def load(self, raw):
        try:
            parsed = self.number_type(raw)
        except ValueError:
            parsed = self.default

        self.data = parsed

    def dump(self):
        return str(self.data)


class IntHandler(NumberHandler):
    """Handles numbers"""
    default = 0
    number_type = int


class BoolHandler(DataHandler):
    """Handles booleans"""

    def load(self, raw):
        if raw == 'True':
            self.data = True
        else:
            self.data = False

    def dump(self):
        return self.data
