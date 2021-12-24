# Steps to setup, run and test the application.

- Download all the files from this repository.
- Install PostgreSQL (version: 14) and Redis.
- First install all the required modules from ```requirements.txt``` by running the following command
    ```
    pip install -r requirements.txt
    ```
- Create a DB in Postgres with name ```frejun``` and Dump all the data from ```fre_jun.sql``` to it. Add the following DB details to ```settings.py```
    ```
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'frejun',
        'USER': 'postgres',
        'PASSWORD': 'homedb',
        'HOST': 'localhost',
        'PORT': '5432',
        }
    }
    ```

- Navigate to the main project directory (```frejun_project```) and Apply all the migrations by using the following commands.
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
- #### To start the application use the following command
    ```
    python manage.py runserver
    ```
- #### To run all the Unit Tests for this application, run the following command
    ```
    python manage.py test
    ```
