#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

import logging
import os
import re
import pyinotify
import time
import traceback

import signal
import hvsystem


HV_DIRECTORY = '/var/lib/hyperv'
HV_FILEREGEX = r'\.kvp_pool_\d'
stopping = False


def main():
    signal.signal(signal.SIGTERM, stop_gracefully)
    signal.signal(signal.SIGINT, stop_gracefully)
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    logging.warn('Start watching %s' % HV_DIRECTORY)
    process_all_files_from_directory(HV_DIRECTORY, process_file)
    watch(HV_DIRECTORY, process_file)


def stop_gracefully(signum, frame):
    global stopping
    stopping = True


def is_stopping(notifier_object=None):
    return stopping


def watch(directory, process_function):
    if hvsystem.is_freebsd():
        mask = pyinotify.IN_CREATE | pyinotify.IN_MODIFY
    else:
        mask = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MOVED_TO
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, EventHandler(directory, process_function), timeout=1000)
    wm.add_watch(directory, mask)
    notifier.loop(callback=is_stopping)


class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, directory, process_function):
        self.directory = directory
        self.process_function = process_function

    def process_default(self, event):
        self.process_function(event.pathname, event=event)


def process_all_files_from_directory(directory, process_function):
    for file_name in os.listdir(directory):
        if is_stopping():
            break
        path = os.path.join(directory, file_name)
        if not os.path.isfile(path):
            continue
        process_function(path, catch_exceptions=True)


def process_file(file_path, event=None, catch_exceptions=False):
    #wait for writing to complete_
    if hvsystem.is_freebsd():
        time.spleep(1)
    if not os.path.exists(file_path):
        return
    if not re.match(HV_FILEREGEX, os.path.basename(file_path)):
        return
    try:
        logging.info(file_path)
        hvsystem.process_file(file_path)
    except:
        logging.error((repr(file_path), event, repr(traceback.format_exc())))
        if not catch_exceptions:
            raise


if __name__ == '__main__':
    main()
