from typing import List

from appium.webdriver import WebElement

from framework.pages.base_page import BasePage, log


class StopwatchPage(BasePage):

    @property
    def stopwatch_timer(self) -> WebElement:
        return self.driver.find_element_by_accessibility_id("StopwatchTimerText")

    @property
    def start_pause_button(self) -> WebElement:
        return self.driver.find_element_by_accessibility_id("StopwatchPlayPauseButton")

    @property
    def lap_button(self) -> WebElement:
        return self.driver.find_element_by_accessibility_id("StopWatchLapButton")

    @property
    def reset_button(self) -> WebElement:
        return self.driver.find_element_by_accessibility_id("StopWatchResetButton")

    @property
    def lap_rows(self) -> List['WebElement']:
        return self.driver.find_elements_by_xpath(".//DataItem[@ClassName='ToggleButton']")

    def start_stopwatch(self):
        if not self.is_stopwatch_running():
            log.info("Starting stopwatch")
            self.start_pause_button.click()
        else:
            log.warn("Unable to start, stopwatch is already running")

    def stop_stopwatch(self):
        if self.is_stopwatch_running():
            log.info("Stopping stopwatch")
            self.start_pause_button.click()
        else:
            log.warn("Unable to stop, stopwatch is not running")

    def reset_stopwatch(self):
        if self.reset_button.is_enabled():
            log.info("Resetting stopwatch")
            self.reset_button.click()
        else:
            log.debug("Reset button is disabled, stopwatch already set to zero")

    def is_stopwatch_running(self) -> bool:
        return self.start_pause_button.get_attribute("Name") == "Pause"
