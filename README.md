myassistant
===========

Project that brings together Python Flask and Python Celery into a system that will provide me with information I'm interested in

Setting up the environment
==========================

"I really have no idea if this is all right or in the correct order.  This may be removed in the 
future as I would imagine installing Flask and Celery are probably common"

1. Execute the command: python virtualenv.py flask
2. Execute the command: python setup.py


Starting Things up
==================

1. Make sure RabbitMQ is running
2. From the "app" folder, run the command: ../flask/bin/celery -A tasks.celery worker --loglevel=info
3. From the top-level folder, run the command: python app/tasks.py
4. To test the system, run the following command: pything tests.py

Useful Links
============
1. http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#installing-celery
2. http://flask.pocoo.org/docs/patterns/celery/
3. http://hairycode.org/2013/07/23/first-steps-with-celery-how-to-not-trip/
4. https://github.com/thrisp/flask-celery-example


Design
======
I want to keep this simple, as its a project that I hope grows and becomes useful.  I am learning 
many things as I more forward with this project.  Things like Python, Flask, Celery, AMQP and RabbitMQ. 

One interesting thing that I quickly realized while developing this code (I found some of it at the 
flask-celery-example link above) is that since this is all asynchronous, the way in which this works is 
to make 2 requests.  The first one submits the request and the second request get the results.  So to look 
at the source code, The first call is made to http://127.0.0.1:5000/myassistant/test.  This will submit the task to the 
backend Celery system and get a task ID.  This task ID is returned to the user/browser/etc.  Then this data 
is parsed and the task ID is sent back as a request using the URL http://127.0.0.1:5000/myassistant/result/<task ID>.  
So while there are 2 requests made, the work is being done while the first response is sent back, processed 
and formed into the second request.  This is what makes the whole system asynchronous and provides a better 
experience for the user.


