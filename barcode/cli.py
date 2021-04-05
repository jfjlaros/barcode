import argparse
import sys

import Levenshtein

from . import doc_split, usage, version
from .barcode import all_barcodes, filter_distance, filter_stretches


def make_barcodes(length, max_stretch, min_dist, distance):
    """Make a set of barcodes, filter them for mononucleotide stretches and for
    distances with other barcodes.

    :arg int length: Lenth of the barcodes.
    :arg int max_stretch: Maximum mononucleotide stretch length.
    :arg int min_dist: Minimum distance between the barcodes.
    :arg function distance: Distance function.
    """
    return filter_distance(
        filter_stretches(all_barcodes(length), max_stretch), min_dist)


def test_barcodes(barcodes, min_dist, distance, handle):
    """Test a set of barcodes.

    :arg list barcodes: List of barcodes.
    :arg int min_dist: Minimum distance between the barcodes.
    :arg function distance: Distance function.
    :arg steam handle: Open readable handle to a file.

    :returns int: The number of barcodes that violate the distance constraint.
    """
    good_subset = filter_distance(barcodes, min_dist)
    if handle:
        handle.write('\n'.join(good_subset))

    return len(barcodes) - len(good_subset)


def _arg_parser():
    """Command line argument parsing."""
    output_parser = argparse.ArgumentParser(add_help=False)
    output_parser.add_argument(
        'OUTPUT', type=argparse.FileType('w'), help='output file')
    input_parser = argparse.ArgumentParser(add_help=False)
    input_parser.add_argument(
        'INPUT', type=argparse.FileType('r'), help='input file')
    distance_parser = argparse.ArgumentParser(add_help=False)
    distance_parser.add_argument(
        '-d', dest='distance', type=int, default=3,
        help='minimum distance between the barcodes (int default=%(default)s)')
    distance_parser.add_argument(
        '-H', dest='hamming', default=False,
        action='store_true', help='use Hamming distance')

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=usage[0], epilog=usage[1])
    parser.add_argument('-v', action='version', version=version(parser.prog))
    subparsers = parser.add_subparsers(dest='subcommand')
    subparsers.required = True

    parser_make = subparsers.add_parser(
        'make', parents=[output_parser, distance_parser],
        description=doc_split(make_barcodes))
    parser_make.add_argument(
        '-l', dest='length', type=int, default=8,
        help='lenght of the barcodes (int default=%(default)s)')
    parser_make.add_argument(
        '-s', dest='stretch', type=int, default=2,
        help='maximum mononucleotide stretch length (int default=%(default)s)')

    parser_test = subparsers.add_parser(
        'test', parents=[input_parser, distance_parser],
        description=doc_split(test_barcodes))
    parser_test.add_argument(
        '-o', dest='output', type=argparse.FileType('w'),
        help='list of good barcodes')

    return parser


def main():
    """Main entry point."""
    parser = _arg_parser()

    try:
        args = parser.parse_args()
    except IOError as error:
        parser.error(error)

    dfunc = Levenshtein.distance
    if args.hamming:
        dfunc = Levenshtein.hamming

    if args.subcommand == 'make':
        args.OUTPUT.write('\n'.join(
            make_barcodes(args.length, args.stretch, args.distance, dfunc)))
        args.OUTPUT.write('\n')

    if args.subcommand == 'test':
        sys.stdout.write(
            '{} barcodes violate the distance contraint.\n'.format(
                test_barcodes(
                    list(map(lambda x: x.strip(), args.INPUT.readlines())),
                    args.distance, dfunc, args.output)))


if __name__ == '__main__':
    main()
