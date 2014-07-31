import requests
import random
import json

for i in range(10):
    
    x = random.randrange(1,10000000)
    y = random.randrange(1,1000000000)
    
    p = {'x':x, 'y':y}
    r = requests.get('http://localhost:5000/myassistant/test', params = p)
   
    rJson = json.loads(r.content)
    gto = rJson['url']
    
    r2 = requests.get(gto)
    print '{} + {} = {}'.format(x,y,r2.content)