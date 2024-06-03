import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def connect_webdriver(no_headless):
    # turn off webdriver-manager logs
    os.environ["WDM_LOG"] = str(logging.NOTSET)
    # place chromedriver in cwd
    os.environ["WDM_LOCAL"] = "1"
    # turn off the progress bar
    os.environ["WDM_PROGRESS_BAR"] = str(0)
    # skip SSL verification
    # os.environ["WDM_SSL_VERIFY"] = "0"

    chrome_options = Options()
    if not no_headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--dns-prefetch-disable")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # os.environ['WDM_LOG_LEVEL'] = '0'
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=chrome_options
    )

    # set default timeout for operations
    driver.implicitly_wait(20)

    return driver
