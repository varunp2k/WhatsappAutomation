from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import urllib.request
import time
import pickle

#emoji 
#This code is taken from https://gist.github.com/shello/efa2655e8a7bce52f273 all credits to the author

from itertools import accumulate
from bisect import bisect
from random import randrange
from unicodedata import name as unicode_name

# Set the unicode version.
# Your system may not support Unicode 7.0 charecters just yet! So hipster.
UNICODE_VERSION = 6

# Sauce: http://www.unicode.org/charts/PDF/U1F300.pdf

EMOJI_RANGES_UNICODE = {
    6: [
        ('\U0001F300', '\U0001F320'),
        ('\U0001F330', '\U0001F335'),
        ('\U0001F337', '\U0001F37C'),
        ('\U0001F380', '\U0001F393'),
        ('\U0001F3A0', '\U0001F3C4'),
        ('\U0001F3C6', '\U0001F3CA'),
        ('\U0001F3E0', '\U0001F3F0'),
        ('\U0001F400', '\U0001F43E'),
        ('\U0001F440', ),
        ('\U0001F442', '\U0001F4F7'),
        ('\U0001F4F9', '\U0001F4FC'),
        ('\U0001F500', '\U0001F53C'),
        ('\U0001F540', '\U0001F543'),
        ('\U0001F550', '\U0001F567'),
        ('\U0001F5FB', '\U0001F5FF')
    ],
    7: [
        ('\U0001F300', '\U0001F32C'),
        ('\U0001F330', '\U0001F37D'),
        ('\U0001F380', '\U0001F3CE'),
        ('\U0001F3D4', '\U0001F3F7'),
        ('\U0001F400', '\U0001F4FE'),
        ('\U0001F500', '\U0001F54A'),
        ('\U0001F550', '\U0001F579'),
        ('\U0001F57B', '\U0001F5A3'),
        ('\U0001F5A5', '\U0001F5FF')
    ],
    8: [
        ('\U0001F300', '\U0001F579'),
        ('\U0001F57B', '\U0001F5A3'),
        ('\U0001F5A5', '\U0001F5FF')
    ]
}

NO_NAME_ERROR = '(No name found for this codepoint)'

def random_emoji(unicode_version = 6):
    if unicode_version in EMOJI_RANGES_UNICODE:
        emoji_ranges = EMOJI_RANGES_UNICODE[unicode_version]
    else:
        emoji_ranges = EMOJI_RANGES_UNICODE[-1]

    # Weighted distribution
    count = [ord(r[-1]) - ord(r[0]) + 1 for r in emoji_ranges]
    weight_distr = list(accumulate(count))

    # Get one point in the multiple ranges
    point = randrange(weight_distr[-1])

    # Select the correct range
    emoji_range_idx = bisect(weight_distr, point)
    emoji_range = emoji_ranges[emoji_range_idx]

    # Calculate the index in the selected range
    point_in_range = point
    if emoji_range_idx is not 0:
        point_in_range = point - weight_distr[emoji_range_idx - 1]

    # Emoji 
    emoji = chr(ord(emoji_range[0]) + point_in_range)
    emoji_name = unicode_name(emoji, NO_NAME_ERROR).capitalize()
    emoji_codepoint = "U+{}".format(hex(ord(emoji))[2:].upper())

    return (emoji, emoji_codepoint, emoji_name)
emoji_send =random_emoji(UNICODE_VERSION)[0]

print(emoji_send)
# PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
# LOCALSTORAGE_PATH = "localstorages.pkl"

# browser = "chrome"
# if "firefox" in browser.lower():
#     driver = webdriver.Firefox(executable_path = os.path.join(PROJECT_ROOT, "geckodriver"))
# elif "chrome" in browser.lower():
#     driver = webdriver.Chrome(executable_path = os.path.join(PROJECT_ROOT, "chromedriver"))
# def save_localstorage(driver, path):
#     with open(path, 'wb') as filehandler:
#         localstorage = dict(driver.execute_script( \
#             "var ls = window.localStorage, items = {}; " \
#             "for (var i = 0, k; i < ls.length; ++i) " \
#             "  items[k = ls.key(i)] = ls.getItem(k); " \
#             "return items; "))
#         pickle.dump(localstorage, filehandler)

# def load_localstorage(driver, path):
#      with open(path, 'rb') as localstoragesfile:
#          localstorages = dict(pickle.load(localstoragesfile))
#          for key, value in localstorages.items():
#             #  driver.add_localstorage(localstorage)
#             driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", key, value)
# # print("1. Load localstorages\n2. Don't load localstorages\nInput: ", end="")
# # choice = int(input())
# driver.get('https://web.whatsapp.com/')
# # if choice == 1:
# if os.path.isfile(LOCALSTORAGE_PATH):
#     load_localstorage(driver, LOCALSTORAGE_PATH)
# driver.get(driver.current_url)
# default_contact = "A1"
# messages_dict = {"hi": "Hello", "ok": "OK", "namaste": "Saadar pranam", "hello":"Hi"}

# def send_msg(driver, name, msg, count):
#     print("Sending message: '%s' to %s" % (msg, name))
#     start = time.time()
#     # user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
#     print("Time to find element: {} s".format(time.time() - start))
#     start = time.time()
#     user = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//span[@title = "{}"]'.format(name))))
#     user.click()
#     print("Time to click: {} s".format(time.time() - start))

#     start = time.time()
#     msg_box = driver.find_element_by_class_name('_3u328')
#     print("Time to find message box: {} s".format(time.time() - start))

    
#     for i in range(count):
#         start = time.time()
#         msg_box.send_keys(msg)
#         print("Time to type message: {} s".format(time.time() - start))
#         start = time.time()
#         button = driver.find_element_by_class_name('_3M-N-')
#         button.click()
#         print("Time to send message: {} s".format(time.time() - start))

# def reply_to_messages(driver, name, messages_dict, msg, tick_mark, sending_clock):
#     # print(msg)
#     if(msg == "typing..."):
#         return
#     for message, reply in messages_dict.items():
#         if msg.lower() == message and tick_mark == [] and sending_clock == []:
#             send_msg(driver, msg_sender, reply, 1)
#             break

# # input("Press any key after loading")
# # img = driver.find_element_by_xpath("//img[@alt='Scan me!']")
# # src = img.get_attribute('src')
# # urllib.request.urlretrieve(src, "captcha.png")
# inp = " "
# # input("Press any key after QR code scan")
# WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]')))
# save_localstorage(driver, LOCALSTORAGE_PATH)
# allchats = driver.find_elements_by_xpath("//div[contains(@style, 'z-index')]")
# allchats = [chat.get_attribute("style") for chat in allchats]
# allchats = [int(chat.split("z-index: ")[1].split(";")[0]) for chat in allchats]
# while inp != "":
#     while True:
#         msg = driver.find_element_by_xpath("//div[contains(@style,'z-index: ')]//span[@dir='ltr']").text
#         print("msg first:", msg)
#         msg_sender = driver.find_element_by_xpath("//div[contains(@style,'z-index: ')]//span[@dir='auto']").get_attribute("title")
#         # print(msg_sender)
#         new_msg = driver.find_elements_by_xpath("//div[contains(@style,'z-index: ')]//span[@class='P6z4j']")
#         # print(new_msg)
#         # tick_mark = driver.find_elements_by_xpath("//div[contains(@style,'z-index: ')]//span[@data-icon='status-dblcheck']")
#         tick_mark_user = driver.find_element_by_xpath("//div[contains(@style,'z-index: ')]")
#         tick_mark = tick_mark_user.find_elements_by_xpath(".//span[contains(@data-icon,'status-dblcheck')]")
#         sending_clock = tick_mark_user.find_elements_by_xpath(".//span[contains(@data-icon,'status-time')]")
#         # print("Tick mark first:", tick_mark)
#         reply_to_messages(driver, msg_sender, messages_dict, msg, tick_mark, sending_clock)
#         for i in allchats:
#             try: 
#                 msg = driver.find_element_by_xpath("//div[contains(@style,'z-index: {};')]//span[@dir='ltr']".format(i)).text
#                 print("msg {}:".format(i), msg)
#                 msg_sender = driver.find_element_by_xpath("//div[contains(@style,'z-index: {};')]//span[@dir='auto']".format(i)).get_attribute("title")
#                 # print(msg_sender)
#                 new_msg = driver.find_elements_by_xpath("//div[contains(@style,'z-index: {};')]//span[@class='P6z4j']".format(i))
#                 # print(new_msg)
#                 # tick_mark = driver.find_elements_by_xpath("//div[contains(@style,'z-index: {};')]//span[@data-icon='status-dblcheck']".format(i))
#                 # # print(tick_mark)
#                 tick_mark_user = driver.find_element_by_xpath("//div[contains(@style,'z-index: {};')]".format(i))
#                 tick_mark = tick_mark_user.find_elements_by_xpath(".//span[contains(@data-icon,'status-dblcheck')]")
#                 sending_clock = tick_mark_user.find_elements_by_xpath(".//span[contains(@data-icon,'status-time')]")
#                 print("Tick mark {}:".format(i), tick_mark)
#             except selenium.common.exceptions.NoSuchElementException as e:
#                 print(e)
#                 continue
#             reply_to_messages(driver, msg_sender, messages_dict, msg, tick_mark, sending_clock)

#         user = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//span[@title = "{}"]'.format(default_contact))))
#         user.click()
#         # save_localstorage(driver, LOCALSTORAGE_PATH)
#         WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@class='_3HZor']/span[@title='{}']".format(msg_sender))))
# driver.close()