import time
from typing import Annotated

from fastapi import APIRouter, Query
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebElement

from dependencies import BASE_URL, get_driver

router = APIRouter()


@router.get("/getPhotos")
async def get_photos(
    username: str,
    max_count: Annotated[int | None, Query(gt=0)] = None,
) -> dict[str, list[str | None]]:
    driver: WebDriver = await get_driver()

    driver.get(f"{BASE_URL}/{username}")
    time.sleep(2)

    photo_urls: set[str | None] = set()
    while True:
        new_photos = driver.find_elements(by=By.XPATH, value="//article//img")
        if new_photos:
            new_photo_urls: set[str | None] = {
                photo.get_attribute("src") for photo in new_photos
            }

            if not new_photo_urls - photo_urls:
                break
            else:
                photo_urls |= new_photo_urls

            if max_count and len(set(photo_urls)) >= max_count:
                break

            last_photo: WebElement = new_photos[-1]
            delta_y: int = int(last_photo.rect["y"])
            ActionChains(driver=driver).scroll_to_element(
                last_photo
            ).scroll_by_amount(0, delta_y).perform()
            time.sleep(2)

    return {"urls": list(photo_urls)[:max_count]}
