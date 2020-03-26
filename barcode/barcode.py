import Levenshtein


_nucleotides = ['A', 'C', 'G', 'T']


def _all_words(bucket, word, length, result):
    """Generate all possible words of a certain length over a specified
    alphabet.

    :arg list bucket: An alphabet.
    :arg str word: A word over the alphabet {bucket}.
    :arg int length: Lenth of the barcodes.
    :arg list result: Constructed words.
    """
    if length:
        for i in bucket:
            _all_words(bucket, word + i, length - 1, result)
    else:
        result.append(word)


def _filter_stretch(barcode, stretches):
    """Test whether {barcode} contains none of the stretches in {stretches}.

    :arg str barcode: A barcode.
    :arg list stretches:

    :returns bool: True if the barcode is clean, False otherwise.
    """
    for i in stretches:
        if i in barcode:
            return False

    return True


def _filter_distance(barcodes, candidate, min_dist, distance):
    """Test whether {candidate} can be added to {barcodes} based on the minimum
    distance between {candidate} and all barcodes in {barcodes}.

    :arg list barcodes: List of barcodes.
    :arg str candidate: Candidate barcode.
    :arg int min_dist: Minimum distance between the barcodes.
    :arg function distance: Distance function.

    :returns bool: True if the barcode is clean, False otherwise.
    """
    for i in barcodes:
        if distance(i, candidate) < min_dist:
            return False

    return True


def all_barcodes(length):
    """Generate all possible barcodes of a certain length.

    :arg int length: Lenth of the barcodes.

    :returns list: List of barcodes.
    """
    result = []

    _all_words(_nucleotides, '', length, result)

    return result


def filter_stretches(barcodes, max_stretch):
    """Filter a list of barcodes for mononucleotide stretches.

    :arg list barcodes: List of barcodes.
    :arg int max_stretch: Maximum mononucleotide stretch length.

    :returns list: List of barcodes filtered for mononucleotide stretches.
    """
    stretches = list(map(lambda x: (max_stretch + 1) * x, _nucleotides))
    result = []

    for i in barcodes:
        if _filter_stretch(i, stretches):
            result.append(i)

    return result


def filter_distance(barcodes, min_dist, distance=Levenshtein.distance):
    """Filter a list of barcodes for distance to other barcodes.

    :arg list barcodes: List of barcodes.
    :arg int min_dist: Minimum distance between the barcodes.
    :arg function distance: Distance function.

    :returns list: List of barcodes filtered for distance to other
        barcodes.
    """
    result = []

    for i in barcodes:
        if _filter_distance(result, i, min_dist, distance):
            result.append(i)

    return result
