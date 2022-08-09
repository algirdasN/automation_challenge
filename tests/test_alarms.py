from selenium.common.exceptions import NoSuchElementException

from framework.pages.alarms_page import AlarmsPage
from framework.pages.sidebar import Sidebar
from tests.base_test import BaseTest


class TestAlarms(BaseTest):

    def initiate_pages(self):
        self.sidebar = Sidebar(self.driver)
        self.alarms_page = AlarmsPage(self.driver)

    def setup_method(self):
        super().setup_method()
        self.sidebar.go_to_alarm_tab()

    def teardown_method(self):
        self.alarms_page.delete_all_alarms()
        super().teardown_method()

    def test_disable_alarm(self):
        name = "disable"
        self.alarms_page.add_new_alarm(name)
        alarm = self.alarms_page.get_alarm_by_name(name)
        AlarmsPage.toggle_alarm(alarm)
        assert not AlarmsPage.is_alarm_enabled(alarm), "Alarm was not disabled"

    def test_edit_alarm(self):
        old_name = "before"
        new_name = "after"
        new_weekdays = set(range(1, 6))
        self.alarms_page.add_new_alarm(old_name, hours=9, minutes=20)
        self.alarms_page.edit_alarm_by_name(old_name, new_name, weekdays=new_weekdays)
        try:
            self.alarms_page.get_alarm_by_name(old_name)
            assert False, "Alarm with old name is still visible"
        except NoSuchElementException:
            pass

        alarm = self.alarms_page.get_alarm_by_name(new_name)
        assert AlarmsPage.get_alarm_toggled_weekdays(alarm) == new_weekdays
