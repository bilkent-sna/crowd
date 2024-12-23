Installing Crowd
====================

**Prerequisites**

Python 3.12 must be installed on your system. If not, follow these steps to install it:

- Visit the official `Python downloads page <https://www.python.org/downloads/>`_.

- Download the installer for Python 3.12 suitable for your operating system.
- Run the installer and ensure you select the option Add Python to PATH during installation.

Python library
--------------
1. Navigate to the `Crowd GitHub repository <https://github.com/Bilkent-Social-Systems-Research-Group/crowd/>`_. 

    

**Option 1: Using Prebuilt Wheel**

2. Go to releases page of the repository and download the latest .whl file.
3. On your computer, go to the directory where .whl file is located
4. Run the following command:

.. code-block:: bash

   pip install name_of_wheel_file.whl

which for this release is:

.. code-block:: bash

 pip install crowd-0.9.0-py3-none-any.whl

5. Crowd now can be imported as a library or called from GUI.

**Option 2: Installing with setup.py**

2. Clone or download the repository:

.. code-block:: bash

    git clone https://github.com/Bilkent-Social-Systems-Research-Group/crowd
    
Or download the code as a zip file, then extract it.

3. Run the following commands:

- Go to the folder where setup.py is placed:

.. code-block:: bash

    cd crowd

- Run setup.py

.. code-block:: bash

    python setup.py install

- Or for development: 

.. code-block:: bash

    python setup.py develop


Note: For the users who prefer only using the Python library, desktop app is not required to be installed. 

Desktop app
-----------

1. Navigate to the releases page of the `Crowd UI repository <https://github.com/Bilkent-Social-Systems-Research-Group/crowd-ui/releases/>`_.  

2. Locate the latest release (v0.9.0) and download the installer. 

3. Run the installer and follow the on-screen instructions to complete the installation.

4. Once the installation is complete, you can start using Crowd's GUI to configure and run simulations:

    - Launch the Crowd app from your desktop or application menu.

    - Create your first project, configure simulation settings and run simulations.

For detailed usage and features, refer to the introduction section. 
