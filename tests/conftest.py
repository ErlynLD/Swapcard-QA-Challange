
import pytest
import json
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from pytest_html import extras

@pytest.fixture(scope='session')
def config():
    with open("config.json") as config_file:
        config = json.load(config_file)

    assert config["browser"] in ['Firefox', 'Chrome', 'Headless Chrome', 'Edge']
    assert isinstance(config["implicit_wait"], int)
    assert config["implicit_wait"] > 0

    return config


def pytest_generate_tests(metafunc):
    if "book_obj" in metafunc.fixturenames:
        try:
            with open("data/test_data.json", 'r') as f:
                test_data = json.load(f)

            book_ids = [book.get('name', f'book_{i}') for i, book in enumerate(test_data)]

            metafunc.parametrize("book_obj", test_data, ids=book_ids)

        except FileNotFoundError:
            pytest.fail("Test Data file NOT FOUND!")
        except json.JSONDecodeError as e:
            pytest.fail(f"Error to parse JSON: {e}")

@pytest.fixture
def driver(config):

    if config["browser"] == 'Firefox':
        options = webdriver.FirefoxOptions()

        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    elif config["browser"] == 'Chrome':
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--enable-cookies")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        print("hello")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    elif config["browser"] == 'Headless Chrome':
        options = webdriver.ChromeOptions()
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        options.add_argument("headless")
        options.add_argument("--disable-blink-features=AutomationControlled")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    else:
        raise Exception(f'Browser "{ config["browser"]}" is not supported.')

    driver.implicitly_wait(config["implicit_wait"])
    driver.maximize_window()

    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            os.makedirs("screenshots", exist_ok=True)

            screenshot_path = f"screenshots/{item.name}.png"

            driver.save_screenshot(screenshot_path)

            if not hasattr(report, 'extra'):
                report.extra = []

            report.extra.append(extras.image(screenshot_path))