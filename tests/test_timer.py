from framework.pages.sidebar import Sidebar
from framework.pages.timer_page import TimerPage
from tests.base_test import BaseTest


class TestTimer(BaseTest):

    def initiate_pages(self):
        self.sidebar = Sidebar(self.driver)
        self.timer_page = TimerPage(self.driver)

    def setup_method(self):
        super().setup_method()
        self.sidebar.go_to_timer_tab()

    def teardown_method(self):
        self.timer_page.delete_all_timers()
        super().teardown_method()

    def test_create_new_timer(self):
        name = "single"
        hours = 0
        minutes = 2
        seconds = 30
        self.timer_page.add_new_timer(name, hours, minutes, seconds)

        timer = self.timer_page.get_timer_by_name(name)
        assert TimerPage.get_timer_duration(timer) == f"{hours:02}:{minutes:02}:{seconds:02}", \
            "Incorrect timer duration was set."

    def test_create_multiple_timers(self):
        self.timer_page.add_new_timer("timer1", hours=1)
        self.timer_page.add_new_timer("timer2", minutes=30)
        assert len(self.timer_page.timer_views) == 2, "Incorrect amount of timers were created."
