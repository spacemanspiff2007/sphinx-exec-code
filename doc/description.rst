
Usage
==================================

Without options
------------------------------
.. code-block:: rst

   .. exec_code::

      print('Easy!')

Generated view:

.. exec_code::

    print('Easy!')

Options
------------------------------
It's possible to further configure both the code block and the output block with the following options:


hide_code/hide_output:
  Will hide the corresponding block
caption/caption_output
  Will add a caption above the block
linenos/linenos_output
  Will add line numbers
language/language_output:
  | Will add syntax highlighting for the specified language
  | The default for the code block is python, the default for the output block is plain text


Example:

.. code-block:: rst

   .. exec_code::
      :linenos:
      :hide_output:
      :caption: This is an important caption

      print('Easy!')

Generated view:

.. exec_code::
  :linenos:
  :hide_output:
  :caption: This is an important caption

  print('Easy!')


Hide code parts
------------------------------
It's possible to hide parts of the code (e.g. to setup a working example)
and it's possible to skip part of the code execution. This is possible with the
``#hide:[start|stop|toggle]`` or ``#skip:[start|stop|toggle]`` marker in the code.

Spaces and dashes are ignored for the case insensitive marker detection so these are all the same:

.. code-block:: python

   #HIDE:START
   # hide: start
   # ----- hide: start -----
        # ----- hide: start -----


Example:

.. code-block:: rst

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


Generated view:

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
