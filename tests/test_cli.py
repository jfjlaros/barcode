"""
Tests for the barcode CLI.
"""
import Levenshtein

from barcode.cli import make_barcodes, test_barcodes as _test_barcodes


class TestCLI(object):
    def setup(self):
        pass #self._output = StringIO.StringIO()

    def test_make_barcodes_1(self):
        assert make_barcodes(2, 1, 1, Levenshtein.distance) == ['AC', 'AG',
            'AT', 'CA', 'CG', 'CT', 'GA', 'GC', 'GT', 'TA', 'TC', 'TG']

    def test_make_barcodes_2(self):
        assert make_barcodes(3, 1, 2, Levenshtein.distance) == ['ACA', 'AGC',
            'ATG', 'CAC', 'CGA', 'GAG', 'GCT', 'GTA', 'TAT', 'TCG']

    def test_barcodes_1(self):
        assert _test_barcodes(
            ['AAA', 'AAT', 'ATA'], 2, Levenshtein.distance, None) == 2

    def test_barcodes_2(self):
        assert _test_barcodes(
            ['AAA', 'AAT', 'ATC'], 2, Levenshtein.distance, None) == 1
