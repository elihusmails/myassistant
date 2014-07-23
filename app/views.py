from app import app
from tasks import doAdd
from tasks import currentHomeTemp
from tasks import currentZipcodeTemp

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
