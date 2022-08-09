from typing import List

from appium.webdriver import WebElement
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

from framework.pages.base_page import BasePage, log


class WorldClockPage(BasePage):

    @property
    def city_pins(self) -> List['WebElement']:
        return self.driver.find_element_by_accessibility_id("ClockCardListView") \
            .find_elements_by_class_name("ListViewItem")

    @property
    def city_info_bars(self) -> List['WebElement']:
        return self.driver.find_element_by_accessibility_id("ClockDetailListView") \
            .find_elements_by_class_name("ListViewItem")

    @property
    def compare_clocks_button(self) -> WebElement:
        return self.driver.find_element_by_xpath(".//*[@AutomationId='CompareTimeButton'][@Name='Compare Time']")

    @property
    def edit_clocks_button(self) -> WebElement:
        return self.driver.find_element_by_xpath(".//*[@AutomationId='CompareTimeButton'][@Name='Edit Clocks']")

    @property
    def add_clock_button(self) -> WebElement:
        return self.driver.find_element_by_accessibility_id("AddClockButton")

    def add_new_clock(self, name):
        log.info(f"Adding new clock: '{name}")
        self.add_clock_button.click()
        new_clock_dialog = self.NewLocationDialog(self.driver)
        new_clock_dialog.enter_search_term(name)
        new_clock_dialog.select_first_suggestion()
        new_clock_dialog.submit()

    def delete_all_clocks(self):
        log.info("Deleting all clocks.")
        self.edit_clocks_button.click()

        for clock in self.city_info_bars:
            try:
                clock.find_element_by_xpath(".//Button[@Name='Delete']").click()
            except NoSuchElementException:
                pass

    class NewLocationDialog(BasePage):

        @property
        def search_bar(self) -> WebElement:
            return self.root.find_element_by_accessibility_id("TextBox")

        @property
        def search_suggestions(self) -> List['WebElement']:
            return self.root.find_elements_by_xpath(".//*[@AutomationId='SuggestionsList']/ListItem")

        @property
        def add_button(self):
            return self.root.find_element_by_accessibility_id("PrimaryButton")

        @property
        def close_button(self):
            return self.root.find_element_by_accessibility_id("CloseButton")

        def __init__(self, driver: WebDriver):
            super().__init__(driver)
            self.root = driver.find_element_by_accessibility_id("AddFlyout")

        def enter_search_term(self, value):
            log.info(f"Searching for location: '{value}'")
            self.search_bar.send_keys(value)

        def select_suggestion(self, index):
            first = self.search_suggestions[index - 1]
            log.info(f"Selecting suggestion: '{first.get_attribute('Name')}'")
            first.click()

        def select_first_suggestion(self):
            self.select_suggestion(1)

        def submit(self):
            self.add_button.click()
            self.wait.until(lambda d: not self.root.is_displayed())
