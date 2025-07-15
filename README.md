# Crowd:

Crowd is a social network simulation framework which simplifies and fastens the process of developing agent-based models and simulations on networks. It is developed as a Python library, which also provides more advanced visualization through its graphical user interface. In this repository, you can find the source code of the Python library version of Crowd and prebuilt wheel file for simpler installation. 

Check out [Crowd's documentation](https://crowd.readthedocs.io/en/latest/) for more detailed explanations for installation, simulation setup, execution, and examples. 

## Steps to Set Up

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
git clone https://github.com/bilkent-sna/crowd
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

## Citation
Please cite the following paper if you use Crowd:
  ```
  @article{rende2025crowd,
     title={Crowd: A Social Network Simulation Framework},
     author={Rende, Ann Nedime Nese and Yilmaz, Tolga and Ulusoy, Ozgur},
     journal={IEEE Transactions on Computational Social Systems},
     year={2025},
     publisher={IEEE},
     doi={10.1109/TCSS.2025.3565377}
  }
  ```

### Related Repositories:
[Crowd GUI](https://github.com/bilkent-sna/crowd-ui/tree/main)

[Case studies Mesa implementations](https://github.com/neserende/mesa-case-studies)
