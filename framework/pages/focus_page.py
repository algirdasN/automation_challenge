from appium.webdriver import WebElement

from framework.pages.base_page import BasePage, log


class FocusPage(BasePage):

    @property
    def input_box(self) -> WebElement:
        return self.driver.find_element_by_accessibility_id("InputBox")

    @property
    def increase_arrow(self) -> WebElement:
        return self.driver.find_element_by_accessibility_id("UpSpinButton")

    @property
    def decrease_arrow(self) -> WebElement:
        return self.driver.find_element_by_accessibility_id("DownSpinButton")

    @property
    def break_text_box(self) -> WebElement:
        return self.driver.find_element_by_accessibility_id("BreakBlock")

    def set_focus_time(self, focus_time: int):
        if focus_time < 15 or focus_time > 240 or focus_time % 15 != 0:
            raise ValueError(f"Invalid value: '{focus_time}'. Acceptable focus time - 0-240 in increments of 15.")

        log.info(f"Setting Focus time to '{focus_time}'")

        input_box_element = self.input_box
        current_value = int(input_box_element.get_attribute("Value.Value"))

        while current_value != focus_time:
            if current_value < focus_time:
                self.increase_arrow.click()
            else:
                self.decrease_arrow.click()
            current_value = int(input_box_element.get_attribute("Value.Value"))

    def get_break_box_text(self) -> str:
        return self.break_text_box.text
