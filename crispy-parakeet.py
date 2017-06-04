#!/usr/bin/env python

#
# main.py

# ------------------------------------------------------------------------------
import logging
import argparse
import os
from fnmatch import fnmatch
import inotify.adapters
from multiprocessing import Process, Queue
from builtins import any

# Custom imports
from INotifyObj import INotifyObj
from Conf import Conf

# GLOBAL VARS
_DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
_LOGGER = logging.getLogger(__name__)


# ------------------------------------------------------------------------------
class File:
    def __init__(self):
        print("File init()")


# ------------------------------------------------------------------------------
def _configureLogging():
    _LOGGER.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    formatter = logging.Formatter(_DEFAULT_LOG_FORMAT)
    ch.setFormatter(formatter)

    _LOGGER.addHandler(ch)


# ------------------------------------------------------------------------------
def _find(path, match):
    files = []

    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            if fnmatch(f, match):
                files.append(f)

    return files


# ------------------------------------------------------------------------------
def watch(q, path):
    print(path)
    wp = bytes(path, encoding='utf-8');
    i = inotify.adapters.Inotify()

    i.add_watch(wp)

    try:
        for event in i.event_gen():
            if event is not None:
                (header, type_names, watch_path, filename) = event
                #_LOGGER.info("MASK->NAMES=%s WATCH-PATH=[%s] FILENAME=[%s]",
                #             type_names,
                #             watch_path.decode('utf-8'), filename.decode('utf-8'))
                d = INotifyObj(type_names, watch_path.decode('utf-8'), filename.decode('utf-8'))
                q.put(d)
    finally:
        i.remove_watch(wp)


# ------------------------------------------------------------------------------
def _main():
    # grab info from configure file
    c = Conf()

    watchQueue = Queue()

    # get args
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="directory to watch")
    args = parser.parse_args()

    # get abs path
    d = os.path.abspath(args.directory)

    if not os.path.isdir(d):
        print("Not a directory!  Exiting...")
        exit(1)

    # watch dir
    watchProcess = Process(target=watch, args=(watchQueue, d,))
    watchProcess.start()

    # test finding files
    match = "*silicon*valley*.mkv"
    files = _find(d, match)
    print(files)

    while True:
        d = watchQueue.get()

        # if no name then it is just an dir access
        if d.getName() == None:
            continue

        # only monitor moves into the dir & creation of files in dir
        if not any(d.getAction() in a for a in c.getActions()):
            continue

        _LOGGER.info(" ==> INotifyObj\n----------------------------------------%s", d)
        

    watchProcess.join() # this will stop the watch

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    _configureLogging()
    _main()

    exit(0)


# ------------------------------------------------------------------------------

