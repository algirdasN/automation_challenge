from framework.pages.sidebar import Sidebar
from framework.pages.world_clock_page import WorldClockPage
from tests.base_test import BaseTest


class TestWorldClock(BaseTest):

    def initiate_pages(self):
        self.sidebar = Sidebar(self.driver)
        self.world_clock_page = WorldClockPage(self.driver)

    def setup_method(self):
        super().setup_method()
        self.sidebar.go_to_world_clock_tab()

    def teardown_method(self):
        self.world_clock_page.delete_all_clocks()
        super().teardown_method()

    def test_buttons_enabled(self):
        assert not self.world_clock_page.compare_clocks_button.is_enabled(), "Compare clocks button is enabled"
        assert not self.world_clock_page.edit_clocks_button.is_enabled(), "Edit clocks button is enabled"
        self.world_clock_page.add_new_clock("sydney")
        assert self.world_clock_page.compare_clocks_button.is_enabled(), "Compare clocks button is disabled"
        assert self.world_clock_page.edit_clocks_button.is_enabled(), "Edit clocks buttons is disabled"

    def test_city_pins(self):
        self.world_clock_page.add_new_clock("salt lake")
        self.world_clock_page.add_new_clock("pune")
        assert len(self.world_clock_page.city_pins) == 3, "Incorrect amount of city pins displayed"
