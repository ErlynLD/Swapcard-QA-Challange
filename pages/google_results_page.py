from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from selenium.webdriver.common.by import By

from utils.utils import Utils


class GoogleResultsPage:

    HEADER_STR = "//div[@role='navigation']//div[@role='listitem' and contains(string(),'{}')]"
    FILTER_VALUES_BY_SECTION_STR = "//a[parent::li[parent::ul[parent::div[parent::div[preceding-sibling::div[child::div/span[@role='heading'] and string()='{}']]]]]]"

    SHOPPING_MENU_OPTIONS = (By.CSS_SELECTOR, "div[role='list'] > div")

    MIN_PRICE_FILTER = (By.CSS_SELECTOR, "input[title='Min']")
    MAX_PRICE_FILTER = (By.CSS_SELECTOR, "input[title='Max']")
    APPLY_PRICE_RANGE_FILTER_BUTTON = (By.XPATH, "//button[string()='Go']")

    LIST_OF_RATED_ITEMS = (By.XPATH, "//g-inner-card//div[not(*) and not(text()) and contains(@aria-label, 'Rated')]")

    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.utils = Utils(config)

    def load(self):
        element = self.driver.find_element(By.XPATH, self.HEADER_STR.format("Shopping"))
        if "headless" not in self.config["browser"].lower():
            self.utils.wait_for_web_element_to_be_visible(self.driver, element)
        else:
            self.utils.wait_for_web_element_to_be_clickable(self.driver, element)

    def get_menu_option_with_header(self, header):
        menu_option =  self.driver.find_element(By.XPATH, self.HEADER_STR.format(header))
        return self.utils.wait_for_web_element_to_be_clickable(self.driver, menu_option)

    def go_to_shopping_section(self):
        self.get_menu_option_with_header("Shopping").click()

    def open_advanced_filters(self):
        shopping_menu_options = self.driver.find_elements(*self.SHOPPING_MENU_OPTIONS)
        self.utils.wait_for_web_element_to_be_clickable(self.driver, shopping_menu_options[0])
        if shopping_menu_options[0].get_attribute("aria-pressed") == "false":
            shopping_menu_options[0].click()

    def filter_by_section_and_value(self, section, value):
        self.open_advanced_filters()
        values = self.driver.find_elements(By.XPATH, self.FILTER_VALUES_BY_SECTION_STR.format(section))
        self.utils.wait_for_web_element_to_be_clickable(self.driver, values[0])
        filter = [link for link in values if value.lower() in link.text.lower()]
        filter[0].click()

    def filter_by_price_range(self, min=1, max=50000):
        min_input = self.driver.find_element(*self.MIN_PRICE_FILTER)
        max_input = self.driver.find_element(*self.MAX_PRICE_FILTER)
        apply_filter_btn = self.driver.find_element(*self.APPLY_PRICE_RANGE_FILTER_BUTTON)

        self.utils.wait_for_web_element_to_be_clickable(self.driver, max_input)

        min_input.send_keys(min)
        max_input.send_keys(max)
        apply_filter_btn.click()

    def filter_up_to(self, max=50000):
        max_input = self.driver.find_element(*self.MAX_PRICE_FILTER)
        apply_filter = self.driver.find_element(*self.APPLY_PRICE_RANGE_FILTER_BUTTON)

        self.utils.wait_for_web_element_to_be_clickable(self.driver, max_input)

        max_input.send_keys(max)
        apply_filter.click()

    def get_rated_items_list(self):
        return self.driver.find_elements(*self.LIST_OF_RATED_ITEMS)


