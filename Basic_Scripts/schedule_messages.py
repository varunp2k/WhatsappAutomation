from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
import urllib.request
import time
import pickle

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
LOCALSTORAGE_PATH = "localstorages.pkl"

browser = "firefox"
if "firefox" in browser.lower():
    driver = webdriver.Firefox(executable_path = os.path.join(PROJECT_ROOT, "geckodriver"))
elif "chrome" in browser.lower():
    driver = webdriver.Chrome(executable_path = os.path.join(PROJECT_ROOT, "chromedriver"))
def save_localstorage(driver, path):
    with open(path, 'wb') as filehandler:
        localstorage = dict(driver.execute_script( \
            "var ls = window.localStorage, items = {}; " \
            "for (var i = 0, k; i < ls.length; ++i) " \
            "  items[k = ls.key(i)] = ls.getItem(k); " \
            "return items; "))
        pickle.dump(localstorage, filehandler)

def load_localstorage(driver, path):
     with open(path, 'rb') as localstoragesfile:
         localstorages = dict(pickle.load(localstoragesfile))
         for key, value in localstorages.items():
            driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", key, value)

name = input("Enter the contact name to send: ")
message = input("Enter the message to send: ")
frequency = input("Enter frequency in the form 'HH:MM:SS': ")
try:
    hour = int(frequency[:2])
    minute = int(frequency[3:5])
    seconds = int(frequency[-2:])
except ValueError as e:
    print("Format of the frequency is incorrect. Assuming 10 seconds.")
    hour = 0
    minute = 0
    seconds = 10

driver.get('https://web.whatsapp.com/')
if os.path.isfile(LOCALSTORAGE_PATH):
    load_localstorage(driver, LOCALSTORAGE_PATH)
driver.get(driver.current_url)

def send_msg(name, msg, count):
    print("Sending message: '%s' to %s" % (msg, name))
    start = time.time()
    print("Time to find element: {} s".format(time.time() - start))
    start = time.time()
    user = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//span[@title = "{}"]'.format(name))))
    user.click()
    print("Time to click: {} s".format(time.time() - start))

    start = time.time()
    msg_box = driver.find_element_by_class_name('_3u328')
    print("Time to find message box: {} s".format(time.time() - start))

    
    for i in range(count):
        start = time.time()
        msg_box.send_keys(msg)
        print("Time to type message: {} s".format(time.time() - start))
        start = time.time()
        button = driver.find_element_by_class_name('_3M-N-')
        button.click()
        print("Time to send message: {} s".format(time.time() - start))

inp = " "
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]')))
save_localstorage(driver, LOCALSTORAGE_PATH)

scheduler = BackgroundScheduler()

scheduler.add_job(send_msg, "interval", seconds=seconds, minutes=minute, hours=hour, args=(name, message, 1))

try:
    scheduler.start()
    while True:
        time.sleep(10)
except (KeyboardInterrupt, SystemExit) as e:
    print(e)
    scheduler.shutdown(wait=True)

# driver.close()