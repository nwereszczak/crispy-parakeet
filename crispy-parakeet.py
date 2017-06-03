#!/usr/bin/env python

#
# main.py

# ------------------------------------------------------------------------------
import logging
import json
import argparse
import os.path as path
import inotify.adapters

from multiprocessing import Process, Queue
from builtins import any

# GLOBAL VARS
_DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
_LOGGER = logging.getLogger(__name__)
_GOOD_ACTIONS = ['IN_MOVED_TO', 'IN_CREATE']

# ------------------------------------------------------------------------------
class Data:
    action = None
    isDir = False
    watchPath = None
    name = None

    def __init__(self, tn, wp, n):
        self.action = tn[0]
        if tn[1] == "IN_ISDIR":
            self.isDir = True
        self.watchPath = wp
        if n != '':
            self.name = n

    def __str__(self):
        s = "\nAction:\t\t" + str(self.action)
        s += "\nIs a Dir:\t" + str(self.isDir)
        s += "\nWatch Path:\t" + str(self.watchPath)
        s += "\nName:\t\t" + str(self.name)
        return s

    def getName(self):
        return self.name

    def getAction(self):
        return self.action


# ------------------------------------------------------------------------------
def _configureLogging():
    _LOGGER.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    formatter = logging.Formatter(_DEFAULT_LOG_FORMAT)
    ch.setFormatter(formatter)

    _LOGGER.addHandler(ch)


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
                d = Data(type_names, watch_path.decode('utf-8'), filename.decode('utf-8'))
                q.put(d)
    finally:
        i.remove_watch(wp)


# ------------------------------------------------------------------------------
def _main():
    watchQueue = Queue()

    # get args
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="directory to watch")
    args = parser.parse_args()

    # get abs path
    d = path.abspath(args.directory)

    if not path.isdir(d):
        print("Not a directory!  Exiting...")
        exit(1)

    # watch dir
    watchProcess = Process(target=watch, args=(watchQueue, d,))
    watchProcess.start()

    while True:
        d = watchQueue.get()

        # if no name then it is just an dir access
        if d.getName() == None:
            continue

        # only monitor moves into the dir & creation of files in dir
        if not any(d.getAction() in a for a in _GOOD_ACTIONS):
            continue

        _LOGGER.info(" ==> Data\n----------------------------------------%s", d)


    watchProcess.join() # this will stop the watch

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    _configureLogging()
    _main()

    exit(0)


# ------------------------------------------------------------------------------

