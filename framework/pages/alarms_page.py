from typing import List

from appium.webdriver import WebElement
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

from framework import utilities
from framework.pages.base_page import BasePage, log


class AlarmsPage(BasePage):

    @property
    def alarm_views(self) -> List['WebElement']:
        return self.driver.find_elements_by_accessibility_id("AlarmViewGrid")

    @property
    def edit_alarms_button(self) -> WebElement:
        return self.driver.find_element_by_accessibility_id("EditAlarmsButton")

    @property
    def add_alarm_button(self) -> WebElement:
        return self.driver.find_element_by_accessibility_id("AddAlarmButton")

    def add_new_alarm(self, name: str, hours: int = 0, minutes: int = 0,
                      repeat: bool = False, weekdays: set[int] = None):
        if weekdays is None:
            weekdays = []
        log.info(f"Adding new alarm: '{name}', '{hours:02}:{minutes:02}'; "
                 f"repeat: '{repeat}', on {[utilities.weekdays[x] for x in weekdays]}")
        self.add_alarm_button.click()
        new_alarm_dialog = self.AlarmDialog(self.driver)
        new_alarm_dialog.set_hours(hours)
        new_alarm_dialog.set_minutes(minutes)
        new_alarm_dialog.set_name(name)
        new_alarm_dialog.set_repeat(repeat)
        new_alarm_dialog.set_weekdays(weekdays)
        new_alarm_dialog.submit()

    def delete_all_alarms(self):
        log.info("Deleting all timers.")
        self.edit_alarms_button.click()

        for timer in self.alarm_views:
            timer.find_element_by_accessibility_id("DeleteButton").click()

    def edit_alarm_by_name(self, name: str, new_name: str = None, hours: int = None, minutes: int = None,
                           repeat: bool = None, weekdays: set[int] = None):
        log.info(f"Editing alarm '{name}'")
        self.get_alarm_by_name(name).click()
        edit_alarm_dialog = self.AlarmDialog(self.driver)
        if new_name is not None:
            edit_alarm_dialog.set_name(new_name)
        if hours is not None:
            edit_alarm_dialog.set_hours(hours)
        if minutes is not None:
            edit_alarm_dialog.set_minutes(minutes)
        if repeat is not None:
            edit_alarm_dialog.set_repeat(repeat)
        if weekdays is not None:
            edit_alarm_dialog.set_weekdays(weekdays)
        edit_alarm_dialog.submit()

    def get_alarm_by_name(self, name: str) -> WebElement:
        for alarm in self.alarm_views:
            if AlarmsPage.get_alarm_name(alarm) == name:
                return alarm

        raise NoSuchElementException(f"Alarm '{name}' was not found.")

    @staticmethod
    def get_alarm_name(alarm: WebElement) -> str:
        return alarm.find_element_by_accessibility_id("AlarmName").get_attribute("Name")

    @staticmethod
    def is_alarm_enabled(alarm: WebElement) -> bool:
        return alarm.find_element_by_accessibility_id("AlarmTime").is_enabled()

    @staticmethod
    def toggle_alarm(alarm: WebElement):
        alarm.find_element_by_accessibility_id("AlarmToggleSwitch").click()

    @staticmethod
    def get_alarm_toggled_weekdays(alarm: WebElement) -> set[int]:
        weekdays = set()
        weekday_buttons = alarm.find_elements_by_xpath(".//Button[@ClassName='ToggleButton']")
        for wb in weekday_buttons:
            if int(wb.get_attribute("Toggle.ToggleState")):
                weekdays.add(utilities.weekdays.index(wb.get_attribute("Name")))
        return weekdays

    class AlarmDialog(BasePage):

        @property
        def hour_picker(self) -> WebElement:
            return self.root.find_element_by_accessibility_id("HourPicker")

        @property
        def minute_picker(self) -> WebElement:
            return self.root.find_element_by_accessibility_id("MinutePicker")

        @property
        def name_input_box(self) -> WebElement:
            return self.root.find_element_by_name("Alarm name")

        @property
        def repeat_check_box(self) -> WebElement:
            return self.root.find_element_by_accessibility_id("RepeatCheckBox")

        @property
        def save_button(self) -> WebElement:
            return self.root.find_element_by_accessibility_id("PrimaryButton")

        @property
        def close_button(self) -> WebElement:
            return self.root.find_element_by_accessibility_id("CloseButton")

        def __init__(self, driver: WebDriver):
            super().__init__(driver)
            self.root = driver.find_element_by_accessibility_id("EditFlyout")

        def set_hours(self, hours: int):
            log.info(f"Setting alarm hours to '{hours}'")
            hour_picker = self.hour_picker
            hour_picker.click()
            hour_picker.send_keys(hours)

        def set_minutes(self, minutes: int):
            log.info(f"Setting alarm minutes to '{minutes}'")
            minute_picker = self.minute_picker
            minute_picker.click()
            minute_picker.send_keys(minutes)

        def set_name(self, name: str):
            log.info(f"Setting alarm name to '{name}'")
            input_box = self.name_input_box
            input_box.click()
            input_box.send_keys(name)

        def set_repeat(self, repeat: bool):
            if self.is_repeat_enabled() == repeat:
                log.debug(f"Repeat value is already set to '{repeat}'")
            else:
                log.info(f"Setting repeat value to '{repeat}'")
                self.repeat_check_box.click()

        def set_weekdays(self, weekdays: set[int]):
            if weekdays:
                log.info(f"Setting repeat weekdays: {[utilities.weekdays[x] for x in weekdays]}")
                for i in weekdays:
                    self.get_weekday_button_by_name(utilities.weekdays[i]).click()

        def is_repeat_enabled(self) -> bool:
            return bool(int(self.repeat_check_box.get_attribute("Toggle.ToggleState")))

        def get_weekday_button_by_name(self, weekday: str) -> WebElement:
            return self.root.find_element_by_name(weekday)

        def submit(self):
            self.save_button.click()
            self.wait.until(lambda d: not self.root.is_displayed())
