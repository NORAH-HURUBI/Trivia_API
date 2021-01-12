import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

database_name = "trivia_test"
class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','misk','localhost:5432',database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_paginate_questions(self):
        
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), 10)
            
    def test_paginate_questions_out_of_bound(self):  
        res = self.client().get('/questions?page=10999')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        

    def test_retrieve_categories(self):
        
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)
    
    def test_retrieve_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        
    def test_create_question(self):
        test_data = {
            'question': ' test question',
            'answer': 'test answer',
            'difficulty': 1,
            'category': 4,
        }
        res = self.client().post('/questions', json=test_data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_question_empty_fileds(self):
        
        test_data = {
            'question': '',
            'answer': '',
            'difficulty': 5,
            'category': 1,
        }
        res = self.client().post('/questions', json=test_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_delete_question(self):
        test_question = Question(question='test question', answer='test answer',difficulty=3, category=6)
        test_question.insert()
        test_question_id = test_question.id

        res = self.client().delete(f'/questions/{test_question_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_question_not_exist(self):
    
        res = self.client().delete('/questions/9980')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_search_question_empty(self):

        test_data = {
            'searchTerm': '',
        }

        res = self.client().post('/questions/search', json=test_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_search_question(self):

        test_data = {
            'searchTerm': 'Africa',
        }

        res = self.client().post('/questions/search', json=test_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_category_questions(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['current_category'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        

    def test_category_not_valid_id(self):
    
        res = self.client().get('/categories/87/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)   
    
    def test_quiz_success(self):
        test_data = {
            'pre_questions':[5, 9],
            'quiz_category': {
                'id': 4,
                'type': 'History'
            }
        }
        res = self.client().post('/quizzes', json=test_data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertNotEqual(data['question']['id'], 5)
        self.assertNotEqual(data['question']['id'], 9)
        self.assertEqual(data['question']['category'], 4)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()