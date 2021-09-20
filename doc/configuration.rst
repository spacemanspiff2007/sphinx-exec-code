Installation and Configuration
==================================
To use this extension just add it to the ``extensions`` in your ``conf.py``

.. code-block::

   extensions = [
       'sphinx_exec_code',
   ]

Additionally the following configuration parameters are available:

.. list-table::
   :widths: auto
   :header-rows: 1

   * - Name
     - Type
     - Description

   * - ``exec_code_working_dir``
     - ``Path`` or ``str``
     - The working directory where the code will be executed

   * - ``exec_code_folders``
     - | ``List`` of
       | ``Path`` or ``str``
     - | Additional folders that will be added to PYTHONPATH.
       | Use this to e.g. make imports available

If it's a relative path it will be resolved relative to the parent folder of the ``conf.py``

Example:

.. code-block::

   exec_code_working_dir = '..'
   exec_code_folders = ['../my_src']

If you are unsure what the values are you can run Sphinx build in verbose mode with ``-v -v``.
The configured values are logged.

Log output for Example:

::

   [exec-code] Working dir: C:\Python\sphinx-exec-code
   [exec-code] Folders: C:\Python\sphinx-exec-code\my_src
