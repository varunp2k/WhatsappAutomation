from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import sys
scriptpath = "path to emoji script"
sys.path.append(os.path.abspath(scriptpath))
import random_emoji_generator

emoji = (random_emoji_generator.random_emoji(6)[0])

driver = webdriver.Firefox(
        executable_path=os.path.join(scriptpath, "geckodriver"))
driver.get('https://web.whatsapp.com/')

def send_msg(driver, name, msg, count):
    user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
    user.click()

    msg_box = driver.find_element_by_class_name('_3u328')

    for i in range(count):
        msg_box.send_keys(msg)
        button = driver.find_element_by_class_name('_3M-N-')
        button.click()
    
def open_chat(driver, name):
    is_existent_chat_found = open_existent_chat(driver, name)
    if not is_existent_chat_found:
        return open_new_chat(driver, name)
    return True

def open_existent_chat(driver, name):
    try:
        user = driver.find_element_by_xpath(
            '//span[@title = "{}"]'.format(name))
        user.click()
    except selenium.common.exceptions.NoSuchElementException:
        return False
    return True

def clear_search(driver):
    clear_button = driver.find_element_by_class_name('_2heX1')
    clear_button.click()

def open_new_chat(driver, name):
    search_box = driver.find_element_by_xpath(
        '//div[@id="side"]//input[@title="Search or start new chat"]')
    search_box.send_keys(name)
    user_xpath = '//div[contains(@style, "translateY(72px);")]//span[@title = "{}"]'.format(name)
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, user_xpath)))
        user = driver.find_element_by_xpath(user_xpath)
        user.click()
    except selenium.common.exceptions.TimeoutException:
        return False
    return True

def send_msg(driver, name, msg, count):
    is_user_found = open_chat(driver, name)
    if not is_user_found:
        clear_search(driver)
        return print(f'contact {name} not found')
    msg_box = driver.find_element_by_class_name('_3u328')

    for i in range(count):
        msg_box.send_keys(msg)
        button = driver.find_element_by_class_name('_3M-N-')
        button.click()

def emoji_reply(driver, name, emoji):
    is_user_found = open_chat(driver, name)
    if not is_user_found:
        clear_search(driver)
        return print(f'contact {name} not found')

inp = " "
input("Press any key after QR code scan")
while inp != "":
    name = input('Enter the name of user or group : ')
    send_msg(driver, name, emoji, 1)
    
