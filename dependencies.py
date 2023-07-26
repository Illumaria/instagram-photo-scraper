import logging
import os
from typing import Any

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

BASE_URL: str = "https://www.instagram.com/"
BROWSER_URL: str | None = os.getenv("BROWSER_URL")
DATA: dict[str, Any] = {}
USERNAME: str | None = os.getenv("INSTAGRAM_USERNAME")
PASSWORD: str | None = os.getenv("INSTAGRAM_PASSWORD")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


async def create_driver() -> WebDriver:
    options = webdriver.ChromeOptions()
    # useful when manual intervention is not needed
    # options.add_argument("--headless=new")
    driver = webdriver.Remote(command_executor=BROWSER_URL, options=options)
    DATA["driver"] = driver
    return driver


async def get_driver() -> WebDriver:
    if not DATA.get("driver"):
        await create_driver()
    return DATA["driver"]


async def login() -> None:
    logger.info("Logging in to Instagram...")
    driver = await get_driver()
    driver.get(BASE_URL)

    # Cookies Pop-up
    WebDriverWait(driver=driver, timeout=5).until(
        ec.element_to_be_clickable(
            (By.XPATH, '//button[text()="Allow all cookies"]')
        )
    ).click()

    # Login
    username_field = WebDriverWait(driver=driver, timeout=5).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="username"]'))
    )
    username_field.send_keys(USERNAME)

    password_field = driver.find_element(
        by=By.CSS_SELECTOR, value='input[name="password"]'
    )
    password_field.send_keys(PASSWORD)

    password_field.submit()

    # Save Login Info Pop-up
    WebDriverWait(driver=driver, timeout=5).until(
        ec.element_to_be_clickable((By.XPATH, '//button[text()="Save Info"]'))
    ).click()

    # Notifications Pop-up
    WebDriverWait(driver=driver, timeout=5).until(
        ec.element_to_be_clickable((By.XPATH, '//button[text()="Not Now"]'))
    ).click()

    logger.info("Login completed!")
