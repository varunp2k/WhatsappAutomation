from selenium import webdriver
import selenium
import os
import urllib.request
import time

driver = webdriver.Chrome(r"add path to driver here")
driver.get('https://web.whatsapp.com/')

def send_msg(driver, name, msg, count):
    print("Sending message: '%s' to %s" % (msg, name))
    user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
    user.click()

    msg_box = driver.find_element_by_class_name('_3u328')

    for i in range(count):
        msg_box.send_keys(msg)
        button = driver.find_element_by_class_name('_3M-N-')
        button.click()

inp = " "
input("Press any key after QR code scan")
while inp != "":
    while True:
        msg = driver.find_element_by_xpath("//div[contains(@style,'z-index: ')]//span[@dir='ltr']").text
        # print(msg)
        msg_sender = driver.find_element_by_xpath("//div[contains(@style,'z-index: ')]//span[@dir='auto']").get_attribute("title")
        # print(msg_sender)
        new_msg = driver.find_elements_by_xpath("//div[contains(@style,'z-index: ')]//span[@class='P6z4j']")
        # print(new_msg)
        tick_mark = driver.find_elements_by_xpath("//div[contains(@style,'z-index: ')]//span[@data-icon='status-dblcheck']")
        # print(tick_mark)
        if msg.lower() == "hi" and tick_mark == []:
            send_msg(driver, msg_sender, "Hi", 1)
        elif msg.lower() == "ok" and tick_mark == []:
            send_msg(driver, msg_sender, "OK", 1)
        for i in [0,1,2,3,4,5]:
            try: 
                msg = driver.find_element_by_xpath("//div[contains(@style,'z-index: {}')]//span[@dir='ltr']".format(i)).text
                # print(msg)
                msg_sender = driver.find_element_by_xpath("//div[contains(@style,'z-index: {}')]//span[@dir='auto']".format(i)).get_attribute("title")
                # print(msg_sender)
                new_msg = driver.find_elements_by_xpath("//div[contains(@style,'z-index: {}')]//span[@class='P6z4j']".format(i))
                # print(new_msg)
                tick_mark = driver.find_elements_by_xpath("//div[contains(@style,'z-index: {}')]//span[@data-icon='status-dblcheck']".format(i))
                # print(tick_mark)
            except selenium.common.exceptions.NoSuchElementException as e:
                print(e)
                continue
            if msg.lower() == "hi" and tick_mark == []:
                send_msg(driver, msg_sender, "Hi", 1)
            elif msg.lower() == "ok" and tick_mark == []:
                send_msg(driver, msg_sender, "OK", 1)
        time.sleep(10)  
driver.close()