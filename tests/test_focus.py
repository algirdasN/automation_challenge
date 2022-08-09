from framework.pages.focus_page import FocusPage
from framework.pages.sidebar import Sidebar
from tests.base_test import BaseTest


class TestFocus(BaseTest):

    def initiate_pages(self):
        self.sidebar = Sidebar(self.driver)
        self.focus_page = FocusPage(self.driver)

    def setup_method(self):
        super().setup_method()
        self.sidebar.go_to_focus_tab()

    def test_focus_time_no_breaks(self):
        self.focus_page.set_focus_time(30)
        assert self.focus_page.get_break_box_text() == "You’ll have no breaks.", "Break box text does not match."

    def test_focus_time_two_breaks(self):
        self.focus_page.set_focus_time(90)
        assert self.focus_page.get_break_box_text() == "You’ll have 2 breaks.", "Break box text does not match."
