# spa_app

This project implements a comment system with the ability to add files and images, as well as CAPTCHA support

"""The project was developed for the backend, but for better understanding and ease of testing, templates were added to display registration forms, autothentication, and adding comments (captcha display)."""

## Requirements.

- Python 3.8+
- Django 4.2
- PostgreSQL
- Redis (для Celery)
- Docker та Docker Compose (optional for deployment via containers)

## Installation.

### 1. Cloning a repository

git clone https://github.com/your-repo/django-comments-project.git
cd spa_app

2. Create a virtual environment
In pycharm:
File/setting/Add interpriter/add local interpriter
	or
In terminal:
python -m venv venv

activate:
source venv/bin/activate  # for Windows: venv\Scripts\activate

3. Setting dependencies
pip install -r requirements.txt

4. Setting up the environment
Create an .env file based on the .env_example and fill in the necessary environment variables:
cp .env_example .env
# Edit the .env file and fill in the values of the variables

5. Generate a SECRET_KEY for the Django project
Write the command in the terminal:
python -c "import random; import string; print(''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(50)))"
Insert the resulting key into the .env file SECRET_KEY=.

Example of filling in the .env:
POSTGRES_HOST=db
POSTGRES_USER=postgres1
POSTGRES_PASSWORD=postgres1
POSTGRES_DB=postgres1
POSTGRES_PORT=5432
PGADMIN_DEFAULT_EMAIL=postgres1@gmail.com
PGADMIN_DEFAULT_PASSWORD=postgres1
PGADMIN_LISTEN_PORT=5050
SECRET_KEY = "your generated secret key"
CELERY_BROKER_URL=redis://redis:6379
CELERY_RESULT_BACKEND=redis://redis:6379

EMAIL_HOST=smtp.gmail.com
EMAIL_FROM=example@gmail.com
EMAIL_HOST_USER=example@gmail.com
EMAIL_HOST_PASSWORD=you have to generate it by yourself
EMAIL_PORT=587
CORPORATE_EMAIL=youremail@gmail.com

Using Docker
1. Create and run containers
To deploy the project, run the following commands:
docker-compose up --build
In the future, you can use the command to launch the project:
docker-compose up

2. Migrations and creating a superuser
After starting the containers, perform migrations and create a superuser:
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

Start checking example via Postman (manually) 

Register a new user:
http://localhost:8000/register/
Body raw:
{
    "username": "user",
    "email": "user@example.com",    
    "password": "password123",
    "password_confirmation": "password123",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "123456789",
    "city": "Kyiv",
    "country": "Ukraine"
}

Get token
http://localhost:8000/token/
{    
    "email": "user@example.com",
    "password": "password123"
}

go to the endpoint 
Authorization  Token  enter: Bearer 'received token'   click Send


endpoints:
GET:
http://localhost:8000/comments/ 
http://localhost:8000/comments/1

POST:
http://localhost:8000/comments/ 

http://localhost:8000/comments/1
{
  "user": 1,
  "username": "user",
  "email": "user@example.com",
  "text": "This is a reply",
  "home_page": "http://example.com",
  "parent": 1
}

http://localhost:8000/comments/1/
PUT:
{
    "id": 1,
    "username": "user",
    "email": "user@example.com",    
    "text": "This is a comment has updated",
    "date": "2024-06-30T21:04:42.565772Z",
    "user": 1,
    "parent": null
}

http://localhost:8000/comments/1/
DELETE:


Для перевірки додавання повідомлення і перевірки каптчі, перейдіть до http://localhost:8000/comments/ в вашому браузері.

Possible errors:

If you encounter the following error while using Redis:
ERROR: for redis  Cannot start service redis: driver failed programming external connectivity on endpoint spa_app_redis_1 (********efc6a28e18427a04bbff47003725e9740119fe8e0322bee327f256be): Error starting userland proxy: listen tcp4 0.0.0.0:6379: bind: address already in use
Solution:
sudo systemctl stop redis

Most errors can be solved with a command:
docker-compose down this will delete the data from the database (Caution)

Celery:
Celery is used for asynchronous processing of tasks, such as sending emails when comments are created or replied to. It allows you to perform tasks outside the main application thread, which provides fast responsiveness and distributed processing.

Signals:
Signals are used to automatically delete the cache after saving or deleting comments. This maintains data consistency and ensures that the list of comments in the cache is updated after every change in the database.


















