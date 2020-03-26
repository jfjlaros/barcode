Usage
=====

The ``barcode`` program has two subcommands; one for the creation of a
set of barcodes and one for the validation of an existing set of
barcodes.

To make a set of barcodes and write this set to a file named
``barcodes.txt``, use the following command:

::

   barcode make barcodes.txt

``barcodes.txt`` will now contain a list of barcodes that all have
length 8, and no barcode will contain a mononucleotide stretch longer
than 2.

The length of the barcodes can be controlled with the ``-l`` parameter,
the minimum edit distance is controlled with the ``-d`` option and the
maximum mononucleotide stretch length can be set with the ``-s`` option.
So if we want to make a list of barcodes of length 10, a minimum edit
distance of 5 (allowing for the correction of 2 read errors) and a
maximum mononucleotide stretch of 1, we use the following command:

::

   barcode make -d 5 -l 10 -s 1 barcodes.txt

To verify a list of existing barcodes, use the command:

::

   barcode test barcode.txt

This will check the distance between any pair of barcodes and will tell
you how many barcodes violate the distance constraint. Again, the
minimum edit distance can be set with the ``-d`` parameter.

Additionally, a good set of barcodes can be extracted by providing an
output file via the ``-o`` option:

::

   barcode test -o good_barcodes.txt barcodes.txt
