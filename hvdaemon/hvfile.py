# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

import collections

ZERO = b'\x00'


class HVFile(collections.OrderedDict):
    KEY_LENGTH = 512
    VALUE_LENGTH = 2048

    def read(self, fd):
        key = fd.read(self.KEY_LENGTH)
        while key:
            value = fd.read(self.VALUE_LENGTH)
            self[key.rstrip(ZERO)] = value.rstrip(ZERO)
            key = fd.read(self.KEY_LENGTH)

    def write(self, fd):
        for key, value in self.items():
            fd.write(self._format(key, self.KEY_LENGTH))
            fd.write(self._format(value, self.VALUE_LENGTH))

    def _format(self, data, length):
        padding = max(0, length - len(data))
        return (data + (padding * ZERO))[:length]