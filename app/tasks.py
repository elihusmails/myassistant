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

@celery.task(name='tasks.doAdd')
def doAdd(x, y):
    return x + y

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
@app.route("/test")
def hello_world(x=16, y=16):
    x = int(request.args.get("x", x))
    y = int(request.args.get("y", y))
    res = add.apply_async((x, y))
    context = {"id": res.task_id, "x": x, "y": y}
    result = "add((x){}, (y){})".format(context['x'], context['y'])
    goto = "{}".format(context['id'])
    return jsonify(result=result, goto=goto)

@app.route("/test/result/<task_id>")
def show_result(task_id):
    retval = add.AsyncResult(task_id).get(timeout=1.0)
    return repr(retval)

@app.route('/')
@app.route('/index')
def index():
    return 'Hello World!!'

@app.route('/combine')
def combine():
    val = doAdd.delay(2,4)
    if val.ready():
        return "Sum is " + str(val.get(timeout=1))
    else:
        return "Addition operation timed out"

@app.route('/weather/home/temp/current')
def homeWeather():
    val = currentHomeTemp.delay()
    if val.ready():
        return str(val.get(timeout=5))
    else:
        return "Current temperature operation timed out"
        
@app.route('/weather/<zipcode>/temp/current')
def currentTempAtZip(zipcode):
    val = currentZipcodeTemp.delay(zipcode)
    if val.ready():
        return str(val.get(timeout=5, no_ack=False))
    else:
        return "Current zipcode temperature operation timed out"
    
    
'''
==========================================
============== MAIN Section ==============
==========================================
'''
if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)