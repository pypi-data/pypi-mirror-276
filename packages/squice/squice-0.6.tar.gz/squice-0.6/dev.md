# Create dev environments for both the app and the lib seperately

**Use the appropriate one for the dev work. Keep a seperation in your mind between the scientific library (lib) and the demonstration of it (app).**

# Virtual environments

## STREAMLIT APP
```
/bin/python3.12 -m venv .env-sq-app
## Load dev environment
source .env-sq-app/bin/activate
(deactivate to exit venv)
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

### run app
streamlit run app/home.py

## distribute to streamlit
This will be automatically distributed to streamlit on push to main
https://share.streamlit.io/

## Pypi library
```
/bin/python3.12 -m venv .env-sq-lib
## Load dev environment
source .env-sq-lib/bin/activate
(deactivate to exit venv)
pip install --upgrade pip
pip install -r requirements_lib.txt --upgrade
```

To install the lib locally while developing
```
pip install .
```

## Pre-commit

The pre-commit hook shyuld run on check in to format files as per standards.
```
pre-commit run --all-files
black ./ --check --line-length 88 --diff
black ./ --line-length 88
```
---

# Debugging

## A python file

## The streamlit app
