from abc import abstractmethod, ABC

from appium import webdriver

from tests import log


class BaseTest(ABC):

    def setup_method(self):
        desired_caps = {"app": "Microsoft.WindowsAlarms_8wekyb3d8bbwe!App"}

        log.debug("Initiating driver")
        self.driver = webdriver.Remote(
            command_executor="http://127.0.0.1:4723",
            desired_capabilities=desired_caps)

        self.initiate_pages()

    def teardown_method(self):
        log.debug("Quitting driver")
        self.driver.quit()

    @abstractmethod
    def initiate_pages(self):
        pass
