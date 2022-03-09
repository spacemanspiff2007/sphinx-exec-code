Installation and Configuration
==================================
To use this extension just add it to the ``extensions`` in your ``conf.py``

.. code-block::

   extensions = [
       'sphinx_exec_code',
   ]

Additionally the following configuration parameters are available:

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

If it's a relative path it will be resolved relative to the parent folder of the ``conf.py``

Example:

.. code-block::

   exec_code_working_dir = '..'
   exec_code_folders = ['../my_src']
   exec_code_example_dir = '.'

If you are unsure what the values are you can run Sphinx build in verbose mode with ``-v -v``.
The configured values are logged.

Log output for Example:

::

   [exec-code] Working dir: C:\Python\sphinx-exec-code
   [exec-code] Folders: C:\Python\sphinx-exec-code\my_src
   [exec-code] Example dir: C:\Python\sphinx-exec-code\doc
