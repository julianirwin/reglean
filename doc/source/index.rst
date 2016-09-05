.. reglean documentation master file, created by
   sphinx-quickstart on Sat Aug 27 13:38:24 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Reglean
===================================

.. toctree::
   :maxdepth: 2
   :caption: Table of Contents

  reglean

Reglean is a tiny module that simplifies the extraction of metadata from 
filenames.

I often give haphazard but descriptive filenames to my datafiles while working
in the lab. For example ``run3_100khz_tc=10_4.7K_new-method``. When I get 
around to analyzing the data with some script, I would like to automatically
glean the metainfo from this filename. Life is too short to give every datafile
highly organized xml fields for metainfo! Filenames are convenient and even
a new student on their first day understands how to descriptively name files!
This module seeks to provide a powerful, convenient and reusable method for
getting information from filenames into your python script.

Example
===================================
::

    from reglean import Gleaner
    wonky_filename = 'run3_100khz_tc=10_4.7K_new-method'
    gl = Gleaner(
      run='run(\d+)',
      freq='(\d+)khz',
      tc='tc=(\d+)',
      temp='_[\d\.]+K_',
      method='_(new|old)-method')
    gleaned = gl.glean(wonky_filename)
    # => {'run': '3', 'freq': '100', 'tc': '10', 'temp': '4.7', 'method': 'new'}
    # => {'freq': '100', 'method': 'new', 'temp': None, 'run': '3', 'tc': '10'}

Oh no!! We got ``'temp': None`` in the dictionary that was returned. What 
happened? Looks like the highly import parenthesis were left out::

      ...
      temp='_[\d\.]+K_',  # should be '_([\d\.]+)K_'
      ...

The parenthesis surround the piece of information that you want. The rest 
of the regex is just there to uniquely define where in the filename your
piece of information resides. If you give a gleaner a regex with more than 
one set of parenthesis::

      ...
      temp='_(\d)(\d)\.(\d)+K_'
      ...

The fields after the first set of parenthesis are ignored. So the above code
would give you ``{'temp': '4'}``.

This class is just a very simple application of the core ``re`` module. The
``re.search`` method is used to search the string given to ``glean()`` for
each of the patterns given to the ``Gleaner`` object as kwargs. Each call
of ``re.search`` results in a match object and the information between the
first set of parenthesis is grabbed with ``match.groups()[0]``.


Other Features
=================================

Translation
---------------------------------

It is common that the filename will have some abbreviation that you may
want to replace with a longer value upon gleaning. For example you may
want to change ``polarization=dn`` (where ``dn`` is the value) to ``down``. This
can be accomplished by adding a translation to the gleaner before ``glean()``
is called::


      g = Gleaner(cat1='...', cat2='...', cat3='...', ...)
      g.add_translation(category='cat1', value='foo', translation='bar'


Or with regular expression relacement analogour to the ``re.sub()`` method::

      g.add_translation(category='cat1', pattern='(\d+)deg', 
                        translation='\1\degreee')



Casting
---------------------------------

By default values are always strings because the filenames they are gleaned 
from are strings. If you want the values to show up as floats (or any other
type) instead you can use the ``cast_to`` parameter of ``add_category()``::


      g = Gleaner(cat1='...', cat2='...', cat3='...', ...)
      g.add_category('cat4', pattern='...', cast_to=float)

Then whatever value is matched by pattern will be passed to ``float`` before it
is returned by ``glean()``.


Filler Objects
---------------------------------

By default if a pattern for a certain category doesn't find a match in the 
string passed to ``glean()`` then ``'category': None`` is added to the ``dict``
return by ``glean()``. If you would rather some other value be the default, use
the ``fill_obj`` parameter of ``glean()``.




API Docs
==================

* :ref:`modindex`

