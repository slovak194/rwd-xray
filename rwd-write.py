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


def get_checksum(data):
    result = -sum(data)
    return result & 0xFF

import sys
import struct


def get_file_checksum(data):
    expected = struct.unpack('<L', data[-4:])[0]
    actual = sum(data[0:-4])

    print("file checksum: {} = {}".format(
        hex(expected),
        hex(actual)))

    return expected, actual


def main():
    f_name, f_ext = os.path.splitext(sys.argv[1])

    with open(sys.argv[1], 'rb') as bin_file:
        bin_data = bin_file.read()

    bin_data = bytearray(bin_data)

    meta_data = pickle.load(open(sys.argv[1] + '.pickle', 'rb'))

    # pprint(meta_data)

    # Calculate and set firmware checksums

    for start, end in meta_data['checksums']:
        calculated_sum = get_checksum(bin_data[start:end])
        check_sum = bin_data[end]
        print("{} {} {}".format(hex(check_sum), "=" if check_sum == calculated_sum else "!=", hex(calculated_sum)))
        if calculated_sum != check_sum:
            user_input = input('Update checksum in original file (Y/N): ')
            if user_input == 'Y':
                bin_data[end] = calculated_sum

    # Encript

    enrypted = b''.join([*map(lambda x: meta_data['encoder'][x].to_bytes(1, byteorder='little'), bin_data)])

    # exit(0)

    data_chuncs = b''

    # Prepend rwd top
    data_chuncs += meta_data['rwd_top']

    # Collect data chunks.
    for addr in meta_data['addresses']:
        addr_bytes = (addr >> 4).to_bytes(2, byteorder='big')

        data_chuncs += addr_bytes + enrypted[addr:addr+128]

    # Set rwd file checksum
    rwd_chekcsum = sum(data_chuncs)
    data_chuncs += rwd_chekcsum.to_bytes(4, byteorder='little')

    # Validate
    get_file_checksum(data_chuncs)

    # Write dto disc with _hacked postfix
    with open(f_name + '_hacked.rwd', 'wb') as o:
        o.write(data_chuncs)
    print('rwd file was written.')


if __name__ == "__main__":
    main()
