from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import username, password
from selenium.common.exceptions import NoSuchElementException
import requests
import time
import random


class InstagramBot():
    def __init__(self, username, password):

        self.username = username
        self.password = password
        s = Service('../chromedriver/chromedriver.exe')
        self.browser = webdriver.Chrome(service=s)

    def close_browser(self):

        self.browser.close()
        self.browser.quit()

    def login(self):

        browser = self.browser
        browser.get("https://www.instagram.com/")
        time.sleep(random.randrange(3, 5))

        username_input = browser.find_element(By.NAME, 'username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(2)

        password_input = browser.find_element(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)
        time.sleep(10)

    def like_photo_by_hashtag(self, hashtag):

        browser = self.browser
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)

        for i in range(1, 3 + 1):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 5))

        hrefs = browser.find_elements(By.TAG_NAME, 'a')
        posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

        for url in posts_urls:
            try:
                browser.get(url)
                like_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                               "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/span[1]/button")))
                like_button.click()
                time.sleep(random.randrange(80, 100))
            except Exception as ex:
                print(ex)
                self.close_browser()

    # проверяем по xpath существует ли элемент на странице

    def xpath_exists(self, url):

        browser = self.browser
        try:
            browser.find_element(By.XPATH, url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    # ставим лайк на пост по рямой ссылке

    def put_exactly_like(self, userpost):

        browser = self.browser
        browser.get(userpost)
        time.sleep(4)

        wrong_userpage = "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/span"
        if self.xpath_exists(wrong_userpage):
            print('Такого поста не существует, проверьте URL')
            self.close_browser()
        else:
            print("Пост успешно найдет, ставим лайк!")
            time.sleep(2)

            like_button = "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/span/button"
            like_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, like_button)))
            like_button.click()

            print(f"Лайк на пост: {userpost} поставлен!")
            self.close_browser()

    # метод собирает ссылки все посты пользователя
    def get_all_posts_urls(self, userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)

        wrong_userpage = "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/span"
        if self.xpath_exists(wrong_userpage):
            print('Такого пользователя не существует, проверьте URL')
            self.close_browser()
        else:
            print("Пользователь успешно найдет, ставим лайки!")
            time.sleep(2)

            posts_count = int(browser.find_element(By.XPATH,
                                                   "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[1]/span").text)
            loops_count = int(posts_count / 12)
            print(loops_count)

            posts_urls = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements(By.TAG_NAME, 'a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

                for href in hrefs:
                    posts_urls.append(href)

                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(2, 4))
                print(f"Итерация # {i}")

            file_name = userpage.split("/")[-2]
            with open(f"{file_name}.txt", 'a') as file:
                for posts_url in posts_urls:
                    file.write(posts_url + "\n")

            set_posts_urls = set(posts_urls)
            set_posts_urls = list(set_posts_urls)

            with open(f"{file_name}_set.txt", 'a') as file:
                for post_url in set_posts_urls:
                    file.write(post_url + '\n')

    # ставим лайки по ссылке на аккаунт пользователя
    def put_many_likes(self, userpage):

        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(4)
        browser.get(userpage)
        time.sleep(4)

        with open(f"{file_name}_set.txt") as file:
            urls_list = file.readlines()

            for post_url in urls_list: # [0:6]
                try:
                    browser.get(post_url)
                    time.sleep(2)

                    like_button = "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/span/button"
                    like_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, like_button)))
                    like_button.click()
                    # time.sleep(random.randrange(80, 100))
                    time.sleep(2)

                    print(f"Лайк на пост: {userpage} успешно поставлен!")
                except Exception as ex:
                    print(ex)
                    self.close_browser()

        self.close_browser()

    # метод скачивает контент со страницы пользователя
    def download_userpage_content(self, userpage):

        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(4)
        browser.get(userpage)
        time.sleep(4)

        img_and_video_src_urls = []
        with open(f"{file_name}_set.txt") as file:
            urls_list = file.readlines()

            for post_url in urls_list[0:10]: # [0:6]
                try:
                    browser.get(post_url)
                    time.sleep(4)

                    img_src = "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[1]/div/div/div/div/div/div/div[1]/img"
                    video_src = "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[1]/div/div/div/div/div/div/div/div/div/div/video"
                    post_id = post_url.split("/")[-2]

                    if self.xpath_exists(img_src):
                        img_src_url = browser.find_element(By.XPATH, img_src).get_attribute("src")
                        img_and_video_src_urls.append(img_src_url)

                        # сохраняем изображение
                        get_img = requests.get(img_src_url)
                        with open(f"{post_id}_img.jpg", "wb") as img_file:
                            img_file.write(get_img.content)

                    elif self.xpath_exists(video_src):
                        video_src_url = browser.find_element(By.XPATH, video_src).get_attribute("src")
                        img_and_video_src_urls.append(video_src_url)

                        # сохраняем видеофайл
                        get_video = requests.get(video_src_url, stream=True)
                        with open(f"{post_id}_video.mp4", "wb") as video_file:
                            for chunk in get_video.iter_content(chunk_size=1024 * 1024):
                                if chunk:
                                    video_file.write(chunk)

                    else:
                        # print("Упс! Что-то пошло не так!")
                        img_and_video_src_urls.append(f"{post_url}, нет ссылки")
                    print(f"Контент из поста {post_url} успешно скачен!")
                except Exception as ex:
                    print(ex)
                    self.close_browser()

            self.close_browser()
        with open("img_and_video_src_urls.txt", "a") as file:
            for i in img_and_video_src_urls:
                file.write(i + "\n")


my_bot = InstagramBot(username, password)
my_bot.login()
my_bot.download_userpage_content("https://www.instagram.com/numerolog.vlada/")
# my_bot.put_many_likes("https://www.instagram.com/numerolog.vlada/")
# my_bot.put_exactly_like("https://www.instagram.com/p/CgZbp1Nv11r5-0IfFYehosdWS1tWSy7bMxRfvk0/")
