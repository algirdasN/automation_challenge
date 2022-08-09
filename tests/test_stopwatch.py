import time

from framework.pages.sidebar import Sidebar
from framework.pages.stopwatch_page import StopwatchPage
from tests.base_test import BaseTest


class TestStopwatch(BaseTest):

    def initiate_pages(self):
        self.sidebar = Sidebar(self.driver)
        self.stopwatch_page = StopwatchPage(self.driver)

    def setup_method(self):
        super().setup_method()
        self.sidebar.go_to_stopwatch_tab()

    def teardown_method(self):
        self.stopwatch_page.reset_stopwatch()
        super().teardown_method()

    def test_lap_button_enable(self):
        assert not self.stopwatch_page.lap_button.is_enabled(), "Lap button is enabled when stopwatch is not running"
        self.stopwatch_page.start_stopwatch()
        assert self.stopwatch_page.is_stopwatch_running(), "Stopwatch did not start"
        assert self.stopwatch_page.lap_button.is_enabled(), "Lap button is not enabled when stopwatch is running"

    def test_laps(self):
        laps = 3
        self.stopwatch_page.start_stopwatch()

        for i in range(laps):
            time.sleep(2)
            self.stopwatch_page.lap_button.click()

        self.stopwatch_page.stop_stopwatch()

        assert len(self.stopwatch_page.lap_rows) == 3, "Incorrect amount of laps registered"
