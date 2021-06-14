import os
import unittest
import json
from random import randrange
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@localhost:5432/{}".format(
            'postgres', 'pysql', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        """ Our "fresh" data """
        category_id = Category.query.first().id
        self.fresh_question = {
            "question": "WHAT DO YOU DO?",
            "answer": "I do my homework😃",
            "category": category_id,
            "difficulty": 5
        }

        self.fresh_question_for_update = {
            "question": "Is trivia funny?",
            "answer": "Great! Very!😃",
            "difficulty": 1,
            "category": Category.query.all()[randrange(0, len(Category.query.all()))].id
        }

        self.bad_question_for_update = {
            "question": "mnasd",
            "answer": "",
            "difficulty": "ssasas",
            "category": "212112212112"
        }

        """ ^^^^^^^^^^
            1. "question" min length should be greate than(gt) 5
            2. "answer" is empty
            3. "difficulty" must include digits not letters
            4. "category" API will lot find category with this huge id in DB
            And my custom validator in checking process  gives error, and returns 400 error, bad request)
         """



        """ Our "bad" data """

        self.bad_question = {
            "question": '',
            "answer": "question without answer",
            "category": "asdas",
            "difficulty": 4
        }
        # category must by integer, we give string to give error


        """ Our "fresh" category """

        self.fresh_category = {
            "type": "Machine Learning"
        }


        """ Our "bad" category """

        self.bad_category = {
            "type": ""
        }


        """ Our "fresh" category data for updating """

        self.update_category = {
            "type": "Artificial Intelligience"
        }


        """ Our "bad" category data for updating """

        self.update_category_bad_data = {
            "type": ""
        }



        """ Our "fresh" data to get quiz with previous questions """

        category = Category.query.first()

        questions = Question.query.filter_by(category=category).all()
        self.get_quiz_with_previous = {
            "previous_questions": [2, 3, 5],
            "quiz_category": {
                "type": category.type,
                "id": category.id
            }
        }



        """ Our "fresh" data to get quiz without previous questions """

        self.get_quiz_without_previous = {
            "quiz_category": {
                "type": "loremsd",
                "id": category.id
            }
        }
        


        """ Our "bad" data to get quiz with category """

        self.add_another_category_to_test_quiz = {
            "type": "Data Science"
        }

        self.get_quiz_with_bad_category_id = {
            "previous_questions": [],
            "quiz_category": {
                "type": "badbady",
                "id": 212123123412312123123231
            }
        }


        """ Get None """

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
        Test for:
            [GET] /categories - get all categories
    """

    def test_get_all_categories(self):
        # send request and get response
        response = self.client().get('/categories')
        # load data: load from JS syntax to Python syntax
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    """
        Test for:
            [GET] /categories/<category_id> - get individual category
    """

    def test_get_category_by_id(self):
        category = Category.query.first()
        # send request and get response
        response = self.client().get(f'/categories/{category.id}')
        # load data: load from JS syntax to Python syntax
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    """
        Test for:
            [GET] /categories/<category_id> - get individual category failed
    """

    def test_get_category_by_id_failed(self):
        response = self.client().get(f'/categories/3141122')
        # load data: load from JS syntax to Python syntax
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    """
        Test for:
            [POST] /categories - create new category
    """

    def test_create_new_category(self):
        # send request and get response
        response = self.client().post('/categories', json=self.fresh_category)
        # load data: load from JS syntax to Python syntax
        data = json.loads(response.data)
        created_category = Category.query.get(int(data['created_category_id']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(data['created_category_id']), created_category.id)
        self.assertTrue(data['success'])

    """
        Test for:
            [POST] /categories - create new category failed
    """

    def test_create_new_category_failed(self):
        # send request and get response
        response = self.client().post('/categories', json=self.bad_category)
        # load data: load from JS syntax to Python syntax
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')
        self.assertFalse(data['success'])

    """
        Test for:
            [DELETE] /categories - delete category
    """

    def test_delete_category_by_id(self):
        category_id = Category.query.all()[-1].id
        # send request and get response
        response = self.client().delete(f'/categories/{category_id}')
        # load data: load from JS syntax to Python syntax
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['deleted_category_id'], category_id)
        self.assertTrue(data['success'])

    """
        Test for:
            [DELETE] /categories - delete category failed
    """

    def test_delete_category_by_id_failed(self):
        # send request and get response
        response = self.client().delete('/categories/12231313123')
        # load data: Load from JS syntax to Python syntax
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertFalse(data['success'])

    """
        Test for:
            [PATCH] /categories - update category
    """

    def test_update_category(self):
        category_id = Category.query.first().id
        # send request and get response
        response = self.client().patch(
            f'/categories/{category_id}', json=self.update_category)
        # load data: Load from JS syntax to Python syntax
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['updated_category_id'], category_id)
        self.assertTrue(data['success'])

    """
        Test for:
            [PATCH] /categories - update category failed
    """

    def test_update_category_failed(self):
        category_id = Category.query.first().id
        # send request and get response
        response = self.client().patch(
            f'/categories/{category_id}', json=self.update_category_bad_data)
        # load data: Load from JS syntax to Python syntax
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')
        self.assertFalse(data['success'])

    """
        Test for:
            [GET] /questions - get all questions
    """

    def test_get_all_questions(self):
        # send request and get response
        response = self.client().get('/questions')
        # load data: Load from JS syntax to Python syntax
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['success'])

    """
        Test for:
            [GET] /questions - get all questions failed
    """

    def test_get_all_questions_failed(self):
        # send request and get response
        response = self.client().get('/questions?page=100000000')
        # load data: Load from JS syntax to Python syntax
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertFalse(data['success'])

    """
        Test for:
            [GET] /categories/<category_id>/questions - get questions by category
    """

    def test_get_questions_by_category_id(self):
        category_id = Category.query.all()[0].id
        response = self.client().get(f'/categories/{category_id}/questions')
        # load data: Load from JS syntax to Python syntax
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['success'])

    """
        Test for:
            [GET] /categories/<category_id>/questions - get questions by category failed
    """

    def test_get_questions_by_category_id_failed(self):
        response = self.client().get('/categories/12231313123/questions')
        # load data: Load from JS syntax to Python syntax
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertFalse(data['success'])

    """
        Test for:
            [GET] /questions/<question_id> - get individual question
    """

    def test_get_question_get_by_id(self):
        question_id = Question.query.first().id
        response = self.client().get(f'/questions/{question_id}')
        # load data: Load from JS syntax to Python syntax
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(data['question_id']), int(question_id))
        self.assertTrue(data['success'])

    """
        Test for:
            [GET] /questions/<question_id> - get individual question failed
    """

    def test_get_question_get_by_id_failed(self):
        response = self.client().get('/questions/1010101010')
        # load data: Load from JS syntax to Python syntax
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertFalse(data['success'])

    """
        Test for:
            [POST] /questions - create new question
    """

    def test_create_new_question(self):
        response = self.client().post('/questions', json=self.fresh_question)

        data = json.loads(response.data)
        question = Question.query.get(int(data['created']))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['created'], question.id)
        self.assertTrue(data['success'])

    """
        Test for:
            [POST] /questions - create new question failed
    """

    def test_create_new_question_failed(self):
        response = self.client().post('/questions', json=self.bad_question)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')
        self.assertFalse(data['success'])

    """
        Test for:
            [DELETE] /questions/<question_id> - delete question
    """

    def test_delete_question(self):
        question_id = Question.query.all()[-1].id
        response = self.client().delete(f'/questions/{question_id}')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['deleted_question_id'], question_id)
        self.assertTrue(data['success'])

    """
        Test for:
            [DELETE] /questions/<question_id> - delete question failed
    """

    def test_delete_question_failed(self):
        response = self.client().delete('/questions/121231312213')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertFalse(data['success'])

    """
        Test for:
            [PATCH] /questions/<question_id> - update question
    """

    def test_update_question(self):
        question = Question.query.first()
        print(question)
        response = self.client().patch(
            f'/questions/{question.id}', json=self.fresh_question_for_update)

        data = json.loads(response.data)
        print(question)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['updated_question_id'], question.id)
        self.assertTrue(data['success'])

    """
        Test for:
            [PATCH] /questions/<question_id> - update question failed
    """

    def test_update_question_failed(self):
        question = Question.query.first()
        response = self.client().patch(
            f'/questions/{question.id}', json=self.bad_question_for_update)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')
        self.assertFalse(data['success'])

    """
        Test for:
            [PATCH] /questions/<question_id> - update question failed for 404 error
    """

    def test_update_question_failed_for_404_error(self):
        response = self.client().patch(f'/questions/1221123232331231324234',
                                       json=self.bad_question_for_update)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertFalse(data['success'])

    """
        Test for:
            [POST] /quizzes - quizz game: get quiz by category
    """

    def test_get_quiz_with_previous_questions(self):
        response = self.client().post('/quizzes', json=self.get_quiz_with_previous)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    """
        Test for:
            [POST] /quizzes - quizz game: get quiz without previous questions
    """

    def test_get_quizzes_without_previous_questions(self):
        response = self.client().post('/quizzes', json=self.get_quiz_without_previous)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    """
        Test for:
            [POST] /quizzes - quizz game: get quiz by category failed
    """

    def test_get_quiz_with_bad_category_id(self):

        response = self.client().post('/quizzes', json=self.get_quiz_with_bad_category_id)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')
        self.assertFalse(data['success'])

    """
        Test for:
            [POST] /quizzes - quizz game: get quiz for 400 error
    """

    def test_get_quiz_for_400_error(self):

        response = self.client().post('/quizzes', json={})

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
