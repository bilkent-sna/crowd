Reading Network Info From Files
===============================

Network information can also be loaded from csv, txt and edgelist files. Configuration in the following format:

.. code-block:: yaml

    structure:
        file:
            type: 'nodes/nodes_edges'
            header:  True/False
            path: 'include-full-path-to-dataset-here'


**Next:** (Optional) Initalizing node types