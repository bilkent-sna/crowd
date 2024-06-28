# Steps to Set Up

- Clone the repository

```
git clone URL_OF_THIS_REPOSITORY.git
```

- (Optional) Create a virtual environment

```
python -m venv crowdenv
```

You can activate the virtual environment later.

```
source crowdenv/bin/activate
```

Once in the virtual environment, you can deactivate using the following:

```
deactivate
```

- To install the library and use it directly cd into it :

```
cd crowd
python setup.py install
```

- Or, use it in the development mode

```
cd crowd
python setup.py develop
```

- After installing, to run a test

```
cd examples/simpletest
python simpletest.py
```

- To use crowd (June 2024 version) as a library:

```
cd examples/crowd-library-test1
python lib_test.py
```
