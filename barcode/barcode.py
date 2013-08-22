#!/usr/bin/env python

"""
Design NGS barcodes.


Use any of the positional arguments with the -h option for more information.
"""

import argparse
import Levenshtein
from . import __version__, __author__, __contact__, __homepage__

def docSplit(func):
    return func.__doc__.split("\n\n")[0]

def version(name):
    """
    Return version information.

    @arg name: Name of the program.
    @type name: str

    @returns: Version information.
    @rtype: str
    """
    return "%s version %s\n%s\n%s\n%s" % (name, __version__, __author__,
        __contact__, __homepage__)
#version

class BarCode(object):
    """
    Design and test NGS barcodes.
    """
    __nucleotides = ['A', 'C', 'G', 'T']


    def __init__(self, distance=Levenshtein.distance):
        """
        Initialise the class.

        @arg distance: Distance function.
        @type distance: func
        """
        self.distance = distance
    #__init__

    def __allWords(self, bucket, word, length, result):
        """
        Generate all possible words of a certain length over a specified
        alphabet.

        @arg bucket: An alphabet.
        @type bucket: list[str]
        @arg word: A word over the alphabet {bucket}.
        @type word: str
        @arg length: Lenth of the barcodes.
        @type length: int
        @arg result: Constructed words.
        @type result: list[str]
        """
        if length:
            for i in bucket:
                self.__allWords(bucket, word + i, length - 1, result)
        else:
            result.append(word)
    #__allWords

    def allBarcodes(self, length):
        """
        Generate all possible barcodes of a certain length.

        @arg length: Lenth of the barcodes.
        @type length: int
        """
        result = []

        self.__allWords(self.__nucleotides, "", length, result)

        return result
    #allBarcodes

    def __filterStretch(self, barcode, stretches):
        """
        Test whether {barcode} contains none of the stretches in {stretches}.

        @arg barcode: A barcode.
        @type barcode: str
        @arg stretches:
        @type stretches: list[str]
        """
        for i in stretches:
            if i in barcode:
                return False

        return True
    #__filterStretch

    def filterStretches(self, barcodes, max_stretch):
        """
        Filter a list of barcodes for mononucleotide stretches.

        @arg barcodes: List of barcodes.
        @type barcodes: list[str]
        @arg max_stretch: Maximum mononucleotide stretch length.
        @type max_stretch: int
        """
        stretches = map(lambda x: (max_stretch + 1) * x, self.__nucleotides)
        result = []

        for i in barcodes:
            if self.__filterStretch(i, stretches):
                result.append(i)

        return result
    #filterStretches

    def __filterDistance(self, barcodes, candidate, min_dist):
        """
        Test whether {candidate} can be added to {barcodes} based on the
        minimum distance between {candidate} and all barcodes in {barcodes}.

        @arg barcodes: List of barcodes.
        @type barcodes: list[str]
        @arg candidate: Candidate barcode.
        @type candidate: str
        @arg min_dist: Minimum distance between the barcodes.
        @type min_dist: int
        """
        for i in barcodes:
            if self.distance(i, candidate) < min_dist:
                return False

        return True
    #__filterDistance

    def filterDistance(self, barcodes, min_dist):
        """
        Filter a list of barcodes for distances with other barcodes.

        @arg barcodes: List of barcodes.
        @type barcodes: list[str]
        @arg min_dist: Minimum distance between the barcodes.
        @type min_dist: int
        """
        result = []

        for i in barcodes:
            if self.__filterDistance(result, i, min_dist):
                result.append(i)

        return result
    #filterDistance
#BarCode

def barcode(length, max_stretch, min_dist, distance):
    """
    Make a set of barcodes, filter them for mononucleotide stretches and for
    distances with other barcodes.

    @arg length: Lenth of the barcodes.
    @type length: int
    @arg max_stretch: Maximum mononucleotide stretch length.
    @type max_stretch: int
    @arg min_dist: Minimum distance between the barcodes.
    @type min_dist: int
    @arg distance: Distance function.
    @type distance: func
    """
    B = BarCode(distance)

    return B.filterDistance(B.filterStretches(B.allBarcodes(length),
        max_stretch), min_dist)
#barcode

def testBarcodes(barcodes, min_dist, distance, handle):
    """
    Test a set of barcodes.

    @arg barcodes: List of barcodes.
    @type barcodes: list[str]
    @arg min_dist: Minimum distance between the barcodes.
    @type min_dist: int
    @arg distance: Distance function.
    @type distance: func

    @returns: The number of barcodes that violate the distance constraint.
    @rtype: int
    """
    B = BarCode(distance)

    good_subset = B.filterDistance(barcodes, min_dist)
    if handle:
        handle.write("\n".join(good_subset))

    return len(barcodes) - len(good_subset)
#testBarcodes

def main():
    """
    Main entry point.
    """
    output_parser = argparse.ArgumentParser(add_help=False)
    output_parser.add_argument("OUTPUT", type=argparse.FileType('w'),
        help="output file")
    input_parser = argparse.ArgumentParser(add_help=False)
    input_parser.add_argument("INPUT", type=argparse.FileType('r'),
        help="input file")
    distance_parser = argparse.ArgumentParser(add_help=False)
    distance_parser.add_argument("-d", dest="distance", type=int, default=3,
        help="minimum distance between the barcodes")
    distance_parser.add_argument("-H", dest="hamming", default=False,
        action="store_true", help="use Hamming distance")

    usage = __doc__.split("\n\n\n")
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=usage[0], epilog=usage[1])
    parser.add_argument("-v", action="version", version=version(parser.prog))
    subparsers = parser.add_subparsers(dest="subcommand")

    parser_make = subparsers.add_parser("make", parents=[output_parser,
        distance_parser], description=docSplit(barcode))
    parser_make.add_argument("-l", dest="length", type=int, default=8,
        help="lenght of the barcodes")
    parser_make.add_argument("-s", dest="stretch", type=int, default=2,
        help="maximum mononucleotide stretch length")

    parser_test = subparsers.add_parser("test", parents=[input_parser,
        distance_parser], description=docSplit(testBarcodes))
    parser_test.add_argument("-o", dest="output", type=argparse.FileType('w'),
        help="list of good barcodes")

    args = parser.parse_args()

    dfunc = Levenshtein.distance
    if args.hamming:
        dfunc = Levenshtein.hamming

    if args.subcommand == "make":
        args.OUTPUT.write("\n".join(barcode(args.length, args.stretch,
            args.distance, dfunc)))

    if args.subcommand == "test":
        print "%s barcodes violate the distance contraint." % testBarcodes(
            map(lambda x: x.strip(), args.INPUT.readlines()), args.distance,
            dfunc, args.output)
#main

if __name__ == "__main__":
    main()
