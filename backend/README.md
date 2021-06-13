# Full Stack Trivia API Backend

## Getting Started

## Setup requirements

### Database
* Database which used:
---------------------------------
| database type | database name |
|---------------|---------------|
| Postgresql    | trivia        |
|---------------|---------------|
* To create database run following command:
```bash
     createdb trivia
```

## Run application
* Windows using Git Bash:
    ```bash
        cd backend
        python -m venv env
        source env/scripts/activate
        pip install -r requirements.txt
        export FLASK_APP=flaskr
        export FLASK_DEBUG=true
        flask run
    ```
* MacOS/Linux:
    ```bash
        cd backend
        python3 -m venv env
        source env/bin/activate
        pip install -r requirements.txt
        export FLASK_APP=flaskr
        export FLASK_DEBUG=true
        flask run
    ```
## Tests
To run tests, run the followinf commands:
```bash
    cd backend
    psql postgres
    drop database trivia_test;
    create database trivia_test;
    \q
    psql trivia_test < trivia.psql
    python test_flaskr.py
```

# API Reference

## Getting Started

* Base URL: At present this app can be run locally and it hosted by default. Default URL: ` http://127.0.0.1:5000 `
* Authentication: This versionof API does not require to API keys :)

* In documentation is used CURL to send requests, another most popular tool to send requests and test API is Postman.

## Error Handling
Error are returned as JSON objects in following format:
```json
    "error": <error_code>,
    "message": <error_message>,
    "success": false
```
Types of error, which API will return:
-------------------------------------
| Error code | Error message        |
-------------------------------------
|     400    | bad request          |
|     404    | resource not found   | 
|     405    | method not allowed   |  
|     422    | unprocessable entity |