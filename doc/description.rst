
Usage
==================================

Without options
------------------------------
.. code-block:: python

   .. exec_code::

      print('Easy!')

Generated view

----

.. exec_code::

    print('Easy!')

----

Options
------------------------------
It's possible to further configure both the code block and the output block with the following options:
`See sphinx docs <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code>`_
for a detailed description

hide/hide_output:
  Will hide the corresponding block
name/name_output
  Define implicit target name that can be referenced by using ref
caption/caption_output
  Will add a caption above the block
linenos/linenos_output
  Will add line numbers
lineno-start/lineno-start_output
  Set the first line number of the block. Linenos is also automatically activated
emphasize-lines/emphasize-lines_output
  Emphasize particular lines of the block
language/language_output:
  | Will add syntax highlighting for the specified language
  | The default for the code block is python, the default for the output block is plain text


Example:

.. code-block:: python

   .. exec_code::
      :linenos:
      :hide_output:
      :caption: This is an important caption

      print('Easy!')

Generated view

----

.. exec_code::
  :linenos:
  :hide_output:
  :caption: This is an important caption

    print('Easy!')

----

Code from files
------------------------------
It's possible to have code in example files with the ``filename`` option.
The folder that is used to resolve to a file name can be :ref:`configured <config_options>`.

Example:

.. code-block:: python

   .. exec_code::
      :filename: file_example.py


Generated view

----

.. exec_code::
   :filename: file_example.py

----

Code Markers
------------------------------
It's possible to hide parts of the code (e.g. to setup a working example)
and it's possible to skip part of the code execution. This is possible with the
``#hide:[start|stop|toggle]`` or ``#skip:[start|stop|toggle]`` marker in the code.
Empty lines after a disabling marker will be ignored.

Spaces and dashes are ignored for the case insensitive marker detection so these are all the same:

.. code-block:: python

   #HIDE:START
   # hide: start
   # ----- hide: start -----
        # ----- hide: start -----


Hiding code parts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

   .. exec_code::

      # --- hide: start ---
      print('Setup!')
      #hide:toggle

      print('Easy!')

      # --- hide: start ---
      print('Hidden!')
      # --- hide: stop ---

      # Note the missing entries!
      print('Visible!')


Generated view (note the skipped empty lines after the stop and disabling toggle marker)

----

.. exec_code::

   # --- hide: start ---
   print('Setup!')
   #hide:toggle

   print('Easy!')

   # --- hide: start ---
   print('Hidden!')
   # --- hide: stop ---

   # Note the missing entries!
   print('Visible!')

----

Skipping code parts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

   .. exec_code::

      # --- skip: start ---
      print(f'1 / 0 = {1 / 0}')
      # --- skip: stop ---

      # --- hide: start ---
      print('1 / 0 = 0')
      # --- hide: stop ---

Generated view

----

 .. exec_code::

    # --- skip: start ---
    print(f'1 / 0 = {1 / 0}')
    # --- skip: stop ---

    # --- hide: start ---
    print('1 / 0 = 0')
    # --- hide: stop ---

----

With the combination of ``skip`` and ``hide`` it's possible to "simulate" every code.


Further Examples
------------------------------

This is an example with captions, highlights and name.


.. code-block:: python

   .. exec_code::
      :lineno-start: 5
      :emphasize-lines: 1, 4
      :caption: This is an important caption
      :caption_output: This is an important output caption
      :name: my_example_1
      :name_output: my_output_1

      print('My')
      # This is a comment

      print('Output!')

Generated view

----

.. exec_code::
   :lineno-start: 5
   :emphasize-lines: 1, 4
   :caption: This is an important caption
   :caption_output: This is an important output caption
   :name: my_example_1
   :name_output: my_output_1

   print('My')
   # This is a comment

   print('Output!')

----

Create a link using to the blocks by using the name:

.. code-block:: text

    See :ref:`this code snippet <my_example_1>` for an example
    See :ref:`this code snippet <my_output_1>` for an example output

See :ref:`this code snippet <my_example_1>` for an example
See :ref:`this code snippet <my_output_1>` for an example output
