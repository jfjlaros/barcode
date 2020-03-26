Introduction
============

Barcodes are used in NGS to tag samples before pooling. After
sequencing, these barcodes are used to *demultiplex* the data, thereby
assigning the reads to the originating sample.

The key aspect of a good set of barcodes is robustness against read
errors. One read error should not be able to transform one barcode into
another. This requirement can be met by selecting barcodes in such a way
that the *edit distance* between any pair of barcodes is larger than
one. An additional desired property is the ability to *correct* read
errors. This can be done by increasing the minimal edit distance between
barcodes to at least three. If one read error occurs, the sequenced
barcode will have a distance of one to the original barcode and a
minimum distance of two to any of the other barcodes. If the read error
is high, the minimum edit distance should be increased to a higher (odd)
number.

For some sequencers it is important that mononucleotide stretches in
barcodes are below a minimum length. An additional filter can be used to
remove these barcodes.
