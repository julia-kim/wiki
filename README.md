# wiki

**Wiki** is a Django app that allows users to search, create new, and edit existing encyclopedia entries. Entry files are stored locally. 

This was written for a CS50W project. Project specifications are [here](https://cs50.harvard.edu/web/2020/projects/1/wiki/).

![Wiki](https://imgur.com/dvujq4q)

## Installation
```cmd
:: Clone repo
git clone https://github.com/julia-kim/wiki.git

cd wiki

:: Setup and activate a virtual environment
python -m venv venv

venv\Scripts\activate.bat

:: Install all dependencies
pip install -r requirements.txt

:: Start up the application
python manage.py runserver
```