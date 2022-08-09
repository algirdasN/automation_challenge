from appium.webdriver import WebElement

from framework.pages.base_page import BasePage, log


class Sidebar(BasePage):

    @property
    def focus_tab_button(self) -> WebElement:
        return self.driver.find_element_by_accessibility_id("FocusButton")

    @property
    def timer_tab_button(self) -> WebElement:
        return self.driver.find_element_by_accessibility_id("TimerButton")

    @property
    def alarm_tab_button(self) -> WebElement:
        return self.driver.find_element_by_accessibility_id("AlarmButton")

    @property
    def stopwatch_tab_button(self) -> WebElement:
        return self.driver.find_element_by_accessibility_id("StopwatchButton")

    @property
    def world_clock_tab_button(self) -> WebElement:
        return self.driver.find_element_by_accessibility_id("ClockButton")

    def go_to_focus_tab(self):
        tab_button = self.focus_tab_button
        if not tab_button.is_selected():
            log.info("Clicking on Focus tab button")
            tab_button.click()

    def go_to_timer_tab(self):
        tab_button = self.timer_tab_button
        if not tab_button.is_selected():
            log.info("Clicking on Timer tab button")
            tab_button.click()

    def go_to_alarm_tab(self):
        tab_button = self.alarm_tab_button
        if not tab_button.is_selected():
            log.info("Clicking on Alarm tab button")
            tab_button.click()

    def go_to_stopwatch_tab(self):
        tab_button = self.stopwatch_tab_button
        if not tab_button.is_selected():
            log.info("Clicking on Stopwatch tab button")
            tab_button.click()

    def go_to_world_clock_tab(self):
        tab_button = self.world_clock_tab_button
        if not tab_button.is_selected():
            log.info("Clicking on World Clock tab button")
            tab_button.click()
