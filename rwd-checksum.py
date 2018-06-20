#!/usr/bin/env python3

# Example usage:
# python3 rwd-checksum.py 39990-TV9-A910.rwd
# file checksum: 0x1bdbfef = 0x44f4c38
# Not Ok, to be calculated and updated
# Update checksum in original file (Y/N): Y
# rwd file was updated. Validate checksum again:
# file checksum: 0x44f4c38 = 0x44f4c38

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
    with open(sys.argv[1], 'rb') as bin_file:
        raw_data = bin_file.read()

    file_checksum_expected, file_checksum_actual = get_file_checksum(raw_data)

    if file_checksum_expected == file_checksum_actual:
        print('Ok')
    else:
        print('Not Ok, to be calculated and updated')
        raw_data = bytearray(raw_data)
        raw_data[-4:] = file_checksum_actual.to_bytes(4, byteorder='little')

        user_input = input('Update checksum in original file (Y/N): ')

        if user_input == 'Y':

            with open(sys.argv[1], 'wb') as o:
                o.write(raw_data)
            print('rwd file was updated. Validate checksum again:')

            with open(sys.argv[1], 'rb') as bin_file:
                raw_data = bin_file.read()

            file_checksum_expected, file_checksum_actual = get_file_checksum(raw_data)

            assert file_checksum_expected == file_checksum_actual, 'Checksum was not properly calculated!!!'


if __name__ == "__main__":
    main()
