from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI

from dependencies import create_driver, login
from routers import instagram


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator:
    driver = await create_driver()
    await login()

    yield

    driver.quit()


app = FastAPI(lifespan=lifespan)
app.include_router(instagram.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
