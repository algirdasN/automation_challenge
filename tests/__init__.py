import logging
import os

log = logging.getLogger("tests")
logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(logging.ERROR)
logging.getLogger("urllib3.connectionpool").setLevel(logging.ERROR)


def setup_module():
    log.debug("Launching WinAppDriver server")
    os.startfile(r"C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe")


def teardown_module():
    log.debug("Killing WinAppDriver and Clock processes")
    os.system("taskkill /f /im WinAppDriver.exe > nul 2>&1")
    os.system("taskkill /f /im Time.exe > nul 2>&1")
