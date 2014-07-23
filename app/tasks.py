from celery import Celery
import urllib2
import json


app = Celery('tasks', backend='amqp', broker='amqp://guest@localhost//')

@app.task(name='tasks.doAdd')
def doAdd(x, y):
    return x + y

@app.task(name='tasks.currentHomeTemp')
def currentHomeTemp():
	f = urllib2.urlopen('http://api.wunderground.com/api/<INSERT-KEY>/geolookup/conditions/q/NY/Whitesboro.json')
	json_string = f.read()
	parsed_json = json.loads(json_string)
	location = parsed_json['location']['city']
	temp_f = parsed_json['current_observation']['temp_f']
	f.close()
	return "Current temperature in %s is: %s" % (location, temp_f)
	
@app.task(name='tasks.currentZipcodeTemp')
def currentZipcodeTemp(zipcode):
	f = urllib2.urlopen('http://api.wunderground.com/api/<INSERT-KEY>/geolookup/conditions/q/' + zipcode + '.json')
	json_string = f.read()
	parsed_json = json.loads(json_string)
	location = parsed_json['location']['city']
	temp_f = parsed_json['current_observation']['temp_f']
	f.close()
	return "Current temperature at zipcode %s is: %s" % (zipcode, temp_f)
