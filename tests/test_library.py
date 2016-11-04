"""
Tests for the barcode library.
"""
from barcode import all_barcodes, filter_distance, filter_stretches


class TestLibrary(object):
    def test_all_barcodes_1(self):
        assert all_barcodes(2) == ['AA', 'AC', 'AG', 'AT', 'CA', 'CC', 'CG',
            'CT', 'GA', 'GC', 'GG', 'GT', 'TA', 'TC', 'TG', 'TT']

    def test_all_barcodes_2(self):
        assert len(all_barcodes(3)) == 4 ** 3

    def test_all_barcodes_3(self):
        assert len(all_barcodes(4)) == 4 ** 4

    def test_all_barcodes_3(self):
        assert len(all_barcodes(5)) == 4 ** 5

    def test_filter_distance_1(self):
        assert filter_distance(all_barcodes(2), 2) == ['AA', 'CC', 'GG', 'TT']

    def test_filter_distance_2(self):
        assert filter_distance(all_barcodes(2), 3) == ['AA']

    def test_filter_distance_3(self):
        assert len(filter_distance(all_barcodes(4), 2)) == 64

    def test_filter_distance_4(self):
        assert len(filter_distance(all_barcodes(4), 3)) == 12

    def test_filter_distance_5(self):
        assert len(filter_distance(all_barcodes(5), 2)) == 256

    def test_filter_distance_6(self):
        assert len(filter_distance(all_barcodes(5), 3)) == 36

    def test_filter_stretches_1(self):
        assert filter_stretches(all_barcodes(2), 1) == ['AC', 'AG', 'AT', 'CA',
            'CG', 'CT', 'GA', 'GC', 'GT', 'TA', 'TC', 'TG']

    def test_filter_stretches_2(self):
        assert len(filter_stretches(all_barcodes(3), 1)) == 36

    def test_filter_stretches_3(self):
        assert len(filter_stretches(all_barcodes(3), 2)) == 60

    def test_filter_stretches_4(self):
        assert len(filter_stretches(all_barcodes(4), 1)) == 108

    def test_filter_stretches_5(self):
        assert len(filter_stretches(all_barcodes(4), 2)) == 228
