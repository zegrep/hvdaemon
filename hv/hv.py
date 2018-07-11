# -*- coding: utf-8 -*-
import collections

class HVFile(object):
    KEY_LENGTH = 512
    VALUE_LENGTH = 2048

    def __init__(self, fd):
        self.fd = fd
        self.data = collections.OrderedDict()

    def read(self):
        key = self.fd.read(self.KEY_LENGTH)
        while key:
            value = self.fd.read(self.VALUE_LENGTH)
            self.data[key.rstrip('\x00')] = value.rstrip('b\x00')
            key = self.fd.read(self.KEY_LENGTH)

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def items(self):
        return self.data.items()