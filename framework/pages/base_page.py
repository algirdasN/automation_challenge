import logging

from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

log = logging.getLogger("framework")


class BasePage:

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5, 0.1)
