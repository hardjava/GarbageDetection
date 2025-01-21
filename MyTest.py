from MyBrowser import BrowserController
from MyArduino import ArduinoController
from MyModel import *
import time

browser = BrowserController('http://172.20.10.5')
browser.start_browser()
browser.click_button("toggle-stream")
arduino = ArduinoController(port='COM7', baudrate=9600)
arduino.connect()
arduino2 = ArduinoController(port='COM3', baudrate=9600)
arduino2.connect()

try:
    while True:
        if arduino.read_arduino() != None:
            img_path = browser.click_save_img("save-still")
            predicted = predict_external_image(img_path)
            arduino.write_lcd(predicted)
            print("send to arduino1")
            arduino2.write_rotation(predicted)
            print("send to arduino2")
except KeyboardInterrupt:
    print("Get Keyboard Interrupt")
    browser.close_browser()
    arduino.disconnect()
    arduino2.disconnect()