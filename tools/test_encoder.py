#!/usr/bin/env python
import os
import sys
import struct
import gzip
import binascii
import operator
import itertools
import pickle
from pprint import pprint

def main():
    print "Hello!"

    dd = pickle.load(open('/home/slovak/Downloads/ILXEPSFirmwareHack/OriginalFirmware/39990-TV9-A910.bin.pickle', 'rb'))
    pprint(dd)


if __name__== "__main__":
    main()