from typing import List

from appium.webdriver import WebElement
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

from framework import utilities
from framework.pages.base_page import BasePage
from tests import log


class TimerPage(BasePage):

    @property
    def timer_views(self) -> List['WebElement']:
        return self.driver.find_elements_by_accessibility_id("TimerViewGrid")

    @property
    def edit_timers_button(self) -> WebElement:
        return self.driver.find_element_by_accessibility_id("EditTimersButton")

    @property
    def add_timer_button(self) -> WebElement:
        return self.driver.find_element_by_accessibility_id("AddTimerButton")

    def add_new_timer(self, name: str, hours: int = 0, minutes: int = 0, seconds: int = 0):
        log.info(f"Adding new timer: '{name}', '{hours:02}:{minutes:02}:{seconds:02}'")
        self.add_timer_button.click()
        new_timer_dialog = self.TimerDialog(self.driver)
        new_timer_dialog.set_duration(hours, minutes, seconds)
        new_timer_dialog.set_name(name)
        new_timer_dialog.save_button.click()

    def delete_all_timers(self):
        log.info("Deleting all timers.")
        self.edit_timers_button.click()

        for timer in self.timer_views:
            timer.find_element_by_accessibility_id("DeleteButton").click()

    def get_timer_by_name(self, name: str) -> WebElement:
        for timer in self.timer_views:
            if TimerPage.get_timer_name(timer) == name:
                return timer

        raise NoSuchElementException(f"Timer '{name}' was not found.")

    @staticmethod
    def get_timer_duration(timer: WebElement) -> str:
        timer_name = timer.find_element_by_accessibility_id("TimerValueText").get_attribute("Name")
        return utilities.parse_timer_text(timer_name)

    @staticmethod
    def get_timer_name(timer: WebElement) -> str:
        return timer.find_element_by_accessibility_id("TimerNameText").get_attribute("Name")

    class TimerDialog(BasePage):

        @property
        def hour_picker(self) -> WebElement:
            return self.root.find_element_by_name("hours")

        @property
        def minute_picker(self) -> WebElement:
            return self.root.find_element_by_name("minutes")

        @property
        def second_picker(self) -> WebElement:
            return self.root.find_element_by_name("seconds")

        @property
        def name_input_box(self) -> WebElement:
            return self.root.find_element_by_name("Timer name")

        @property
        def save_button(self) -> WebElement:
            return self.root.find_element_by_accessibility_id("PrimaryButton")

        @property
        def close_button(self) -> WebElement:
            return self.root.find_element_by_accessibility_id("CloseButton")

        def __init__(self, driver: WebDriver):
            super().__init__(driver)
            self.root = driver.find_element_by_accessibility_id("EditFlyout")

        def set_duration(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
            log.info(f"Setting timer duration to '{hours:02}:{minutes:02}:{seconds:02}'")
            hour_picker = self.hour_picker
            hour_picker.click()
            hour_picker.send_keys(hours)

            minute_picker = self.minute_picker
            minute_picker.click()
            minute_picker.send_keys(minutes)

            second_picker = self.second_picker
            second_picker.click()
            second_picker.send_keys(seconds)

        def set_name(self, name: str):
            log.info(f"Setting timer name to '{name}'")
            input_box = self.name_input_box
            input_box.click()
            input_box.send_keys(name)

        def submit(self):
            self.save_button.click()
            self.wait.until(lambda d: not self.root.is_displayed())
