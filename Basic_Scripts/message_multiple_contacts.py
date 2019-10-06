from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC


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
    
    
options = driver.find_element_by_xpath('//div[@title="Menu"]')
options.click()
logout_xpath = '/html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[3]/span/div/ul/li[6]/div'
WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, logout_xpath)))
logout = driver.find_element_by_xpath(logout_xpath)
logout.click()
