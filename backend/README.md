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
## Types of error, which API will return:

-------------------------------------
| Error code | Error message        |
|------------|----------------------|
|     400    | bad request          |
|     404    | resource not found   | 
|     405    | method not allowed   |  
|     422    | unprocessable entity |

## Endpoints

## `Get /categories `

* ### General
    * Get all categories

* ### Example
    * Request: ` curl http://127.0.0.1:5000/categories `
    * Response:
        ```json
        {
            "categories": {
                "1": "science",
                "2": "geography",
                "3": "sports",
                "4": "history",
                "5": "entertainment"
            },
            "success": true,
            "total_categories": 5
        }
        ```
* ### Errors 🐞
    * This endpoint doesn't give any errors

## ` POST /categories `

* ### General
    * Add new category
    * You should send request with ` POST ` method. Your request should include data about new category in JSON format
    * JSON data should include following parameteres:
    ---------------------------------------------
    |   | Parameter | Type   | Description      |
    |---|-----------|--------|------------------|
    | 1 | type      | String | Name of category |


* ### Example
    * Request:
        ```bash
        curl -X POST \
            -H "Content-Type: application/json" \
            -d '{
                "type": "Music"
            }' http://127.0.0.1:5000/categories
        ```
    * Response:
        ```json
            {
                "categories": {
                    "1": "science",
                    "2": "geography",
                    "3": "sports",
                    "4": "history",
                    "5": "entertainment",
                    "6": "Music"
                },
                "success": true,
                "total_categories": 6
            }   
        ```
* ### Errors 🐞
    * API raises error * 400 * if ` type ` parameter is empty or request body is empty
    * Example:
        * Request: 
            ```bash
            curl -X POST \
                -H "Content-Type: application/json" \
                -d '{
                    "type": ""
                }' http://127.0.0.1:5000/categories
            ``
        * Response:
            ```json
            {
                "error": 400,
                "message": "bad request",
                "success": false
            }
            ```
        * And if length of ` type ` parameter less than 3, API raises this error



## `Get /categories/<category_id>`

* ### General
    * Get category by id.
    * Category id is given in the URL parametres

* ### Example
    * Request: `curl http://127.0.0.1:5000/categories/1 `
    * Response:
        ```json
            {
                "category_id": 1,
                "category_type": "science",
                "success": true,
                "total_categories": 5
            }
        ```

* ### Errors 🐞
    * APIraises error *404* if category doesn't exists in database
    * Example:
        * Request: ` curl http://127.0.0.1:5000/categories/101010101010 `
        * Response:
            ```json
                {
                    "error": 404,
                    "message": "resource not found",
                    "success": false
                }
            ```

