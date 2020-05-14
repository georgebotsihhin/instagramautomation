from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from random import randrange, choice, randint
from time import sleep
from selectors import get_selectors
import re

class Instagram():

    def __init__(self, username, password, headless=True, hashtags=None, comments=None, limits=None):
        self.username = username
        self.password = password
        self.hashtags = hashtags
        self.comments = comments
        self.limits = limits

        self.task_counter = 1
        # Initial user data on bot start
        self.initial_followers = 0
        self.initial_following = 0

        # User data after bot finished
        self.followers_goal = 0
        self.likes_goal = 0
        self.comments_goal = 0

        # Current data
        self.current_followers = 0
        self.current_likes = 0
        self.current_comments = 0

        # Bot results
        self.total_likes = 0
        self.total_new_following = 0
        self.total_new_followers = 0
        self.total_comments = 0

        self.need_to_like = True
        self.need_to_follow = True
        self.need_to_comment = False

        self.task_achieved = False

        self.comment_default = 'Очень здорово!'
        self.chromedriver_path = './chromedriver'
        self.logfile = 'log.dat'
        self.logged_in = False
        self.driver_options = Options()
        self.driver_options.add_argument('--disable-notifications')
        self.driver_options.add_argument('--no-sandbox')
        self.driver_options.add_argument('--disable-software-rasterizer')
        self.driver_options.add_argument('--headless')
        self.driver_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(executable_path=self.chromedriver_path, options=self.driver_options)
        self.selectors = get_selectors()

    def login(self):
        self.driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')

        self.__sleep__(3, 8)
        username = self.driver.find_element_by_name(self.selectors['username'])
        username.send_keys(self.username)
        print(f'Signing in as {self.username}')

        self.__sleep__(2, 7)
        password = self.driver.find_element_by_name(self.selectors['password'])
        password.send_keys(self.password)

        self.__sleep__(1, 5)
        button_login = self.driver.find_element_by_css_selector(self.selectors['button_login'])
        print(f'Attempting to sign in...')
        self.__sleep__()
        button_login.click()

        error_occured = self.is_login_error()

        if error_occured:
            print(f'Login failed, error occured: {error_occured}')
            return False
        else:
            print(f'Login succeeded')
            self.logged_in=True
            fix_popup = self.notification_popup_click()
            if fix_popup:
                print('Notification settings applied')
            return True

    def __replace__(self, text, dic):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    def get_self_profile_link(self):
        rep = {'replacethistring': self.username}
        selector = self.__replace__(self.selectors['self_profile'], rep)
        return selector

    def is_login_error(self):
        try:
            error_message = self.driver.find_element(By.ID, self.selectors['login_error']).text
        except NoSuchElementException:
            return False
        return error_message

    def notification_popup_click(self):
        try:
            self.__sleep__()
            decline = self.driver.find_element_by_css_selector(self.selectors['notification_btn'])
            decline.click()
        except NoSuchElementException:
            return False
        return True

    def check_page_exists(self, path):
        self.driver.get(path)
        ret = True
        try:
            self.__sleep__(2, 5)
            error = self.driver.find_element_by_css_selector(self.selectors['page_exists_err']).text
            if 'sorry' in error.lower():
                ret = False
        except NoSuchElementException:
            ret = True

        self.__sleep__(3, 5)
        return ret

    def check_is_private_account(self, path):
        self.driver.get(path)
        ret = False
        try:
            self.__sleep__()
            error = self.driver.find_element_by_css_selector(self.selectors['private_account_err']).text
            if 'private' in error.lower():
                ret = True
        except NoSuchElementException:
            ret = False

        self.__sleep__(1, 5)
        return ret

    def generate_hashtag_link(self, num):
        if num > 0 and num < 10:
            if num == 1:
                rep = {'replacethisfirstnum': '3', 'replacethisecondnum': '1', 'replacethisthirdnum': str(num)}
                return self.__replace__(self.selectors['hashtag_link'], rep)
            elif num == 2:
                rep = {'replacethisfirstnum': '3', 'replacethisecondnum': '1', 'replacethisthirdnum': str(num)}
                return self.__replace__(self.selectors['hashtag_link'], rep)
            elif num == 3:
                rep = {'replacethisfirstnum': '3', 'replacethisecondnum': '1', 'replacethisthirdnum': str(num)}
                return self.__replace__(self.selectors['hashtag_link'], rep)
            elif num == 4:
                rep = {'replacethisfirstnum': '3', 'replacethisecondnum': '2', 'replacethisthirdnum': '1'}
                return self.__replace__(self.selectors['hashtag_link'], rep)
            elif num == 5:
                rep = {'replacethisfirstnum': '3', 'replacethisecondnum': '2', 'replacethisthirdnum': '2'}
                return self.__replace__(self.selectors['hashtag_link'], rep)
            elif num == 6:
                rep = {'replacethisfirstnum': '3', 'replacethisecondnum': '2', 'replacethisthirdnum': '3'}
                return self.__replace__(self.selectors['hashtag_link'], rep)
            elif num == 7:
                rep = {'replacethisfirstnum': '3', 'replacethisecondnum': '3', 'replacethisthirdnum': '1'}
                return self.__replace__(self.selectors['hashtag_link'], rep)
            elif num == 8:
                rep = {'replacethisfirstnum': '3', 'replacethisecondnum': '3', 'replacethisthirdnum': '2'}
                return self.__replace__(self.selectors['hashtag_link'], rep)
            else:
                rep = {'replacethisfirstnum': '3', 'replacethisecondnum': '3', 'replacethisthirdnum': '3'}
                return self.__replace__(self.selectors['hashtag_link'], rep)
        else:
            rep = {'replacethisfirstnum': '3', 'replacethisecondnum': '1', 'replacethisthirdnum': '1'}
            return self.__replace__(self.selectors['hashtag_link'], rep)

    def generate_random_comment(self):
        if self.comments and len(self.comments) > 0:
            random_comment = choice(self.comments)
            print(f'Random comment chosen {random_comment}')
            return random_comment
        else:
            print('Self comments not found, using default in generate_random_comment()')
            return self.comment_default

    def comment_by_page(self, page, comment):
        if self.check_page_exists(page):
            self.__sleep__(2, 7)

            try:
                comment_area = self.driver.find_element_by_css_selector(self.selectors['comment_textarea'])
                comment_area.click()

                self.__sleep__(1, 6)
                comment_area = self.driver.find_element_by_css_selector(self.selectors['comment_textarea'])
                comment_area.send_keys(comment)
                comment_area.send_keys(Keys.ENTER)
                print(f'Saved a comment under {page}')

                self.current_comments += 1

                self.__sleep__()
                print('Return back to profile')
                self.driver.get(self.get_self_profile_link())
                return True
            except NoSuchElementException:
                print('No comment area found')
                self.driver.get(self.get_self_profile_link())
                return False
        else:
            self.__sleep__()
            print(f'{page} does not exist. Cannot perform comment_by_page() task')
            self.driver.get(self.get_self_profile_link())
            return False

    def comment_random_hashtag(self):
        print(f'TASK {self.task_counter} execute comment_random_hashtag()')
        random_hashtag = None
        if self.hashtags and len(self.hashtags) > 0:
            random_hashtag = choice(self.hashtags)
            print(f'Chosen hashtag {random_hashtag}')
            self.__sleep__(2, 6)
            rep = {'replacethistring': random_hashtag}
            self_selector = self.selectors['tag_url']

            selector = self.__replace__(self_selector, rep)
            if self.check_page_exists(selector):
                rnd = randint(1, 3)
                if rnd ==  3:
                    self.append_to_hashtags()

                self.__sleep__(1, 7)
                thumbnail_number = randint(1, 9)
                thumbnail = self.driver.find_element_by_css_selector(self.generate_hashtag_link(thumbnail_number))
                thumbnail_href = thumbnail.get_attribute('href')

                print(f'chosen photo to comment {thumbnail_href}')
                self.__sleep__()
                comment = self.generate_random_comment() or self.comment_default
                if self.comment_by_page(thumbnail_href, comment):
                    self.task_counter += 1
            else:
                print(f'{web_url} does not exist. Cannot perform comment_random_hashtag() task')
                self.driver.get(self.get_self_profile_link())
                return False
        else:
            print('Hashtags length equals to zero. Cannot perform comment_random_hashtag() task')
            return False

        return True


    def like_by_page(self, page):
        if self.check_page_exists(page):
            self.__sleep__(7, 10)
            like_photo = self.driver.find_element_by_css_selector(self.selectors['like_btn'])
            self.__sleep__()
            like_photo.click()

            print(f'Liked photo thumbail {page}')
            self.current_likes += 1
            self.__sleep__(3, 5)
            print('Return back to profile')
            self.driver.get(self.get_self_profile_link())
            return True
        else:
            self.__sleep__()
            print(f'{page} does not exist. Cannot perform like_by_page() task')
            self.driver.get(self.get_self_profile_link())
            return False

    def like_random_hashtag(self):
        print(f'TASK {self.task_counter} execute like_random_hashtag()')
        random_hashtag = None
        if self.hashtags and len(self.hashtags) > 0:
            random_hashtag = choice(self.hashtags)
            print(f'Chosen hashtag {random_hashtag}')
            self.__sleep__()

            rep = {'replacethistring': str(random_hashtag)}
            selector = self.__replace__(self.selectors['tag_url'], rep)

            if self.check_page_exists(selector):
                rnd = randint(1, 5)
                if rnd ==  3:
                    self.append_to_hashtags()

                self.__sleep__(3, 5)
                thumbnail_number = randint(1, 9)
                thumbnail = self.driver.find_element_by_css_selector(self.generate_hashtag_link(thumbnail_number))
                thumbnail_href = thumbnail.get_attribute('href')

                print(f'chosen photo to like {thumbnail_href}')
                if self.like_by_page(thumbnail_href):
                    self.task_counter += 1
            else:
                print(f'{web_url} does not exist. Cannot perform like_random_hashtag() task')
                self.driver.get(self.get_self_profile_link())
                return False
        else:
            print('Hashtags length equals to zero. Cannot perform like_random_hashtag() task')
            return False

        return True

    def append_to_hashtags(self):
        print(f'Current hashtags {self.hashtags}')
        try:
            hashtag_string = self.driver.find_element_by_xpath(self.selectors['hashtag_string'])
            print(f'Found hashtags {hashtag_string.text}')
            links = hashtag_string.find_elements_by_css_selector('div > a')
            for link in links:
                hashtag = link.text.replace('#', '')
                print(f'Appending hashtag {hashtag}')
                self.hashtags.append(hashtag)
            print(f'New hashtags {self.hashtags}')

        except NoSuchElementException:
            print('No hashtag string found')


    def follow_random_hashtag(self):
        print(f'TASK {self.task_counter} execute follow_random_hashtag()')
        random_hashtag = None
        if self.hashtags and len(self.hashtags) > 0:
            random_hashtag = choice(self.hashtags)
            print(f'Chosen hashtag {random_hashtag}')
            self.__sleep__()

            rep = {'replacethistring': str(random_hashtag)}
            selector = self.__replace__(self.selectors['tag_url'], rep)

            if self.check_page_exists(selector):
                rnd = randint(3, 8)
                if rnd ==  3:
                    self.append_to_hashtags()

                self.__sleep__(1, 6)
                thumbnail_number = randint(1, 9)
                thumbnail = self.driver.find_element_by_css_selector(self.generate_hashtag_link(thumbnail_number))
                thumbnail_href = thumbnail.get_attribute('href')

                self.__sleep__(1, 3)
                self.driver.get(thumbnail_href)
                self.__sleep__(7, 10)
                profile = self.driver.find_element_by_xpath(self.selectors['hashtag_follow']).get_attribute('href')
                self.__sleep__()

                print(f'chosen person to follow {profile}')
                self.__sleep__()
                if self.follow_by_page(profile):
                    self.task_counter += 1
            else:
                print(f'{web_url} does not exist. Cannot perform like_random_hashtag() task')
                self.driver.get(self.get_self_profile_link())
                return False
        else:
            print('Hashtags length equals to zero. Cannot perform like_random_hashtag() task')
            return False

        return True

    def get_random_suggestion_link(self):
        random_int = randint(1, 20)
        random_int_s = str(random_int)

        rep = {'replacethisStringse': str(random_int_s)}
        selector = self.__replace__(self.selectors['suggestion_selector'], rep)

        get_profile = self.driver.find_element_by_css_selector(selector)
        if get_profile.text:
            return get_profile.text
        else:
            return None

    def follow_by_page(self, page):
        if self.check_page_exists(page):
            self.__sleep__(1, 4)
            try:
                follow_btn = self.driver.find_element_by_xpath(self.selectors['follow_btn'])
            except NoSuchElementException:
                follow_btn = self.driver.find_element_by_xpath(self.selectors['follow_btn_b'])
            self.__sleep__()

            follow_btn.click()
            self.current_followers += 1
            print(f'Followed account {page} successfully. Redirect back to main profile.')

            self.__sleep__(2, 5)
            self.driver.get(self.get_self_profile_link())
            return True
        else:
            self.__sleep__()
            print(f'{page} does not exist. Cannot perform follow_by_page() task')
            self.driver.get(self.get_self_profile_link())
            return False

    def random_follow_from_suggestions(self):
        print(f'TASK {self.task_counter} execute random_follow_from_suggestions()')
        self.__sleep__()
        if self.check_page_exists(self.selectors['get_suggested_url']):
            self.__sleep__(1, 4)
            get_profile = self.get_random_suggestion_link()
            if get_profile:
                rep = {'replacethistring': get_profile}
                profile_url = self.__replace__(self.selectors['self_profile'], rep)
                if self.follow_by_page(profile_url):
                    self.task_counter += 1
            else:
                print('error, profile not found. redirect back to main profile')
                self.__sleep__()
                self.driver.get(self.get_self_profile_link())
                return False
        else:
            self.__sleep__()
            print(f'{web_url} does not exist. Cannot perform random_follow_from_suggestions() task')
            self.driver.get(self.get_self_profile_link())
            return False

    def __sleep__(self, min=None, max=None):
        if min and max:
            timeDelay = randrange(min, max)
            sleep(timeDelay)
            print(f'Sleep {timeDelay} sec')
        elif min and not max:
            sleep(min)
            print(f'Sleep {min} sec')
        else:
            sleep(1)
            print(f'Sleep 1 sec')

    def like_feed_posts(self, limit=5):
        self.driver.get(self.selectors['insta'])
        self.__sleep__(3, 5)
        posts = self.driver.find_elements_by_css_selector(self.selectors['feed_posts'])
        posts_count = len(posts)
        if limit > 0 and posts_count > limit:
            posts_count = limit
        self.__sleep__(3, 10)
        for i in range(1, posts_count):
            self.__sleep__(1, 3)
            counter = 1
            for post in posts:
                self.__sleep__(3, 5)
                like_btn = post.find_element_by_css_selector(self.selectors['feed_post'])
                like_btn_color = like_btn.find_element_by_css_selector('svg').get_attribute('fill')
                if like_btn_color != self.selectors['liked_color']:
                    like_btn.click()
                    self.current_likes += 1
                    print(f'Liked photo #{counter} on feed')
                    self.__sleep__(2, 5)
                    counter += 1
                else:
                    print(f'Photo #{i} is already liked')
                    pass
                self.__sleep__()

    def __scrolldown__(self):
        self.driver.execute_script(self.selectors['scroll_to_btm'])
        self.__sleep__()
