# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

# API Documentation

## GET Endpoints

GET '/categories'
- Retrieves all available categories.
- Request Arguments: None.
- Returns: all categories with its corresponding ids.

```
Example:
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}

```
GET '/questions' OR GET '/questions?page=<page-number>'
- Retrieves a paginated list of questions of all available categories.
- Request Arguments: Page Number.
- Returns: 
  - All categories.
  - Ten questions per page. 
  - Category type for each question. 
  - Total number of questions.

```
Example:/questions?page=1
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 24
}

```
GET '/categories/<int:category_id>/questions'
- Retrieves a category and its all related questions.
- Request Arguments: category id.
- Returns: 
  - Current category. 
  - Related questions.
  - Total number of questions.

```
Example:/categories/6/questions
{
  "current_category": 6, 
  "questions": [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ], 
  "total_questions": 2
}

```
## POST Endpoints

POST '/questions'
- Add a new question.
- Request body: question, answer, difficulty and category.
- Returns: 
  - Created question id.
  - Total number of questions.

```
Example:curl -POST -H "Content-Type: application/json" -d '{"question":"test question","answer":"test answer","difficulty":"3","category":"4"}'
http://127.0.0.1:5000/questions

  {
  "created": 54,
  "success": true,
  "total_questions": 26
}
```
POST '/questions/search'
- Search for questions that contain specified search term.
- Request body:search term.
- Returns:
  - Related questions to search term.
  - Total number of questions.

```
Example: curl -POST -H "Content-Type: application/json" -d '{"searchTerm":"Africa"}' http://127.0.0.1:5000/questions/search
{
  "current_category": null,
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```
POST '/quizzes'
- A game to pick random questions that either include all categories, or only questions belong to for one specific category.
- Request body:
  - All which include maximum five random questions from all categories. 
     Or
  - Maximum five random questions from chosen category.
- Returns:
  - What the user specify. 

## DELETE Endpoint

DELETE '/questions/<question_id>'
- Delete a question with specified id.
- Request Arguments: question id.
- Returns:
        - Deleted question id.
        - Current questions.
        - Total number of questions.
```
Example:curl -X DELETE http://localhost:5000/questions/54
{
  "deleted": "54",
  "success": true,
  "total_questions": 41
}
```
## Error Handling
404 error 
This error occurs when server not able to locate resources or requested arguments.

```
Example: http://localhost:5000/categories/443/questions
{
  "error": 404, 
  "message": "Resource Not Found", 
  "success": false
}

```
422 error 
This error occurs when server not able to process request body.

```
Example: curl -POST -H "Content-Type: application/json" -d '{"searchTerm":""}' http://127.0.0.1:5000/questions/search
{
  "error": 422,
  "message": "Unprocessable Entity",
  "success": false
}

```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```