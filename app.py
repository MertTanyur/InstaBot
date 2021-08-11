from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

USERNAME = ''
PASSWORD = ''
# you have to install chrome driver
DRIVER_PATH = ''


class InstaBot:

    def __init__(self, username, password, driver_path):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome(executable_path=driver_path)
        self.post_links = []
        self.post_statistics = {}

    def login(self):
        self.driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(5)
        username = self.driver.find_element_by_name('username')
        password = self.driver.find_element_by_name('password')

        username.send_keys(self.username)
        password.send_keys(self.password)
        time.sleep(2)
        password.send_keys(Keys.ENTER)

        time.sleep(5)
        button = self.driver.find_element_by_css_selector('.cmbtv button')
        button.click()

        time.sleep(3)
        button = self.driver.find_element_by_css_selector('.HoLwm')
        button.click()

    def find_followers(self):
        pass

    def follow(self):
        pass

    def retrieve_a_profile(self, any_username):
        span = self.driver.find_element_by_xpath(
            '/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[1]/div/span[2]')
        span.click()
        time.sleep(1)
        place_holder = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')

        place_holder.send_keys(any_username)
        time.sleep(5)
        first_result = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]')
        first_result.click()
        time.sleep(2)
        self.list_all_posts()

    def list_all_posts(self):
        posts_list = []
        post_links = []
        rows = self.driver.find_elements_by_css_selector('.Nnq7C')
        for row in rows:
            elements = row.find_elements_by_css_selector('.v1Nh3')
            for element in elements:
                posts_list.append(element)

        # print(posts_list)
        for element in posts_list:

            post_links.append(element.find_element_by_tag_name(
                'a').get_attribute('href'))
        self.post_links = post_links
        return post_links

    def find_likers(self, post_link, repeating=False):
        # opening likes modal
        like_anchor = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[2]/div/div/a')
        like_anchor.click()
        time.sleep(2)
        long_list = self.driver.find_element_by_xpath(
            '/html/body/div[6]/div/div/div[2]/div')
        # counting likers
        username_set = set()
        username_list = []
        # print(elements_list)
        for i in range(1, 3000):
            last_height = 0
            for element in long_list.find_elements_by_css_selector('div span a'):
                username = element.get_attribute('title')
                username_set.add(username)
                if username not in username_list:
                    username_list.append(username)
            last_height = self.driver.execute_script(
                'return arguments[0].scrollTop', long_list)
            self.driver.execute_script(
                'arguments[0].scrollTop = arguments[0].offsetHeight * arguments[1]', long_list, i)
            time.sleep(0.05)
            print(f'i is -> {i}')
            if self.driver.execute_script('return arguments[0].scrollTop', long_list) == last_height:
                break
        if len(username_list) == 0 and not repeating:
            self.find_likers(post_link, repeating=True)
        else:
            self.post_statistics[post_link]['liked_users'] = username_list

            print(username_list)
            print(f'len of username list is -> {len(username_list)}')

    def visit_posts_and_analyze_likers(self):
        print(f'recorded posts links are -> {self.post_links}')
        if len(self.post_links) != 0:
            for link in self.post_links:
                self.post_statistics[link] = {
                    'liked_users': [],
                    'post_description': '',
                    'post_image_link': ''
                }
                self.driver.get(link)
                time.sleep(2)
                self.find_likers(link)
                time.sleep(2)

        print(self.post_statistics)


bot = InstaBot(USERNAME, PASSWORD, DRIVER_PATH)

bot.login()

bot.retrieve_a_profile('porscheturkiye')
bot.visit_posts_and_analyze_likers()
