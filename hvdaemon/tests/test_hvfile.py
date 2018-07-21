# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

import os
import unittest
from StringIO import StringIO
from collections import OrderedDict

from hvdaemon.hvfile import HVFile


class HVFileTest(unittest.TestCase):
    def setUp(self):
        super(HVFileTest, self).setUp()
        filename = os.path.realpath(__file__)
        self.path = os.path.dirname(filename)

    def test_readfile(self):
        filename = os.path.join(self.path, '.kvp_pool_1')
        hf = HVFile()
        hf.read(open(filename))
        self.assertEqual(hf.items(), OrderedDict((('test', 'abc'), ('test1', 'abc1'))).items())

    def test_write_read(self):
        whf = HVFile((('x', 'y'),))
        fd = StringIO()
        whf.write(fd)
        fd.seek(0)
        rhf = HVFile()
        rhf.read(fd)
        self.assertTrue(rhf['x'], 'y')
        self.assertEqual(len(rhf), 1)

    def test_write_max(self):
        hf = HVFile()
        hf[HVFile.KEY_LENGTH * 2 * 'a'] = HVFile.VALUE_LENGTH * 2 * 'b'
        fd = StringIO()
        hf.write(fd)
        self.assertEqual(fd.pos, HVFile.KEY_LENGTH + HVFile.VALUE_LENGTH)
