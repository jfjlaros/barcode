Library
=======

Barcode design via the library is done in three steps. First obtain the
full set of permutations with the ``all_barcodes`` function:

.. code:: python

   >>> from barcode import all_barcodes, filter_distance, filter_stretches
   >>>
   >>> # Generate all barcodes of length 2.
   >>> all_barcodes(2)
   ['AA', 'AC', 'AG', 'AT', 'CA', 'CC', 'CG', 'CT', 'GA', 'GC', 'GG', 'GT', 'TA',
   'TC', 'TG', 'TT']

The resulting list can be filtered with the ``filter_distance`` and
``filter_stretches`` functions:

.. code:: python

   >>> # Filter all barcodes of length 3 for a minimal edit distance of 3.
   >>> filter_distance(all_barcodes(3), 3)
   ['AAA', 'CCC', 'GGG', 'TTT']
   >>>
   >>> # Filter all barcodes of lenght 2 for mononucleotide stretches of length
   >>> # longer than 1.
   >>> filter_stretches(all_barcodes(2), 1)
   ['AC', 'AG', 'AT', 'CA', 'CG', 'CT', 'GA', 'GC', 'GT', 'TA', 'TC', 'TG']

For the best result, apply the ``filter_stretches`` function before
applying the ``filter_distance`` function:

.. code:: python

   >>> # Make a set of barcodes of length 3, having no mononucleotide stretches
   >>> # and a minimum edit distance of 3.
   >>> filter_distance(filter_stretches(all_barcodes(3), 1), 3)
   ['ACA', 'CGC', 'GAG']
