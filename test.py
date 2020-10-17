from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class Bot(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://blackfriday.ro/')


# bot = Bot()
# bot.driver.find_element_by_css_selector('html body section#sticky_parent div.wrap div.table >  section:nth-child(1)  a')
