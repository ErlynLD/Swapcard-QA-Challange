from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.conftest import driver
from utils.utils import Utils


class GoogleHomePage:

    SEARCH_INPUT = (By.CSS_SELECTOR, "textarea[name='q']")

    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.utils = Utils(config)

    def load(self):
        self.driver.get(self.config["base_url"])
        element = self.driver.find_element(*self.SEARCH_INPUT)
        #WebDriverWait(self.driver, self.config["implicit_wait"]).until(EC.element_to_be_clickable(self.driver.find_element(*self.SEARCH_INPUT)))
        if "headless" not in self.config["browser"].lower():
            self.utils.wait_for_web_element_to_be_visible(self.driver, element)
        else:
            self.utils.wait_for_web_element_to_be_clickable(self.driver, element)

    def search(self, phrase):
        search_input = self.driver.find_element(*self.SEARCH_INPUT)
        search_input.send_keys(phrase + Keys.RETURN)
