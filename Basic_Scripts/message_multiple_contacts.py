import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pickle

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
LOCALSTORAGE_PATH = "localstorages.pkl"

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
            #  driver.add_localstorage(localstorage)
            driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", key, value)

browser = "chrome"
if "firefox" in browser.lower():
    driver = webdriver.Firefox(executable_path = os.path.join(PROJECT_ROOT, "geckodriver"))
elif "chrome" in browser.lower():
    driver = webdriver.Chrome(executable_path = os.path.join(PROJECT_ROOT, "chromedriver"))
driver.get('https://web.whatsapp.com/')
if os.path.isfile(LOCALSTORAGE_PATH):
    load_localstorage(driver, LOCALSTORAGE_PATH)
driver.get(driver.current_url)

def send_msg(driver, name, msg, count):
    try:
        user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
    except selenium.common.exceptions.NoSuchElementException as e:
        search_box = driver.find_element_by_xpath('//div[@id="side"]//input[@title="Search or start new chat"]')
        search_box.send_keys(name)
        user_xpath = '//div[contains(@style, "translateY(72px);")]//span[@title = "{}"]'.format(name)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, user_xpath)))
        user = driver.find_element_by_xpath(user_xpath)
    user.click()

    msg_box = driver.find_element_by_class_name('_3u328')

    for i in range(count):
        msg_box.send_keys(msg)
        button = driver.find_element_by_class_name('_3M-N-')
        button.click()

inp = " "
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]')))
save_localstorage(driver, LOCALSTORAGE_PATH)
contacts = ("Name 1","Name 2","Name 3",)
for i in contacts:
    name = i
    msg = "Good Morning! Hope you have a great day"
    count = 1
    send_msg(driver, name, msg, count)
    time.sleep(1.5)

driver.close()