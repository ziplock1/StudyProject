import requests
import datetime
import json


def flowers1_light_control(state):
    command = '{"data":{"switch": "' + state + '"}}'
    i = 0
    while True:
        i += 1
        r = requests.post('http://192.168.9.10:8081/zeroconf/switch', data=command)
        result = json.loads(r.text)
        err = result["error"]
        if err == 0:
            break
        if i >= 10:
            break
    if i < 10:
        return 0
    else:
        return err


def get_flowers1_light_state():
    r = requests.post('http://192.168.9.10:8081/zeroconf/info', data='{"data":{}}')
    if r.status_code == 200:
        result = json.loads(r.text)
        return result["data"]["switch"]


holidays = ["01.01", "02.01", "03.01", "04.01", "05.01", "08.01",
            "23.02", "08.03", "29.04", "30.04", "01.05", "09.05",
            "10.05", "12.06", "04.11", "30.12", "31.12"]

today = datetime.datetime.now()
dayofweek = today.weekday()
day_month = f'{today.day:02d}' + "." + f'{today.month:02d}'

if (dayofweek >= 5) or (day_month in holidays):
    on_time = datetime.time(11, 0, 0)
    off_time = datetime.time(21, 0, 0)
else:
    on_time = datetime.time(9, 0, 0)
    off_time = datetime.time(20, 0, 0)

cur_time = datetime.datetime.now().time()

Flowers1_light_state = get_flowers1_light_state()

if (cur_time >= on_time) and (cur_time < off_time):
    if Flowers1_light_state == "off":
        flowers1_light_control("on")
else:
    if Flowers1_light_state == "on":
        flowers1_light_control("off")
