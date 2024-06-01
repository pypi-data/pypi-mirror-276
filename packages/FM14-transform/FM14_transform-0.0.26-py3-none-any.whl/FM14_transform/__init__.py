#!/usr/bin/env python

import argparse
import FM14_transform.data2bufr as data2bufr
import os

THISDIR = os.path.dirname(os.path.realpath(__file__))

def test():
    print("Hello world!")

def transform2bufr():
    parser = argparse.ArgumentParser(
        description='Utility to take as input a TAC or other text file containing a ' +
        'single FM14 SYNOP MOBIL record and convert to bufr file')
    parser.add_argument(
        'fm14', metavar='fm14', type=str, nargs=1,
        help='Filename of TAC or METAR bulletin'
    )
    parser.add_argument(
        'month', metavar='month', type=int, nargs=1,
        help='Numeric value (1-12) of the month of the observation'
    )
    parser.add_argument(
        'year', metavar='year', type=int, nargs=1,
        help='Year of the observation in YYYY format'
    )
    args = parser.parse_args()
    fm14_filename = args.fm14[0]
    month = args.month[0]
    year = args.year[0]

    with open(fm14_filename) as fh:
        data = fh.read()
    results = data2bufr.transform(data, year, month)

    for item in results:
        print(item)
        bufr4 = item['bufr4']
    