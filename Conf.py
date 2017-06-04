#!/usr/bin/env python

#
# Conf.py

import subprocess
import os.path as path
import json

# ------------------------------------------------------------------------------
class Conf:
    __path = "./cp.conf"
    __whitelistActions = ['IN_MOVED_TO', 'IN_CREATE']
    __ffmpegBin = "Not found.  Please Install ffmpeg."
    __ffmpegOpt = dict(video='h264', audio='aac', hardsubbing='false') # subtitle can be embedded
    __to = '/media/plex'
    __tmp = '/tmp'
    __info = dict()

    def __init__(self):
        # find ffmpeg bin
        c = subprocess.run(["which", "ffmpeg"], stdout=subprocess.PIPE)
        if c.returncode == 0 and c.stdout != None:
            self.__ffmpegBin = c.stdout.decode('utf-8').rstrip();

        self.__readConf()


    def __str__(self):
        return str(self.__info)


    # generate default conf file
    def __generateConf(self):
        d = dict(whitelistActions=self.__whitelistActions, ffmpegBin=self.__ffmpegBin,
            to=self.__to, tmp=self.__tmp, ffmpegOpt=self.__ffmpegOpt)
        with open(self.__path, 'w', encoding="utf-8") as f:
            json.dump(d, f, indent=4, sort_keys=True)


    # Read and save conf file
    def __readConf(self):
        if not path.exists(self.__path):
            self.__generateConf()

        with open(self.__path, 'r', encoding="utf-8") as f:
           self.__info = json.load(f)


    def getActions(self):
        return self.__whitelistActions


    def getInfo(self):
        return self.__info


# ------------------------------------------------------------------------------