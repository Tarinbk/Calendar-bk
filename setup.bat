@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment and installing Django...
call venv\Scripts\activate.bat
pip install django

echo Creating Django project and app...
django-admin startproject config .
python manage.py startapp events

echo Migrating database...
python manage.py migrate

echo ========================================================
echo Setup complete! 
echo To start your development server, run:
echo 1. venv\Scripts\activate
echo 2. python manage.py runserver
echo ========================================================
pause
