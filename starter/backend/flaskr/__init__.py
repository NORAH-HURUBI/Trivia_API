import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
#=====================================================================================#
def paginate_questions(request, select_question):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in select_question]
  current_questions = questions[start:end]
  return current_questions
#=====================================================================================#
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  
  
  #Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  
#=====================================================================================#
  CORS(app, resources={'/': {'origins': '*'}})
#=====================================================================================#
  
 # the after_request decorator to set Access-Control-Allow
  
#=====================================================================================#
  @app.after_request
  def after_request(response):
   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
   return response
#=====================================================================================#
# an endpoint to handle GET requests for all available categories. 
#=====================================================================================#
  @app.route('/categories')
  def retrieve_categories():

   try:
     get_categories = Category.query.all()
     categories_type = {category.id: category.type for category in get_categories}

     return jsonify({
                'success': True,
                'categories': categories_type
            }), 200
   except:
            abort(404)
#=====================================================================================#
  
#an endpoint to handle GET requests for questions,including pagination (every 10 questions). 
#This endpoint should return a list of questions,number of total questions, current category, categories.
 
#=====================================================================================#
  @app.route('/questions')
  def retrieve_questions():
    select_question = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, select_question)
    
    if len(current_questions) == 0:
      abort(404)
   
    get_categories = Category.query.all()
    category_type = {category.id: category.type for category in get_categories}

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(select_question),
      'categories': category_type,
      'current_category': None
    })
#=====================================================================================#

#an endpoint to DELETE question using a question ID. 
  
#=====================================================================================#
  @app.route('/questions/<question_id>', methods=['DELETE'])
  def delete_question(question_id):
    
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()
      select_question = Question.query.all()
      

      return jsonify({
        'success': True,
        'deleted': question_id,
        'total_questions': len(select_question)
      })

    except:
      abort(422)

#=====================================================================================#
# an endpoint to POST a new question, which will require the question and answer text, 
#category, and difficulty score.
#=====================================================================================#
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
    new_question = body.get('question')
    answer_text = body.get('answer')
    difficulty_score = body.get('difficulty')
    category = body.get('category')
    if new_question == "" and answer_text == "":
            abort(422)
    
    try:
       question = Question(question=new_question, answer=answer_text, 
        difficulty=difficulty_score, category=category)
       question.insert()
  
       questions = Question.query.order_by(Question.id).all()
       return jsonify({
        'success': True,
        'created': question.id,
        'total_questions': len(questions)
      })
    except:
        abort(422)
#=====================================================================================#
 # a POST endpoint to get questions based on a search term. 
 # It should return any questions for whom the search term is a substring of the question. 
#=====================================================================================#
  @app.route('/questions/search', methods=['POST'])
  def search_question():
   term = request.get_json()
   search = term.get('searchTerm')
   searching_questions = "%{}%".format(search)
   if search == "":
     abort(422)
   try:
     select_question = Question.query.order_by(Question.id).filter(Question.question.ilike(searching_questions)).all()
     current_questions = paginate_questions(request, select_question)
     questions_len=len(select_question)
     return jsonify ({
         'success': True,
        'questions': current_questions,
        'total_questions': questions_len,
        "current_category": None
            })
   except:
        abort(404)

#=====================================================================================#

# a GET endpoint to get questions based on category. 

#=====================================================================================#
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_category_questions(category_id):
      get_category = Category.query.get(category_id)
      if not get_category:
            abort(404)
      try:
       category_questions = Question.query.filter_by(category=category_id).all()
       questions_format = [questions.format() for questions in category_questions]
       return jsonify({
           'success': True,
           'questions': questions_format,
           'total_questions': len(category_questions),
           'current_category': category_id
        })
      except:
        abort(422)
#=====================================================================================#
 # Create a POST endpoint to get questions to play the quiz. 
 # This endpoint should take category and previous question parameters 
 # and return a random questions within the given category, 
 # if provided, and that is not one of the previous questions. 
#=====================================================================================#
  @app.route('/quizzes', methods=['POST'])
  def quiz():
    play = request.get_json()
    pre_questions = play.get('previous_questions',[])
    quiz_category = play.get('quiz_category')
    if (quiz_category['id'] == 0):
        #- fetches maximum a five questions from all categories..
      play_quiz = Question.query.all()
    else:
       #- fetches maximum a five questions from one chosen category..
      play_quiz = Question.query.filter_by(category=quiz_category['id']).all() 
    num_of_questions = len(play_quiz)
    #- To pick random question..
    def random_question():
      return play_quiz[random.randint(0, len(play_quiz)-1)]

    next_question = random_question()
    #- This function to check the question repetition...
    def repetition(next_question):
     repeated =False
     if next_question.id in pre_questions:
          repeated =True
     return repeated

   #- This loop  to ensure the question not repeated..
    while  repetition(next_question) :
      next_question = random_question()
      # Required to put (if ) when the total of questions less than 5 ...
      if (len(pre_questions) == num_of_questions):
                return jsonify({
                    'success': True
                })

    return jsonify({
            'success': True,
            'question': next_question.format(),
        })
#=====================================================================================#
  
# error handlers for all expected errors including 404 and 422. 
  
#=====================================================================================#
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "Resource Not Found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "Unprocessable Entity"
      }), 422
#=====================================================================================#
  
  return app

    