#!/usr/bin/env python
import os
import sys
import struct
import gzip
import binascii
import operator
import itertools
import pickle


def main():
    # f_name, f_ext = os.path.splitext(sys.argv[1])

    with open(sys.argv[1], 'rb') as bin_file:
        bin_data = bin_file.read()

    meta_data = pickle.load(open(sys.argv[1] + '.pickle', 'rb'))

    # Collect data chunks.

    data_chuncs = ''
    for addr in meta_data['addresses']:
        adr_bytes = chr(((addr >> 4) >> (8 * 0)) & 0xFF) + chr(((addr >> 4) >> (8 * 0)) & 0xFF)

        # data_chuncs = data_chuncs + adr_bytes +


    # Calculate and set firmware checksums
    # Encript
    # Prepend rwd top
    # Calculate and set rwd checksum
    # Write dto disc with _hacked postfix

    print(meta_data.keys())


if __name__ == "__main__":
    main()
