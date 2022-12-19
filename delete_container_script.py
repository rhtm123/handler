
import requests as req
import json
from datetime import datetime
import pytz
import time



def delete_container(name):
    url = "http://127.0.0.1:2000/api/v1/container/ssl/delete-container/?container_name="+name 
    res =json.loads(req.get(url).text)
    print(res)



while True:
    url = "https://codingchaska.up.railway.app/api/v1/container/containers/?image_name=&active=true&user="
    res =json.loads(req.get(url).text)
    results = res['results']

    for result in results:
        activetime = datetime.fromisoformat(result['last_active'])
        currenttime = datetime.now(pytz.timezone('Asia/Kolkata'))
        container_name = result['container_name']

        diff = currenttime - activetime
        diff_minutes = (diff.days * 24 * 60) + (diff.seconds/60)
        if diff_minutes>5:
            delete_container(container_name)
    time.sleep(120)
