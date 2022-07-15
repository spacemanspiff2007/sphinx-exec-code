Installation and Configuration
==================================

Installation
----------------------------------

.. code-block::

   pip install sphinx-exec-code



To use this extension just add it to the ``extensions`` in your ``conf.py``

.. code-block::

   extensions = [
       'sphinx_exec_code',
   ]

Configuration
----------------------------------

The following configuration parameters are available:

.. _config_options:

.. list-table::
   :widths: auto
   :header-rows: 1

   * - Name
     - Type
     - Description

   * - ``exec_code_working_dir``
     - ``Path`` or ``str``
     - The working directory where the code will be executed.

   * - ``exec_code_folders``
     - | ``List`` of
       | ``Path`` or ``str``
     - | Additional folders that will be added to PYTHONPATH.
       | Use this to e.g. make imports available.

   * - ``exec_code_example_dir``
     - ``Path`` or ``str``
     - | The directory that is used to create the path to the
       | example files. Defaults to the parent folder of the ``conf.py``.

   * - ``exec_code_stdout_encoding``
     - ``str``
     - | Encoding used to decode stdout.
       | The default depends on the operating system but should be ``utf-8``.


If it's a relative path it will be resolved relative to the parent folder of the ``conf.py``

Example:

.. code-block:: python

   exec_code_working_dir = '..'
   exec_code_folders = ['../my_src']
   exec_code_example_dir = '.'

If you are unsure what the values are you can run Sphinx build in verbose mode with ``-v -v``.
The configured values are logged.

Log output for Example:

.. code-block:: text

   [exec-code] Working dir: C:\Python\sphinx-exec-code
   [exec-code] Folders: C:\Python\sphinx-exec-code\my_src
   [exec-code] Example dir: C:\Python\sphinx-exec-code\doc
   [exec-code] Stdout encoding: utf-8
