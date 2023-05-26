from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import username, password
import time
import random


# def login(username, password):
#     service = Service('../chromedriver/chromedriver.exe')
#     browser = webdriver.Chrome(service=service)
#
#     try:
#         browser.get("https://www.instagram.com/")
#         time.sleep(random.randrange(3, 5))
#
#         username_input = browser.find_element(By.NAME, 'username')
#         username_input.clear()
#         username_input.send_keys(username)
#
#         time.sleep(2)
#
#         passowrd_input = browser.find_element(By.NAME, 'password')
#         passowrd_input.clear()
#         passowrd_input.send_keys(password)
#
#         passowrd_input.send_keys(Keys.ENTER)
#         time.sleep(10)
#
#         browser.close()
#         browser.quit()
#     except Exception as ex:
#         print(ex)
#         browser.close()
#         browser.quit()
#
#
# login(username, password)

def hashtag_search(username, password, hashtag):
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
        time.sleep(5)

        try:
            browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
            time.sleep(5)

            for i in range(1, 3 + 1):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(3, 5))

            hrefs = browser.find_elements(By.TAG_NAME, 'a')
            posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]


            # posts_urls = []
            # for item in hrefs:
            #     href = item.get_attribute('href')
            #
            #     if "/p/" in href:
            #         posts_urls.append(href)
            #         print(href)

            for url in posts_urls:
                try:
                    browser.get(url)
                    like_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/span[1]/button")))
                    like_button.click()
                    time.sleep(random.randrange(80, 100))
                except Exception as ex:
                    print(ex)

            browser.close()
            browser.quit()
        except Exception as ex:
            print(ex)
            browser.close()
            browser.quit()

    except Exception as ex:
        print(ex)
        browser.close()
        browser.quit()


hashtag_search(username, password, 'surfing')