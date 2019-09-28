from selenium import webdriver
import os

driver = webdriver.Chrome(r"add path to driver here")
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
while inp != "":
    name = input('Enter the name of user or group : ')
    msg = input('Enter your message : ')
    count = int(input('Enter the count : '))
    send_msg(driver, name, msg, count)
    inp = input('Enter 1 to continue: ')
    
options = driver.find_element_by_xpath('//div[@title="Menu"]')
options.click()
logout = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[3]/span/div/ul/li[6]/div')
time.sleep(2)
logout.click()
