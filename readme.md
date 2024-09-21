# run 
pip install -r requirements.txt

python -m venv env

cd env/Scripts

activate

cd ../..

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

server is running on http://127.0.0.1:8000/