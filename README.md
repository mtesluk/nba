# NBA stats

Project for Engineer’s Thesis, which is using relational database to store NBA statistics, serving them by Django Rest Framework and managing with Angular on client side. Built with CI methodology with Gitlab service.

## PROJECT BACKEND
Python 3.6.7
Django 2.0.7

#Requirements
To install libs in virtualenv exec 'pip install -r requirements.txt'

#Server
To run deveopment server exec 'python manage.py runserver'
To run production server exec 'gunicorn project.wsgi'

#Tests
To run test exec 'python manage.py test'

## NBA-STATS FRONTEND
Angular 7

#Requirements
To install exec 'npm install -g @angular/cli@7' and than 'npm install'

#Server
To run server exec 'ng start'

#Build
To compile app run 'ng build --prod'