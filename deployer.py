import RPi.GPIO as GPIO
import time
import random
import requests
from requests.auth import HTTPBasicAuth

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

green_led = 4
red_led = 17
button = 14

GPIO.setup(green_led, GPIO.OUT)
GPIO.setup(red_led, GPIO.OUT)
GPIO.setup(button, GPIO.IN, GPIO.PUD_UP)

GPIO.output(green_led, 1)
GPIO.output(red_led, 1)
time.sleep(random.uniform(5, 10))
GPIO.output(green_led, 0)
GPIO.output(red_led, 0)

id = 0


def build(key):
    url = "https://drukwerkdeal.atlassian.net/builds/rest/api/latest/queue/" + key
    myResponse = requests.post(
        url,
        auth = HTTPBasicAuth('dmyroshnychenko', 'dmyroshnychenko_jira'),
        headers = {'accept': 'application/json', 'Content-Type': 'application/json'},
        data='{}'
    ).json()
    return myResponse['buildNumber']

def checkState(key):
    global id
    
    if id:
        url = 'https://drukwerkdeal.atlassian.net/builds/rest/api/latest/result/' + key + '-' + str(id)
        print(url)
        latest = requests.get(
            url,
            auth = HTTPBasicAuth('dmyroshnychenko', 'dmyroshnychenko_jira'),
            headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
        ).json()
        buildUrl = ''
    else:
        url = 'https://drukwerkdeal.atlassian.net/builds/rest/api/latest/result/' + key
        print(url)
        myResponse = requests.get(
            url,
            auth = HTTPBasicAuth('dmyroshnychenko', 'dmyroshnychenko_jira'),
            headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
        ).json()

        latest = myResponse['results']['result'][0]

    #for key in latest:
    #    print(key + " : " + str(latest[key]))
    print(latest['buildState'])
    print(latest['buildNumber'])

    if latest['lifeCycleState'] == 'Finished':
        id = 0
    
    if latest['buildState'] == 'Successful':
        GPIO.output(green_led, 1)
        GPIO.output(red_led, 0)
    else:
        GPIO.output(green_led, 0)
        GPIO.output(red_led, 1)

while True:
    checkState('SS-SB')
    time.sleep(5)
    if GPIO.input(button) == False:
        GPIO.output(green_led, 1)
        GPIO.output(red_led, 1)
        t1 = time.clock()
        while GPIO.input(button) == False:
            pass
        t2 = time.clock()
        GPIO.output(green_led, 0)
        GPIO.output(red_led, 0)
        if t2-t1 > 3:
            break

        id = build('SS-SB')

GPIO.cleanup()


