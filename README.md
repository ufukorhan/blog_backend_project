# Blog Project Backend

1. Clone the repository
```
git clone https://github.com/ufukorhan/blog_backend_project.git
```

2. Create a virtual environment
```
virtualenv -p python3.11 venv # python version what you use.
```
3. Activate the virtual environment
```
source venv/bin/activate
```
4. Install the requirements
```
pip install -r requirements.txt
```
5. Create a .env file in the root directory of the project
```
touch .env
```
6. Add the following environment variables to the .env file
    - DEBUG
    - SECRET_KEY 
    - PG_DB_HOST
    - PG_DB_USER
    - PG_DB_PASSWORD
    - PG_DB_NAME
    - PG_DB_PORT
      
You should make the necessary configurations in settings.py

7. Run the migrations
```
python manage.py migrate
```
8. Create a superuser
```
python manage.py createsuperuser
```
9. Run the server
```
python manage.py runserver
```

10. Access the API endpoints
```
http://localhost:8000/swagger/
```

11. Run the tests
