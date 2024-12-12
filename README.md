# Steps to Set Up

#### Option 1: Using Prebuilt Wheel:

1. Download the wheel file:

- Go to releases page of this repository and download the latest .whl file.

2. Go to the directory where .whl file is located
3. Run the following command:

```
  pip install name_of_wheel_file.whl
```

which for this release is:

```
 pip install crowd-0.9.0-py3-none-any.whl
```

4. Crowd now can be imported as a library or called from GUI.

#### Option 2: Installing with setup.py:

1. Clone or download the repository:

```
git clone https://github.com/Bilkent-Social-Systems-Research-Group/crowd
```

- Or download the code as a zip file, then extract it.

2. Run the following commands:

- Go to the folder where setup.py is placed:
  ```
    cd crowd
  ```
- Run setup.py
  ```
  python setup.py install
  ```
  Or for development:
  `python setup.py develop`
