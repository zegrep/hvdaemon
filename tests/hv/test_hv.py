# -*- coding: utf-8 -*-
import unittest
from collections import OrderedDict

from hvdaemon.hv import HVFile


class HVTest(unittest.TestCase):
    def test_readfile(self):
        hf = HVFile(open('.kvp_pool_1'))
        hf.read()
        self.assertEqual(hf.items(), OrderedDict((('test', 'abc'), ('test1', 'abc1'))).items())