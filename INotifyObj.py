#!/usr/bin/env python

# INotifyObj.py

# ------------------------------------------------------------------------------
class INotifyObj:
    __action = None
    __isDir = False
    __watchPath = None
    __name = None


    def __init__(self, tn, wp, n):
        self.__action = tn[0]
        if tn[1] == "IN_ISDIR":
            self.__isDir = True
        self.__watchPath = wp
        if n != '':
            self.__name = n


    def __str__(self):
        s = "\nAction:\t\t" + str(self.v_action)
        s += "\nIs a Dir:\t" + str(self.v_isDir)
        s += "\nWatch Path:\t" + str(self.__watchPath)
        s += "\nName:\t\t" + str(self.__name)
        return s


    def getName(self):
        return self.__name


    def getAction(self):
        return self.__action

# ------------------------------------------------------------------------------
