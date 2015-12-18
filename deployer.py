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
time.sleep(random.uniform(5, 10))
GPIO.output(green_led, 0)
GPIO.output(red_led, 0)


def build(key):
    url = "https://drukwerkdeal.atlassian.net/builds/rest/api/latest/queue/" + key
    myResponse = requests.post(
        url,
        auth = HTTPBasicAuth('dmyroshnychenko', 'dmyroshnychenko_jira'),
        headers = {'accept': 'application/json', 'Content-Type': 'application/json'},
        data='{}'
    ).json()
    return myResponse['link']['href']

def checkState(url):
    print(url)
    myResponse = requests.get(
        url,
        auth = HTTPBasicAuth('dmyroshnychenko', 'dmyroshnychenko_jira'),
        headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    ).json()

    for key in myResponse:
        print(key + " : " + str(myResponse[key]))
    
    if myResponse['buildState'] == 'Successful':
        GPIO.output(green_led, 1)
        GPIO.output(red_led, 0)
    else:
        GPIO.output(green_led, 0)
        GPIO.output(red_led, 1)

while True:
    if GPIO.input(button) == False:
        GPIO.output(green_led, 1)
        
        while GPIO.input(button) == False:
            pass

        key = build('SS-SB')
        while True:
            time.sleep(5)
            checkState(key)
            while GPIO.input(button) == False:
                pass
            break
        
        break

GPIO.cleanup()


