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

<br>
<br>

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
    * API raises error **400** if ` type ` parameter is empty or request body is empty
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

<br>
<br>

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
    * API raises error **404** if category doesn't exists in database
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

<br>
<br>

## ` PATCH /categories/<category_id> `

* ## General
    * Update category with id. Id given in URL parameteres
    * You can update only ` type ` parameter of category
    * You should send request with ` PATCH ` method. Your request should include data about updated parameter of category in JSON format
    * JSON data should include following parameteres:
    ---------------------------------------------
    |   | Parameter | Type   | Description      |
    |---|-----------|--------|------------------|
    | 1 | type      | String | Name of category |

* ## Example
    * Request:

            ```bash
            curl -X PATCH \
                -H "Content-Type: application/json" \
                -d '{
                    "type": "Deep Learning"
                }' http://127.0.0.1:5000/categories
            ``
    * Response:
        ```json
        {
            "success": true,
            "updated_category_id": 7
        }
        ```
    * Before request ` type ` of category with id 7 was *Machine Learning*, after request it was changed to *Deep Learning*

* ### Errors 🐞
    * API raises error **400** if ` type ` parameter is empty or request body is empty
    * Example:
        * Request: 
            ```bash
            curl -X PATCH \
                -H "Content-Type: application/json" \
                -d '{
                    "type": ""
                }' http://127.0.0.1:5000/categories/7
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

<br>
<br>

## ` DELETE /categories/<category_id> `

* ## General
    * Delete category with id. ID given in URL parameters

* ## Example
    * Request: ` curl -X DELETE http://127.0.0.1:5000/categories/7 `
    * Response:
        ```json
        {
            "deleted_category_id": 7,
            "success": true
        }
        ```

* ### Errors 🐞
    * If category doesn't exists in database, API returns **404** eror
    * Request: ` curl -X DELETE http://127.0.0.1:5000/categories/72342324 `
    * Response:
        ```json
        {
            "error": 400,
            "message": "bad request",
            "success": false
        }
        ```
        * And if deleting was unsuccessful, API returns **422** error

<br>
<br>

## ` GET /questions `

* ## General
    * Get all questions
    * Results are paginated in groups of 8. Include an URL parameter to choose page, starting from 1
    * If not questions, and page not equals to 1, API raises error **404**

* ## Example
    * Request: ` curl http://127.0.0.1:5000/questions `
    * Response:
        ```json
        {
            "categories": {
                "1": "science",
                "2": "art",
                "3": "Geography",
                "4": "History",
                "5": "Entertainment",
                "6": "Sports"
            },
            "questions": [
                {
                    "answer": "Blood",
                    "category": "science",
                    "category_id": 1,
                    "difficulty": 4,
                    "id": 1,
                    "question": "Hematology is a branch of medicine involving the study of what?"
                },
                {
                    "answer": "The Palace of Versailles",
                    "category": "Geography",
                    "category_id": 3,
                    "difficulty": 3,
                    "id": 2,
                    "question": "In which royal palace would you find the Hall of Mirrors?"
                },
                {
                    "answer": "George Washington Carver",
                    "category": "History",
                    "category_id": 4,
                    "difficulty": 2,
                    "id": 3,
                    "question": "Who invented Peanut Butter?"
                }
            ],
            "success": true,
            "total_questions": 3
        }       
        ```

* ### Errors 🐞
    * If not questions, and page not equals to 1, API raises error **404**

<br>
<br>

## ` GET /categories/<category_id>/questions `

* ### General
    * Get all questions by category id. Category ID given in URL parameters

* ### Example
    * Request: ` curl http://127.0.0.1:5000/categories/1/questions `
    * Response:
        ```json
        {
            "current_category": "science",
            "questions": [
                {
                    "answer": "Blood",
                    "category": "science",
                    "category_id": 1,
                    "difficulty": 4,
                    "id": 1,
                    "question": "Hematology is a branch of medicine involving the study of what?"
                }
            ],
            "success": true,
            "total_questions": 8
        }
        ```
* ### Errors 🐞
    * If category with given id in URL doesn't exists in database, API raises **404** error
    * Example:
        * Request: ` curl http://127.0.0.1:5000/categories/21323123/questions `
        * Response:
            ```json
            {
                "error": 404,
                "message": "resource not found",
                "success": false
            }
            ```

<br>
<br>

## ` POST /questions `

* ### General
    * Add new question
    * You should send request with ` POST ` method. Your request should include data about new question in JSON format
    * JSON data should include following parameteres:
    ----------------------------------------------------------------------------
    |   | Parameter  | Type   | Description                                    |
    |---|------------|--------|------------------------------------------------|
    | 1 | questions  | String | Question of new question                       |
    | 2 | answer     | String | Answer of question                             |
    | 3 | difficulty | Number | Difficulty of question(optional), by default 1 |
    | 4 | category   | Number | Id of category                                 |


* ### Example
    * Request:
        ```bash
        curl -X POST \
            -H "Content-Type: application/json" \
            -d '{
                "question": "The Taj Mahal is located in which Indian city?",
                "answer": "Agra",
                "difficulty": "2",
                "category": "3"
            }' http://127.0.0.1:5000/questions
        ```
    * Response:
        ```json
        {
            "created": 4,
            "success": true
        }
        ```
* ### Errors 🐞
    * API raises error **400**:
        1. If ` question ` parameter is empty or length less than 5
        2. If ` difficulty ` parameter is empty, or not a number
        3. If ` category ` parameter is empty, or not a number or not exists in database
        4. If request body is empty 

    * Example:
        * Request: 
            ```bash
            curl -X POST \
                -H "Content-Type: application/json" \
                -d '{
                    "question": "Lorem",
                    "answer": "ipsum",
                    "difficulty": "should be number",
                    "category": "21221223231231"
                }' http://127.0.0.1:5000/questions
            ``
        * In this request 
            1. ` question` parameter violates required length
            2. ` difficulty ` parameter violates required type
            3. ` category ` parameter not exists in database

        * Response:
            ```json
            {
                "error": 400,
                "message": "bad request",
                "success": false
            }
            ```

<br>
<br>

## ` GET /questions/8 `

* ### General
    * Get individual question with question id. Question id is given in the URL parameters

* ### Example
    * Request: ` http://127.0.0.1:5000/questions/8 `
    * Response:
        ```json
        {
            "answer": "Escher",
            "category": "art",
            "category_id": 2,
            "difficulty": 1,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?",
            "question_id": 8,
            "success": true,
            "total_questions": 8
        }
        ```

* ### Errors 🐞
    * If question with given id in URL doesn't exists in database, API raises **404** error
    * Example:
        * Request: ` http://127.0.0.1:5000/questions/1111112222 `
        * Response:
            ```json
            {
                "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?",
                "answer": "Escher",
                "difficulty": "1",
                "category": "2" 
            }            
            ``` 
