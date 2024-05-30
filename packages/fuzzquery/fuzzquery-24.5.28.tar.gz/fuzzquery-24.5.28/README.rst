fuzzquery 24.5.28
=================

**fuzzquery** is a lightweight package for fuzzy word/phrase searches in a body of text. Tokens are used to determine the number and type of approximations that can be made at a token’s position, within your query.

Installation
------------

To install ``fuzzquery`` use the following command-line: 

.. code-block:: console

  pip install fuzzquery

Documentation
-------------

The official documents can be viewed at `readthedocs <https://fuzzquery.readthedocs.io/>`_.
A version of documents can be viewed by calling python's built-in ``help`` function on any part of the **fuzzquery** package. 

Examples
--------

finditer
++++++++

.. code-block:: python

  import fuzzquery as fq

  data = """ 
  I would classify music as one of my favorite hobbies. 
  I love classical music played by classy musicians for a classic musical. 
  Beethoven can not be out-classed, music-wise - a man of class, musically gifted.
  """
  query = 'class{4} music{5}'
  
  print(f'\n{query.upper()} using skip')
  for span, match in fq.finditer(data, query, skip=('classify', ','), ci=True):
      print(f'  {match}')
      
  print(f'\n{query.upper()} no skip')
  for span, match in fq.finditer(data, query, ci=True):
      print(f'  {match}')

**output:**

.. code-block:: console

  CLASS{4} MUSIC{5}
    classify music
    classical music
    classy musicians
    classic musical
    classed, music-wise
    class, musically

  CLASS{4} MUSIC{5} with skip
    classical music
    classy musicians
    classic musical

iterall
+++++++

.. code-block:: python

  import fuzzquery as fq
  
  data = """ 
  I headed homeward to meet with the Wardens. 
  When I arrived, I was greeted by a homely man that told me the homestead was awarded 5 million dollars.
  We intend to use some of the homage to create a homeless ward. 
  The first piece of furniture will be my late-friend Homer's wardrobe.
  """
  
  queries = ('home{5}', 
             'home{4} ward{4}', 
             '{1}ward{=2}{2}', 
             'hom{6} {4w} wa{=1}{5}')
  
  for query, span, match in fq.iterall(data, queries, ci=True):
      if query: print(f'\n{query.upper()}')
      print(f'  {match}')

**output:**

.. code-block:: console

  HOME{5}
    homeward
    homely
    homestead
    homeless
    Homer's
  
  HOME{4} WARD{4}
    homeless ward
    Homer's wardrobe
  
  {1}WARD{=2}{2}
    Wardens
    awarded
    wardrobe
  
  HOM{6} {4W} WA{=1}{5}
    homeward to meet with the Wardens
    homestead was
    homage to create a homeless ward
    Homer's wardrobe
