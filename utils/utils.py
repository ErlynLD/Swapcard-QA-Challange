from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Utils:

    def __init__(self, config):
        self.config = config

    def wait_for_web_element_to_be_clickable(self, driver, element):
        WebDriverWait(driver, self.config["implicit_wait"]).until(EC.element_to_be_clickable(element))
        return element

    def wait_for_web_element_to_be_visible(self, driver, element):
        WebDriverWait(driver, self.config["implicit_wait"]).until(EC.visibility_of(element))
        return element