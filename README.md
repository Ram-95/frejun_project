# Steps to setup, install and test the application.

- Download all the files from this repository.
- Install PostgreSQL (version: 14) and Redis.
- First install all the required modules from ```requirements.txt```
    ```
    pip install -r requirements.txt
    ```
- Dump all the data to Postgres DB from ```fre_jun.sql```.
- Navigate to the main project directory (```frejun_project```) and Apply all the migrations by using the following commands.
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
- To start the application use the following command
    ```
    python manage.py runserver
    ```
- To run all the Unit Tests for this application, run the following command
    ```
    python manage.py test
    ```
