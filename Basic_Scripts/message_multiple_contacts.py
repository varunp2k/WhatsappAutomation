from selenium import webdriver
import time

driver = webdriver.Chrome(r"add path to chrome driver here")
driver.get('https://web.whatsapp.com/')

def send_msg(driver, name, msg, count):
    user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
    user.click()

    msg_box = driver.find_element_by_class_name('_3u328')

    for i in range(count):
        msg_box.send_keys(msg)
        button = driver.find_element_by_class_name('_3M-N-')
        button.click()
    

inp = " "
input("Press any key after QR code scan")
contacts =("enter contact names here")
for i in contacts:
    name = i
    msg = "Good Morning!Hope you have a great day"
    count = 1
    send_msg(driver, name, msg, count)
    time.sleep(1.5)