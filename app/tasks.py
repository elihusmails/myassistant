from __future__ import absolute_import
from os import path, environ
import json
from flask import Flask, Blueprint, abort, jsonify, request, session
import settings
from celery import Celery
import urllib2


app = Flask(__name__)
app.config.from_object(settings)

'''
==========================================
============= CELERY Section =============
==========================================
'''
def make_celery(app):
    celery = Celery(app.import_name, backend='amqp', broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@celery.task(name='tasks.currentHomeTemp')
def currentHomeTemp():
    f = urllib2.urlopen('http://api.wunderground.com/api/' 
                        + app.config['WUNDERGROUND_KEY'] 
                        + '/geolookup/conditions/q/NY/Whitesboro.json')
    
    json_string = f.read()
    parsed_json = json.loads(json_string)
    location = parsed_json['location']['city']
    temp_f = parsed_json['current_observation']['temp_f']
    f.close()
    return "Current temperature in %s is: %s" % (location, temp_f)
	
@celery.task(name='tasks.currentZipcodeTemp')
def currentZipcodeTemp(zipcode):
	f = urllib2.urlopen('http://api.wunderground.com/api/' 
                        + app.config['WUNDERGROUND_KEY'] 
                        + '/geolookup/conditions/q/' + zipcode + '.json')
    
	json_string = f.read()
	parsed_json = json.loads(json_string)
	location = parsed_json['location']['city']
	temp_f = parsed_json['current_observation']['temp_f']
	f.close()
	return "Current temperature at zipcode %s is: %s" % (zipcode, temp_f)

@celery.task(name="tasks.add")
def add(x, y):
    return x + y



'''
==========================================
============= FLASK Section ==============
==========================================
'''
@app.route('/')
@app.route('/index')
def index():
    return 'Hello World!!'


@app.route("/myassistant/test")
def hello_world(x=16, y=16):
    x = int(request.args.get("x", x))
    y = int(request.args.get("y", y))
    res = add.apply_async((x, y))
    return generateTaskIdJson(res)


@app.route("/myassistant/result/<task_id>")
def show_result(task_id):
    retval = add.AsyncResult(task_id).get(timeout=1.0)
    return repr(retval)


@app.route('/myassistant/weather/home/temp/current')
def homeWeather():
    res = currentHomeTemp.apply_async()
    return generateTaskIdJson(res)

        
@app.route('/myassistant/weather/<zipcode>/temp/current')
def currentTempAtZip(zipcode):
    res = currentZipcodeTemp.delay(zipcode)
    return generateTaskIdJson(res)


'''
==========================================
=========== UTILITY Section ==============
==========================================
'''
def generateTaskIdJson(taskResult):
    context = {"id": taskResult.task_id, 
              "url": 'http://' + app.config['CALLBACK_IP'] 
                                    + ':'
                                    + str(app.config['CALLBACK_PORT'])
                                    + '/myassistant/result/'
                                    + taskResult.task_id}
    goto = "{}".format(taskResult.task_id)
    callbackUrl = "{}".format(context);
    return jsonify(callback=callbackUrl)

'''
==========================================
============== MAIN Section ==============
==========================================
'''
if __name__ == "__main__":
    port = int(environ.get("PORT", app.config['LISTEN_PORT']))
    app.run(host=app.config['LISTEN_ADDRESS'], port=port, debug=True)