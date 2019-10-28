from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
import urllib.request
import time
import pickle

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
LOCALSTORAGE_PATH = "localstorages.pkl"

browser = "chrome"
if "firefox" in browser.lower():
    driver = webdriver.Firefox(executable_path = os.path.join(PROJECT_ROOT, "geckodriver"))
elif "chrome" in browser.lower():
    driver = webdriver.Chrome(executable_path = os.path.join(PROJECT_ROOT, "chromedriver.exe"))
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

driver.get('https://web.whatsapp.com/')
#if os.path.isfile(LOCALSTORAGE_PATH):
    #load_localstorage(driver, LOCALSTORAGE_PATH)
driver.get(driver.current_url)

name = input("Enter the contact name to send: ")
msg = input("Enter the message to send: ")
count = int(input("Enter number of time u want to send  the message "))
stime = input("Enter the time in HH:MM:SS: ")
y= datetime.now()
ptime=stime.split(":")
ntime=y.replace(hour=int(ptime[0]),minute=int(ptime[1]),second=int(ptime[2]))
print(ntime)
g=datetime.now()


if(g>ntime):
	print("give a valid time")
	exit()
	



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

while(True):
	t = datetime.now()
	if(t.hour==ntime.hour and t.minute==ntime.minute and t.second==ntime.second):
		send_msg(name, msg, count)
		break
	time.sleep(0.5)