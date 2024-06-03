import logging
import time
from selenium_assist.helpers import dump_and_exit
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains


def load_page(task, url, driver, continue_on_error=False, silence_warning=False):
    logging.debug(task)
    try:
        driver.get(url)
    except Exception as e:
        if not continue_on_error:
            dump_and_exit(
                "Cannot load webpage, dumping source and exiting!", driver, exc=e
            )
        else:
            if not silence_warning:
                logging.warning("Cannot load webpage, continuing ...")
    return


def wait_for_presence(
    task,
    xpath,
    driver,
    timeout=60,
    extra_timeout=0,
    continue_on_error=False,
    silence_warning=False,
):
    logging.debug(task)
    try:
        element_present = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(driver, timeout).until(element_present)
        time.sleep(extra_timeout)
    except TimeoutException:
        if not continue_on_error:
            dump_and_exit(
                f"Timed out waiting for element presence ({xpath}), dumping source and exiting!",
                driver,
            )
        else:
            if not silence_warning:
                logging.warning(
                    f"Timed out waiting for element presence ({xpath}), continuing ..."
                )
    return


def wait_for_visibility(
    task,
    xpath,
    driver,
    timeout=60,
    extra_timeout=3,
    continue_on_error=False,
    silence_warning=False,
):
    logging.debug(task)
    try:
        element_present = EC.visibility_of_element_located((By.XPATH, xpath))
        WebDriverWait(driver, timeout).until(element_present)
        time.sleep(extra_timeout)
    except TimeoutException:
        if not continue_on_error:
            dump_and_exit(
                "Timed out waiting for element visibility, dumping source and exiting!",
                driver,
            )
        else:
            if not silence_warning:
                logging.warning(
                    "Timed out waiting for element visibility, continuing ..."
                )
    return


def click_element(
    task, xpath, driver, extra_timeout=0, continue_on_error=False, silence_warning=False
):
    logging.debug(task)
    try:
        driver.find_element(By.XPATH, xpath).click()
        time.sleep(extra_timeout)
    except (ElementClickInterceptedException, StaleElementReferenceException):
        if not continue_on_error:
            dump_and_exit(
                "Cannot click on element, dumping source and exiting!", driver
            )
        else:
            if not silence_warning:
                logging.warning("Cannot click on element, continuing ...")
    return


def send_keys(
    task,
    xpath,
    keys,
    driver,
    extra_timeout=5,
    skip_check=False,
    continue_on_error=False,
    silence_warning=False,
):
    logging.debug(task)
    try:
        element_present = EC.element_to_be_clickable((By.XPATH, xpath))
        WebDriverWait(driver, extra_timeout).until(element_present)
        element = driver.find_element(By.XPATH, xpath)
        element.clear()
        element.send_keys(keys)
        if not skip_check:
            WebDriverWait(driver, extra_timeout).until(
                lambda browser: element.get_attribute("value") == keys
            )
    except Exception as e:
        if not continue_on_error:
            dump_and_exit(
                "Cannot send keys on element, dumping source and exiting!",
                driver,
                exc=e,
            )
        else:
            if not silence_warning:
                logging.warning("Cannot send keys on element, continuing ...")
    return


def hoover_over_element(
    task, xpath, driver, continue_on_error=False, silence_warning=False
):
    logging.debug(task)
    try:
        element = driver.find_element(By.XPATH, xpath)
        action = ActionChains(driver)
        action.move_to_element(element).perform()
    except Exception as e:
        if not continue_on_error:
            dump_and_exit(
                "Cannot hoover over element, dumping source and exiting!", driver, exc=e
            )
        else:
            if not silence_warning:
                logging.warning("Cannot hoover over element, continuing ...")
    return


def switch_to_iframe(
    task,
    xpath,
    driver,
    timeout=60,
    extra_timeout=0,
    continue_on_error=False,
    silence_warning=False,
):
    logging.debug(task)
    try:
        element_present = EC.frame_to_be_available_and_switch_to_it((By.XPATH, xpath))
        WebDriverWait(driver, timeout).until(element_present)
        time.sleep(extra_timeout)
    except TimeoutException:
        if not continue_on_error:
            dump_and_exit(
                "Timed out switching to iframe, dumping source and exiting!", driver
            )
        else:
            if not silence_warning:
                logging.warning("Timed out switching to iframe, continuing ...")
    return


def get_table_data(task, xpath, driver, continue_on_error=False, silence_warning=False):
    logging.debug(task)
    data = []
    try:
        for tr in driver.find_elements(By.XPATH, xpath + "//tr"):
            tds = tr.find_elements(By.TAG_NAME, "td")
            if tds:
                data.append([td.text for td in tds])
    except Exception as e:
        if not continue_on_error:
            dump_and_exit(
                "Cannot get table data, dumping source and exiting!", driver, exc=e
            )
        else:
            if not silence_warning:
                logging.warning("Cannot get table data, continuing ...")
    return data


def get_element_text(
    task, xpath, driver, continue_on_error=False, silence_warning=False
):
    logging.debug(task)
    data = ""
    try:
        data = driver.find_element(By.XPATH, xpath).text
    except Exception as e:
        if not continue_on_error:
            dump_and_exit(
                "Cannot get element text, dumping source and exiting!", driver, exc=e
            )
        else:
            if not silence_warning:
                logging.warning("Cannot get element text, continuing ...")
    return data


def execute_script(
    task, xpath, script, driver, continue_on_error=False, silence_warning=False
):
    logging.debug(task)
    data = ""
    try:
        data = driver.find_element(By.XPATH, xpath)
        driver.execute_script(script, data)
    except Exception as e:
        if not continue_on_error:
            dump_and_exit(
                'Cannot execute script "{}", dumping source and exiting!', driver, exc=e
            )
        else:
            if not silence_warning:
                logging.warning('Cannot execute script "{}", continuing ...')
    return data
