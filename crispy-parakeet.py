#!/usr/bin/env python

#
# main.py

# ------------------------------------------------------------------------------
import logging
import argparse
import sys
import os.path as path
import inotify.adapters
from multiprocessing import Process, Queue

# GLOBAL VARS
_DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
_LOGGER = logging.getLogger(__name__)


# ------------------------------------------------------------------------------
def _configure_logging():
    _LOGGER.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    formatter = logging.Formatter(_DEFAULT_LOG_FORMAT)
    ch.setFormatter(formatter)

    _LOGGER.addHandler(ch)


# ------------------------------------------------------------------------------
def watch(q, path):
    print(path)
    wd = bytes(path, encoding='utf-8');
    i = inotify.adapters.Inotify()

    i.add_watch(wd)

    try:
        for event in i.event_gen():
            if event is not None:
                (header, type_names, watch_path, filename) = event
                _LOGGER.info("MASK->NAMES=%s WATCH-PATH=[%s] FILENAME=[%s]",
                             type_names,
                             watch_path.decode('utf-8'), filename.decode('utf-8'))
                q.put([type_names, watch_path.decode('utf-8'), filename.decode('utf-8')])
    finally:
        i.remove_watch(wd)


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
        print(watchQueue.get())

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    _configure_logging()
    _main()

    exit(0)


# ------------------------------------------------------------------------------

