# Barcode: Design NGS barcodes
Barcode is a program for the design and validation of sets of barcodes.

Barcodes are used in NGS to tag samples before pooling. After sequencing, these
barcodes are used to *demultiplex* the data, thereby assigning the reads to the
originating sample.

The key aspect of a good set of barcodes is robustness against read errors. One
read error should not be able to transform one barcode into another. This
requirement can be met by selecting barcodes in such a way that the *edit
distance* between any pair of barcodes is larger than one. An additional
desired property is the ability to *correct* read errors. This can be done by
increasing the minimal edit distance between barcodes to at least three. If one
read error occurs, the sequenced barcode will have a distance of one to the
original barcode and a minimum distance of two to any of the other barcodes. If
the read error is high, the minimum edit distance should be increased to a
higher (odd) number.

For some sequencers it is important that mononucleotide stretches in barcodes
are below a minimum length. An additional filter can be used to remove these
barcodes.

Development of Barcode is hosted
[on our GitLab server](https://git.lumc.nl/j.f.j.laros/barcode).


## Easy installation
If you have installed the `pip` package installer, you can easily install
Barcode by typing:

    pip install barcode


## Installing from source
To install from the source repository, use:

    git clone https://git.lumc.nl/j.f.j.laros/barcode.git
    cd barcode
    pip install .


## Usage
The `barcode` program has two subcommands; one for the creation of a set of
barcodes and one for the validation of an existing set of barcodes.

To make a set of barcodes and write this set to a file named `barcodes.txt`,
use the following command:

    barcode make barcodes.txt

`barcodes.txt` will now contain a list of barcodes that all have length 8, and
no barcode will contain a mononucleotide stretch longer than 2.

The length of the barcodes can be controlled with the `-l` parameter, the
minimum edit distance is controlled with the `-d` option and the maximum
mononucleotide stretch length can be set with the `-s` option. So if we want to
make a list of barcodes of length 10, a minimum edit distance of 5 (allowing
for the correction of 2 read errors) and a maximum mononucleotide stretch of 1,
we use the following command:

    barcode make -d 5 -l 10 -s 1 barcodes.txt

To verify a list of existing barcodes, use the command:

    barcode test barcode.txt

This will check the distance between any pair of barcodes and will tell you how
many barcodes violate the distance constraint. Again, the minimum edit distance
can be set with the `-d` parameter.

Additionally, a good set of barcodes can be extracted by providing an output
file via the `-o` option:

    barcode test -o good_barcodes.txt barcodes.txt


## Library usage
Barcode design via the library is done in three steps. First obtain the full
set of permutations with the `all_barcodes` function:

```python
>>> from barcode import all_barcodes, filter_distance, filter_stretches
>>>
>>> # Generate all barcodes of length 2.
>>> all_barcodes(2)
['AA', 'AC', 'AG', 'AT', 'CA', 'CC', 'CG', 'CT', 'GA', 'GC', 'GG', 'GT', 'TA',
'TC', 'TG', 'TT']
```

The resulting list can be filtered with the `filter_distance` and
`filter_stretches` functions:

```python
>>> # Filter all barcodes of length 3 for a minimal edit distance of 3.
>>> filter_distance(all_barcodes(3), 3)
['AAA', 'CCC', 'GGG', 'TTT']
>>>
>>> # Filter all barcodes of lenght 2 for mononucleotide stretches of length
>>> # longer than 1.
>>> filter_stretches(all_barcodes(2), 1)
['AC', 'AG', 'AT', 'CA', 'CG', 'CT', 'GA', 'GC', 'GT', 'TA', 'TC', 'TG']
```

For the best result, apply the `filter_stretches` function before applying the
`filter_distance` function:

```python
>>> # Make a set of barcodes of length 3, having no mononucleotide stretches
>>> # and a minimum edit distance of 3.
>>> filter_distance(filter_stretches(all_barcodes(3), 1), 3)
['ACA', 'CGC', 'GAG']
```
