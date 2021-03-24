
# Project Setup
1: Install virtualenv using pip
```
$ pip3 install virtualenv
```
2: From the project directory, create a new virtual environment for ths project and then activate.
```
$ virtualenv venv
$ source venv/bin/activate
```
3: Install project dependencies
```
$ pip3 install -r requirements.txt
```

# How-to-run
1. Make sure the source data is placed in the `data` directory
2. Run bash script
```
$ bash run_analysis.sh -t _ -n _
```
`_` is referred to argument. Run bash `run_analysis.sh --help` for further info.