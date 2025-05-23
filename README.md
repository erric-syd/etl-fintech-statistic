# etl-fintech-statistic
Mini ETL OJK Fintech statistic processor.

## Tech Stack
- MacOS
- python 3.11.6
- Postgresql 16

## Step-by-step
1. Buat folder di local dan clone repo nya
2. Buat virtual environment
3. Input environment variables di virtual env. nya
4. Buat database postgresql di local 
5. Install requirements
6. Run main.py
```
python main.py

DB_URL_PSQL=postgresql://salmoners@localhost/fdc_test python main.py
```

# CLONE REPO
    git clone -b main https://github.com/erric-syd/etl-fintech-statistic.git .


# VIRTUAL ENVIRONMENT
Membuat virtual env. untuk isolasi packages. Project ini menggunakan mkvirtualenv.
## Tutorial install mkvirtualenv
[mkvirtualenv python](https://www.geeksforgeeks.org/using-mkvirtualenv-to-create-new-virtual-environment-python/)
## Tutorial install python untuk mkvirtualenv
Run di terminal:

    pyenv install --list | grep -E "3\.([7-9]|10|11)"
    pyenv install 3.11.6
## Create virtual env.
Run di terminal:

    mkvirtualenv etl_fintech_statistic_env -p ~/.pyenv/versions/3.11.6/bin/python

## Env. Variable
````
DB_URL_PSQL=postgresql://salmoners@localhost/fdc_test
````


# REQUIREMENTS
    pip install -r requirements.txt


# VISUALIZATIONS
On main.py, True: Enable viz, False: Disable viz

    enable_visualization = [True / False]
## Handling socket.error: [Errno 48] Address already in use
You can find the process using the port (e.g., port 8080) with this command:
    
    lsof -i :8080

This will show you the PID (Process ID). Then, you can kill the process:

    kill -9 <PID>
