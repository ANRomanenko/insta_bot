from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from config import username, password
import time
import random


def login(username, password):
    service = Service('../chromedriver/chromedriver.exe')
    browser = webdriver.Chrome(service=service)

    try:
        browser.get("https://www.instagram.com/")
        time.sleep(random.randrange(3, 5))

        username_input = browser.find_element(By.NAME, 'username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(2)

        passowrd_input = browser.find_element(By.NAME, 'password')
        passowrd_input.clear()
        passowrd_input.send_keys(password)

        passowrd_input.send_keys(Keys.ENTER)
        time.sleep(10)

        browser.close()
        browser.quit()
    except Exception as ex:
        print(ex)
        browser.close()
        browser.quit()


login(username, password)