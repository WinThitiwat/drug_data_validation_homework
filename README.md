# Project File
- `config.py` - a Python file containing constant variables
- `drug_enum.py` - a Python file containing ENUM for categorical data validation and reference
- `main.py` - the main Python file that receives and validate inputs, and trigger functions according to the input
- `metadata_analysis.py` - a Python file running analysis about Metadata
- `mic_analysis.py` - a Python file running analysis about MIC
- `utils.py` - a Python file containing helper functions for other Python files 
- `requirements.txt` - a text file containing all mandatory dependencies for the project


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
1. Create `data` directory if not exist at the root project 
2. Make sure the source data is placed in the `data` directory that's just created
3. Run bash script
```
$ bash run_analysis.sh -t <..> -n <..>
```
`<..>` is referred to argument. Run `bash run_analysis.sh --help` for further information.
