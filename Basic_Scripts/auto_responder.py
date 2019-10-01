from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
            #  driver.add_localstorage(localstorage)
            driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", key, value)
# print("1. Load localstorages\n2. Don't load localstorages\nInput: ", end="")
# choice = int(input())
driver.get('https://web.whatsapp.com/')
# if choice == 1:
if os.path.isfile(LOCALSTORAGE_PATH):
    load_localstorage(driver, LOCALSTORAGE_PATH)
driver.get(driver.current_url)
default_contact = "A1"
messages_dict = {"hi": "Hello", "ok": "OK", "namaste": "Saadar pranam", "hello":"Hi"}

def send_msg(driver, name, msg, count):
    print("Sending message: '%s' to %s" % (msg, name))
    start = time.time()
    # user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
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

def reply_to_messages(driver, name, messages_dict, msg, tick_mark, sending_clock):
    # print(msg)
    if(msg == "typing..."):
        return
    for message, reply in messages_dict.items():
        if msg.lower() == message and tick_mark == [] and sending_clock == []:
            send_msg(driver, msg_sender, reply, 1)
            break

# input("Press any key after loading")
# img = driver.find_element_by_xpath("//img[@alt='Scan me!']")
# src = img.get_attribute('src')
# urllib.request.urlretrieve(src, "captcha.png")
inp = " "
# input("Press any key after QR code scan")
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]')))
save_localstorage(driver, LOCALSTORAGE_PATH)
allchats = driver.find_elements_by_xpath("//div[contains(@style, 'z-index')]")
allchats = [chat.get_attribute("style") for chat in allchats]
allchats = [int(chat.split("z-index: ")[1].split(";")[0]) for chat in allchats]
while inp != "":
    while True:
        msg = driver.find_element_by_xpath("//div[contains(@style,'z-index: ')]//span[@dir='ltr']").text
        print("msg first:", msg)
        msg_sender = driver.find_element_by_xpath("//div[contains(@style,'z-index: ')]//span[@dir='auto']").get_attribute("title")
        # print(msg_sender)
        new_msg = driver.find_elements_by_xpath("//div[contains(@style,'z-index: ')]//span[@class='P6z4j']")
        # print(new_msg)
        # tick_mark = driver.find_elements_by_xpath("//div[contains(@style,'z-index: ')]//span[@data-icon='status-dblcheck']")
        tick_mark_user = driver.find_element_by_xpath("//div[contains(@style,'z-index: ')]")
        tick_mark = tick_mark_user.find_elements_by_xpath(".//span[contains(@data-icon,'status-dblcheck')]")
        sending_clock = tick_mark_user.find_elements_by_xpath(".//span[contains(@data-icon,'status-time')]")
        # print("Tick mark first:", tick_mark)
        reply_to_messages(driver, msg_sender, messages_dict, msg, tick_mark, sending_clock)
        for i in allchats:
            try: 
                msg = driver.find_element_by_xpath("//div[contains(@style,'z-index: {};')]//span[@dir='ltr']".format(i)).text
                print("msg {}:".format(i), msg)
                msg_sender = driver.find_element_by_xpath("//div[contains(@style,'z-index: {};')]//span[@dir='auto']".format(i)).get_attribute("title")
                # print(msg_sender)
                new_msg = driver.find_elements_by_xpath("//div[contains(@style,'z-index: {};')]//span[@class='P6z4j']".format(i))
                # print(new_msg)
                # tick_mark = driver.find_elements_by_xpath("//div[contains(@style,'z-index: {};')]//span[@data-icon='status-dblcheck']".format(i))
                # # print(tick_mark)
                tick_mark_user = driver.find_element_by_xpath("//div[contains(@style,'z-index: {};')]".format(i))
                tick_mark = tick_mark_user.find_elements_by_xpath(".//span[contains(@data-icon,'status-dblcheck')]")
                sending_clock = tick_mark_user.find_elements_by_xpath(".//span[contains(@data-icon,'status-time')]")
                print("Tick mark {}:".format(i), tick_mark)
            except selenium.common.exceptions.NoSuchElementException as e:
                print(e)
                continue
            reply_to_messages(driver, msg_sender, messages_dict, msg, tick_mark, sending_clock)

        user = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//span[@title = "{}"]'.format(default_contact))))
        user.click()
        # save_localstorage(driver, LOCALSTORAGE_PATH)
        time.sleep(5)
driver.close()