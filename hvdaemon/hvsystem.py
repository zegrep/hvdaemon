# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

import logging
import sys

logger = logging.getLogger()
del logging


def process_file(filename):
    logger.info(filename)


def is_freebsd():
    return sys.platform.startswith('freebsd')