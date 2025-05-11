# etl-fintech-statistic
Mini ETL OJK Fintech statistic processor.


# CLONE REPO
    git clone -b main https://github.com/erric-syd/etl-fintech-statistic.git .


# VIRTUAL ENVIRONMENT
Membuat virtual env. untuk isolasi packages. Project ini menggunakan mkvirtualenv dan python 3.11.6.
## Tutorial install mkvirtualenv
https://www.geeksforgeeks.org/using-mkvirtualenv-to-create-new-virtual-environment-python/
## Tutorial install python untuk mkvirtualenv
Run di terminal:

    pyenv install --list | grep -E "3\.([7-9]|10|11)"
    pyenv install 3.11.6
## Create virtual env.
Run di terminal:

    mkvirtualenv etl_fintech_statistic_env -p ~/.pyenv/versions/3.11.6/bin/python

## Env. Variable
Menggunakan postgresql versi 16.0
````
DB_URL_PSQL=postgresql://salmoners@localhost/fdc_test
````


# REQUIREMENTS
    pip install -r requirements.txt