from flask_restful import Resource
from gpiozero import LED
from time import sleep
# from models.toybox import ToyboxModel
led = LED(18)

class TEST(Resource):
    def get(self):
        print('TEST')
        return 'Hello Friend'

class Disco(Resource):

    def get(self):
        led.on()
        sleep(1)
        led.off()
        sleep(1)
        led.on()
        sleep(1)
        led.off()
        sleep(1)
        led.on()
        sleep(1)
        led.off()
        sleep(1)
        led.on()
        sleep(1)
        led.off()
        sleep(1)
        led.on()
        sleep(1)
        led.off()
        print('Initiating Disco')
        return 'Hello Friend'


