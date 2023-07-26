# Instagram Photo Scraper

Just another Instagram photo scraper. Uses Python and Selenium to do the dirty work, and FastAPI as a backend.

Only works for "Posts" and ignores "Stories", "Tagged" and whatever else there is on Instagram.

## Prerequisites

* Python >= 3.11
* Docker >= 20.10.17
* Docker Compose >= 2.10.2

## Usage

1. Set the following environment variables: `INSTAGRAM_USERNAME`, `INSTAGRAM_PASSWORD`.
2. Execute the following commands:
    ```commandline
    ./build.sh
    
    docker-compose -f ./docker/docker-compose.yaml up
    ```
3. Now try the endpoint `http://localhost:8080/getPhotos?username={username}&max_count={max_count}` (`max_count` is optional). For example, [http://localhost:8080/getPhotos?username=glam_app](http://localhost:4444/getPhotos?username=glam_app).
4. In case of troubles, go to [http://localhost:7900/?autoconnect=1&resize=scale&password=secret](http://localhost:7900/?autoconnect=1&resize=scale&password=secret) and help Selenium with logging in to Instagram.

## Response Schema

```json
{
  "urls": ["string"]
}
```
