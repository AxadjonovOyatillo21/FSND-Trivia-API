# Full Stack Trivia API Backend

## Getting Started

## Setup requirements

### Database
* Database which used:
---------------------------------
| database type | database name |
|---------------|---------------|
| Postgresql    | trivia        |

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

## Errors Handling
Error are returned as JSON objects in following format:
```json
    "error": <error_code>,
    "message": <error_message>,
    "success": false
```
## Types of 
#, which API will return:

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
        1) If ` question ` parameter is empty or length less than 5
        2) If ` difficulty ` parameter is empty, or not a number
        3) If ` category ` parameter is empty, or not a number or not exists in database
        4) If request body is empty 

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
            1) ` question` parameter violates required length
            2) ` difficulty ` parameter violates required type
            3) ` category ` parameter not exists in database

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

## ` GET /questions/<question_id> `

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

<br>
<br>

## ` PATCH /questions/<question_id> `

* ### General
    * Update individual question with question id. Question id is given in the URL parameters
    * You can update only ` question `, ` answer `, ` difficulty ` or ` category ` parameter of category
    * You should send request with ` PATCH ` method. Your request should include data about updated parameter of category in JSON format
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
        curl -X PATCH \
            -H "Content-Type: application/json" \
            -d '{
                "question": "Whose autobiography is entitled 'I Know Why the Caged Bir Sings'?",
                "answer": "Maya Angelou",
                "difficulty": "2",
                "category": 4
            }' http://127.0.0.1:5000/questions/6 
        ```

        * Response:
            ```json
            {
                "success": true,
                "updated_question_id": 6
            }
            ```
        * Before request:
            1) ` question ` parameter was *The Taj Mahal is located in which Indian city?*, after request it was changed to *"Whose autobiography is entitled 'I Know Why the Caged Bir Sings'?*
            2) ` answer ` parameter was *Agra*, after request  it was changed to *Maya Angelou*
            3) ` difficulty ` parameter was *1*, after request  it was changed to *2*
            4) ` category ` parameter was the category id *2*, after request  it was changed to category id of *History* category *4*
        
* ### Errors 🐞
    * API raises error **400**:
        1) If ` question ` parameter is empty or length less than 5
        2) If ` difficulty ` parameter is empty, or not a number
        3) If ` category ` parameter is empty, or not a number or not exists in database
        4) If request body is empty 

    * Example:
        * Request: 
            ```bash
            curl -X PATCH \
                -H "Content-Type: application/json" \
                -d '{
                    "question": "False",
                    "answer": "dolor",
                    "difficulty": "",
                    "category": "should be number"
                }' http://127.0.0.1:5000/questions
            ``
            
        * In this request 
            1) ` question` parameter violates required length
            2) ` difficulty ` parameter is empty
            3) ` category ` parameterviolates required type

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

## ` DELETE /questions/<question_id> `

* ## General
    * Delete question with id. ID given in URL parameters

* ## Example
    * Request: ` curl -X DELETE http://127.0.0.1:5000/questions/4 `
    * Response:
        ```json
        {
            "deleted_question_id": 4,
            "success": true
        }
        ```

* ### Errors 🐞
    * If question doesn't exists in database, API returns **404** eror
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

## ` POST /quizzes `

* ## General
    * Play and enjoy with Trivia quiz game😊
    * You should send request with ` POST ` method. Your request should include data about ` previous questions ` and ` quiz_category(dict object, which includes type and id of category) ` in JSON format
    * ` previous_questions ` is optional, if not previous_questions, if previous_questions exixsts, you should give list of id`s of previous_questions. 
        * Example format:
            ```json
            {
                "previous_questions": [1, 2, 7, 4]
            }
            ```
    * ` quiz_category ` is optional if ` quiz_category ` type is all, but, if ` quiz_category ` exists this parameter is very required!!! ` quiz_category ` is a dict object, which includes typ and id of category. 
        * Example format:
            ```json
            {
                "quiz_category": {
                    "type": "science",
                    "id": 1
                }
            }
            ```
    * To get all questions you shouldn't give ` previous_questions ` parameter or give ` previous_questions ` with empty array
    * To play game in all categories, you shouldn't give ` quiz_category ` parameter or give ` quiz_category ` parameter with ` type ` *click*, or ` id ` *0*
    * Warning: if ` quiz_category ` parameter exists, you should give ` id ` in ` quiz_category `, to get play in all categories give ` id ` equal to zero
    * JSON data should include following parameteres:
    -----------------------------------------------------------------------------------------------
    |   | Parameter              | Type         | Description                                     |
    |---|------------------------|--------------|-------------------------------------------------|
    | 1 | previous_questions     | Array        | Array which includes id`s of previous_questions |
    | 2 | quiz_category          | Dict Object  | Array which includes id`s of previous_questions |
    * API returns random question which not in previous_questions :)
    * if in given category not any questions, api returns JSON data in following format:
        ```json
        {
            "previous_questions": [],
            "question": null,
            "success": true
        }
        ```
* ## Example
    * Get with category:
        * Request:
            ```bash
            curl -X POST \
                -H "Content-Type: application/json" \
                -d '{
                    "previous_questions": [1],
                    "quiz_category": {
                        "type": "science",
                        "id": "1"
                    }
                }' http://127.0.0.1:5000/quizzes
            ```
        * Response:
            ```json
            {
                "previous_questions": [
                    1
                ],
                "question": {
                    "answer": "Alexander Fleming",
                    "category": "science",
                    "category_id": 1,
                    "difficulty": 3,
                    "id": 9,
                    "question": "Who discovered penicillin?"
                },
                "quiz_category": 0,
                "success": true
            }
            ```
    * All categories:
        * Request:
            ```bash
            curl -X POST \
                -H "Content-Type: application/json" \
                -d '{
                    "previous_questions": [1, 9, 7],
                    "quiz_category": {
                        "type": "click",
                        "id": "0"
                    }
                }' http://127.0.0.1:5000/quizzes
            ```
        * Response:
            ```json
            {
                "previous_questions": [
                    1,
                    9,
                    7
                ],
                "question": {
                    "answer": "Escher",
                    "category": "art",
                    "category_id": 2,
                    "difficulty": 1,
                    "id": 8,
                    "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
                },
                "quiz_category": 0,
                "success": true
            }
            ```
        OR
        * Request:
            ```bash
            curl -X POST \
                -H "Content-Type: application/json" \
                -d '{
                    "previous_questions": [1, 9]
                }' http://127.0.0.1:5000/quizzes
            ```
        * Response:
            ```json
            {
                "previous_questions": [
                    1,
                    9
                ],
                "question": {
                    "answer": "Maya Angelou",
                    "category": "History",
                    "category_id": 4,
                    "difficulty": 2,
                    "id": 6,
                    "question": "Whose autobiography is entitled 'I Know Why the Caged Bir Sings'?"
                },
                "quiz_category": 0,
                "success": true
            }
            ```
    
* ### Errors 🐞
    * API raises **400** error if:
        1) If request body is empty
        2) If in ` quiz_category ` parameter *id* is empty or string, and or doesn't exists in database
        3) If in ` previous_question ` given not id 
    * Example:
        * 1 - category with given id doesn't exists:
            * Request:
                ```bash
                curl -X POST \
                    -H "Content-Type: application/json" \
                    -d '{
                        "previous_questions": [1, 9, 7],
                        "quiz_category": {
                            "type": "click",
                            "id": "123213232311232"
                        }
                    }' http://127.0.0.1:5000/quizzes
                ```
            * Response:
                ```json
                {
                    "error": 400,
                    "message": "bad request",
                    "success": false
                }
                ```
        * 2 - category id violates required type: 
            * Request:
                ```bash
                curl -X POST \
                    -H "Content-Type: application/json" \
                    -d '{
                        "previous_questions": [1, 9, 7],
                        "quiz_category": {
                            "type": "click",
                            "id": "should be number"
                        }
                    }' http://127.0.0.1:5000/quizzes
                ```
            * Response:
                ```json
                {
                    "error": 400,
                    "message": "bad request",
                    "success": false
                }
                ```   
        * 3 - in previous questions array exists string: 
            * Request:
                ```bash
                curl -X POST \
                    -H "Content-Type: application/json" \
                    -d '{
                        "previous_questions": [1, 9, "string"],
                        "quiz_category": {
                            "type": "science",
                            "id": "1"
                        }
                    }' http://127.0.0.1:5000/quizzes
                ```
            * Response:
                ```json
                {
                    "error": 400,
                    "message": "bad request",
                    "success": false
                }
                ```       

## Author:

* Akhdajonov Oyatillo

Akhadjonov Oyatillo | 2021
