import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from custom_validator import valid_response
from flask_cors.decorator import cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    #========================================#
    #                                        #
    #  CORS (Cross Origin Resource Sharing)- #
    #  settings                       #      #
    #                                        #
    #========================================#

    @app.after_request
    def after_reques(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Mehotds',
                             'GET, POST, PATCH, DELETE')
        response.headers.add('Content-Type', 'application/json')

        return response
    #========================================#
    #                                        #
    #  HELPERS - paginating function         #
    #  and filter_questions function         #
    #                                        #
    #========================================#

    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = [questions.format() for questions in selection]
        current_questions = questions[start:end]

        return current_questions

    def filter_questions(previous_questions, questions):
        return [question for question in questions if question['id'] not in previous_questions]
    #========================================#
    #                                        #
    #   [GET] /categories - retrive all      #
    #   categories                           #
    #                                        #
    #========================================#

    @app.route('/categories', methods=['GET'])
    @cross_origin()
    def get_all_catgories():
        categories = Category.query.all()
        if len(categories) == 0:
            abort(404)
        formatted_categories = {}
        for category in categories:
            formatted_categories[str(category.format()['id'])] = category.format()[
                'type']

        return jsonify({
            "success": True,
            "categories": formatted_categories,
            "total_categories": len(categories)
        })
    #========================================#
    #                                        #
    #  [GET] /categories/<category_id> - get #
    #  get category by id                    #
    #                                        #
    #  [DELETE] /categories/<category_id> -  #
    #  delete category                       #
    #                                        #
    #  [PATCH] - categories/<category_id> -  #
    #  update category                       #
    #                                        #
    #========================================#

    @app.route('/categories/<int:category_id>', methods=['GET', 'PATCH', 'DELETE'])
    @cross_origin()
    def get_or_delete_or_update_category_by_id(category_id):
        if request.method == 'GET':
            category = Category.query.get_or_404(category_id)
            return jsonify({
                "category_id": category.id,
                "category_type": category.type,
                "total_categories": len(Category.query.all()),
                "success": True
            })
        if request.method == 'DELETE':
            category = Category.query.get_or_404(category_id)
            try:
                category.delete()
                return jsonify({
                    "deleted_category_id": category.id,
                    "success": True
                })
            except:
                abort(422)

        if request.method == 'PATCH':
            category = Category.query.get_or_404(category_id)
            data = request.get_json()
            try:
                if 'type' in data:
                    if len(data['type']) > 3:
                        category.type = data['type']
                    else:
                        abort(400)
                category.update()
                return jsonify({
                    "success": True,
                    "updated_category_id": category.id
                })
            except:
                abort(400)
    #========================================#
    #                                        #
    #   [POST] /categories - create new      #
    #   category                             #
    #                                        #
    #========================================#

    @app.route('/categories', methods=['POST'])
    @cross_origin()
    def add_new_category():
        data = request.get_json()
        new_category = data.get('type')
        print(data)
        if not new_category:
            abort(400)
        try:
            category = Category(type=new_category)
            category.insert()
            return jsonify({
                "created_category_id": category.id,
                "success": True
            })
        except:
            abort(400)
    #========================================#
    #                                        #
    #   [GET]                                #
    #   /categories/<category_id>/questions  #
    #   - get questions by category          #
    #                                        #
    #========================================#

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    @cross_origin()
    def get_questions_by_category(category_id):
        current_category = Category.query.get_or_404(category_id)
        current_questions = paginate_questions(
            request, current_category.questions)
        return jsonify({
            "questions": current_questions,
            "total_questions": len(Question.query.all()),
            "current_category": current_category.type,
            "success": True
        })
    #========================================#
    #                                        #
    #  [GET] /questions - get all questions  #
    #                                        #
    #========================================#

    @app.route('/questions', methods=['GET'])
    @cross_origin()
    def get_all_questions():
        selection = Question.query.all()
        current_questions = paginate_questions(request, selection)
        if len(current_questions) == 0:
            abort(404)
        categories = Category.query.all()
        formatted_categories = {}
        for category in categories:
            formatted_categories[str(category.format()['id'])] = category.format()[
                'type']
        return jsonify({
            "questions": current_questions,
            "total_questions": len(selection),
            "categories": formatted_categories,
            "success": True
        })
    #========================================#
    #                                        #
    #   [POST] /questions - create new       #
    #   question                             #
    #                                        #
    #========================================#

    @app.route('/questions', methods=['POST'])
    @cross_origin()
    def create_new_question():
        data = request.get_json()
        new_question = data.get('question')
        new_answer = data.get('answer')
        parent_category = data.get('category')
        new_difficulty = data.get('difficulty')
        search_term = data.get('searchTerm')
        try:
            if search_term:
                questions = Question.query.filter(
                    Question.question.ilike(f'%{search_term}%'))
                print(questions)
                current_questions = paginate_questions(request, questions)
                return jsonify({
                    "questions": current_questions,
                    "total_questions": len(Question.query.all())
                })

            else:
                category_id = int(parent_category)
                category_parent = Category.query.get(category_id)
                if len(new_question) < 5 or category_parent is None:
                    abort(400)
                create_question = Question(question=new_question, answer=new_answer,
                                           category=category_parent, difficulty=new_difficulty)
                create_question.insert()
                return jsonify({
                    "success": True,
                    "created": create_question.id
                })
        except:
            abort(400)
    #========================================#
    #                                        #
    #   [GET] /questions/<question_id> - get #
    #   question by id                       #
    #                                        #
    #   [DELETE] - questions/<question_id> - #
    #   delete question                      #
    #                                        #
    #   [PATCH] - questions/<question_id> -  #
    #   update question                      #
    #                                        #
    #========================================#

    @app.route('/questions/<int:question_id>', methods=['GET', 'DELETE', 'PATCH'])
    @cross_origin()
    def get_or_delete_question(question_id):
        if request.method == 'GET':
            question = Question.query.get_or_404(question_id)
            return jsonify({
                "question_id": question.id,
                "question": question.question,
                "answer": question.answer,
                "difficulty": question.difficulty,
                "category_id": question.category.format()["id"],
                "category": question.category.format()["type"],
                "total_questions": len(Question.query.all()),
                "success": True
            })

        if request.method == 'PATCH':
            question = Question.query.get_or_404(question_id)
            data = request.get_json()

            try:
                if valid_response(data, 'question'):
                    question.question = data['question']
                if valid_response(data, 'answer'):
                    question.answer = data['answer']
                if valid_response(data, 'difficulty'):
                    question.difficulty = int(data['difficulty'])
                if valid_response(data, 'category_id', Category):
                    try:
                        category = Category.query.get(int(data['category_id']))
                        if category:
                            question.category = category
                        else:
                            abort(400)
                    except:
                        abort(400)
                question.update()
                return jsonify({
                    'success': True,
                    'updated_question_id': question.id
                })
            except:
                abort(400)

        if request.method == 'DELETE':
            question = Question.query.get_or_404(question_id)

            if question:
                question.delete()
                return jsonify({
                    "deleted_question_id": question.id,
                    "success": True
                })
            else:
                abort(422)
    #======================================#
    #                                      #
    #   [POST] /quizzes - play and enjoy   #
    #   with trivia quiz game              #
    #                                      #
    #======================================#

    @app.route('/quizzes', methods=['POST'])
    @cross_origin()
    def play_trivia_quizz_game():
        data = request.get_json()
        print(data)
        try:
            if data:
                previous_questions = data.get('previous_questions', [])
                quiz_category = data.get('quiz_category')
                if int(quiz_category['id']) == 0 or quiz_category['type'] == 'click':
                    questions = Question.query.all()
                    questions = [question.format()
                                for question in questions]
                    questions = filter_questions(
                        previous_questions, questions)
                else:
                    category = Category.query.get(int(quiz_category['id']))
                    if category and category != None:
                        questions = Question.query.filter(
                            Question.category == category).all()
                        questions = [question.format()
                                    for question in questions]
                        questions = filter_questions(
                            previous_questions, questions)
                    else:
                        abort(400)
                if len(questions) > 0:
                    print(questions)
                    return jsonify({
                        "previous_questions": previous_questions,
                        "quiz_category": quiz_category['id'],
                        "question": questions[random.randrange(0, len(questions))],
                        "success": True
                    })
                else:
                    return jsonify({
                        "previous_questions": previous_questions,
                        "question": None,
                        "success": True
                    })
            else:
                abort(400)
        except:
            abort(400)

    #====================#
    #                    #
    #   ErrorHandlers    #
    #                    #
    #====================#
    #                    #
    #   [400] - bad      #
    #   request          #
    #                    #
    #====================#

    @app.errorhandler(400)
    def resource_not_found(e):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400
    #====================#
    #                    #
    #   [404] - resource #
    #   not found        #
    #                    #
    #====================#

    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404
    #====================#
    #                    #
    #   [405] - method   #
    #   not allowed      #
    #                    #
    #====================#

    @app.errorhandler(405)
    def resource_not_found(e):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method now allowed'
        }), 405
    #====================#
    #                    #
    #   [422] - unproces #
    #   -sable entity    #
    #                    #
    #====================#

    @app.errorhandler(422)
    def resource_not_found(e):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable entity'
        }), 422

    return app
