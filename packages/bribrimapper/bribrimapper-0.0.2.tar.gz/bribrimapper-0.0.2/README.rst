Bribri Mapper
=============

Bribri Mapper is a Python library that provides identification and conversion
functions for Bribri text processing. It is based on the `dragonmapper`_ PyPI package.
This was created for Dartmouth LING 48 with Professor Coto-Solano. It is not being actively maintained, however I would welcome any contributions or change requests.

GitHub: `https://github.com/isabellahoch/bribrimapper`_
Free software: MIT license

Features
--------

- Explicitly convert a Bribri string into the International Phonetic Alphabet (IPA)
- Explicitly transcribe Bribri tones

.. code-block:: python

    >>> s = "e'tã ie' ẽ' tkèsẽ kũlũk , kóxlĩ kiök"
    >>> bribrimapper.bribri_to_ipa(s)
    "e2tã ie2 ẽ2 tke1sẽ kũlũk , kõ4lĩ kiök"
    >>> bribrimapper.transcribe_bribri_tones(s)
    "e˩˧tã ie˩˧ ẽ˩˧ tke˧sẽ kũlũk , kõ˥˧lĩ kiök"

Getting Started
---------------

- `Install Bribri Mapper <https://isabellahoch.github.io/bribrimapper/installation.html>`_
- Report bugs and ask questions via `GitHub Issues <https://github.com/isabellahoch/bribrimapper>`_
- Contribute documentation, code, or feedback

.. _dragonmapper: https://github.com/tsroten/dragonmapper
.. _https://github.com/isabellahoch/bribrimapper: https://github.com/isabellahoch/bribrimapper