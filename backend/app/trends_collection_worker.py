import asyncio
import logging
import random
import re
from pprint import pprint
from typing import Any

import httpx
from dotenv import load_dotenv

from app.globals import API_KEY, POSTS_UPDATE_RATE

load_dotenv()

logger: logging.Logger = logging.getLogger(__name__)


class TrendsCollectionWorker:
    _UPDATE_TRENDS_INTERVAL = 3600

    _NUMBER_OF_TRENDS_TO_TRACK = 10
    _POST_COLLECTION_MAX_STARTUP_DELAY = 60
    _COUNTRY = "Canada"

    def __init__(self, queue: asyncio.Queue[Any]) -> None:
        self._queue: asyncio.Queue[Any] = queue
        self._stop_working: asyncio.Event = asyncio.Event()
        self._trends: list[Any] = []
        base_url = "https://twitter-api45.p.rapidapi.com"
        api_secret_key: str | None = API_KEY
        if not api_secret_key:
            raise RuntimeError("x-rapidapi-key not found")
        request_headers: dict[str, str] = {
            "x-rapidapi-key": api_secret_key,
            "x-rapidapi-host": "twitter-api45.p.rapidapi.com",
        }
        self._http_client = httpx.AsyncClient(
            headers=request_headers, base_url=base_url
        )

    async def start(self) -> None:
        self._stop_working.clear()
        tasks: list[asyncio.Task[Any]] = list()
        while True:
            try:
                all_trends: list[Any] = await self._get_trends()
                self._trends = all_trends[0 : self._NUMBER_OF_TRENDS_TO_TRACK]
                if not self._trends:
                    await asyncio.sleep(5)
                    continue
                await self._queue.put(
                    {"message-type": "trends_list", "data": self._trends}
                )
                for trend_id, _ in enumerate(self._trends):
                    tasks.append(
                        asyncio.create_task(self._posts_collection_worker(trend_id))
                    )
                await asyncio.sleep(self._UPDATE_TRENDS_INTERVAL)
            finally:
                for task in tasks:
                    task.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)
                tasks = []

    async def close(self) -> None:
        self._stop_working.set()
        await self._http_client.aclose()

    async def _posts_collection_worker(self, trend_id: int) -> None:
        await asyncio.sleep(random.randint(1, self._POST_COLLECTION_MAX_STARTUP_DELAY))

        while True:
            posts_data: dict[Any, Any] = await self._get_posts(
                self._trends[trend_id]["name"]
            )
            cleaned_posts_data: list[Any] = self._clean_get_posts_response(posts_data)
            await self._queue.put(
                {
                    "message-type": "trend_posts",
                    "data": {"trend_id": trend_id, "posts": cleaned_posts_data},
                }
            )
            await asyncio.sleep(POSTS_UPDATE_RATE[trend_id])

    async def _get_trends(self) -> list[Any]:
        trends_list = []
        try:
            results: httpx.Response = await self._http_client.get(
                "/trends.php", params={"country": self._COUNTRY}
            )
            if results.is_success:
                trends_data: Any = results.json()
                trends_list: Any = trends_data["trends"]
        except Exception:
            logger.exception("Failed to get trends", extra={"country": self._COUNTRY})
            pass
        return trends_list

    async def _get_posts(self, query: str) -> dict[Any, Any]:
        posts_data = {}
        try:
            results: httpx.Response = await self._http_client.get(
                "/search.php", params={"search_type": "Top", "query": query}
            )
            if results.is_success:
                posts_data: Any = results.json()
        except Exception:
            logger.exception("Failed to get posts", extra={"query": query})
        return posts_data

    def _clean_get_posts_response(self, data: dict[Any, Any]) -> list[Any]:
        try:
            cleaned_posts: list[Any] = []
            posts: list[dict[Any, Any]] = data["timeline"]
            for index, post in enumerate(posts):
                cleaned_posts.append(dict())
                cleaned_posts[index]["name"] = post.get("user_info", {}).get("name")
                cleaned_posts[index]["screen_name"] = post.get("user_info", {}).get(
                    "screen_name"
                )
                cleaned_posts[index]["avatar"] = post.get("user_info", {}).get("avatar")
                cleaned_posts[index]["created_at"] = post.get("created_at", None)
                cleaned_posts[index]["tweet_id"] = post.get("tweet_id", None)
                cleaned_posts[index]["text"] = re.sub(
                    r".?https?://\S+$", "", post.get("text", "")
                )
                cleaned_posts[index]["source"] = self._get_post_url(post)
                cleaned_posts[index]["favorites"] = post.get("favorites")
                cleaned_posts[index]["replies"] = post.get("replies")
                cleaned_posts[index]["retweets"] = post.get("retweets")
                cleaned_posts[index]["views"] = post.get("views")
                cleaned_posts[index]["media"] = list()
                try:
                    for video in post.get("media", {}).get("video", []):
                        for variant in video.get("variants", []):
                            if variant.get("content_type") == "video/mp4":
                                url = variant.get("url")
                                if url:
                                    cleaned_posts[index]["media"].append(
                                        {"content_type": "video", "source": url}
                                    )
                                    break
                    for photo in post.get("media", {}).get("photo", []):
                        url = photo.get("media_url_https")
                        if url:
                            cleaned_posts[index]["media"].append(
                                {"content_type": "photo", "source": url}
                            )
                except Exception:
                    pass
            return cleaned_posts
        except Exception:
            logger.exception("Failed to clean api response with posts data")
            return list()

    def _get_post_url(self, post: dict[Any, Any]) -> str:
        try:
            url: str = (
                "https://x.com/"
                + post["user_info"]["screen_name"]
                + "/status/"
                + post["tweet_id"]
            )
            return url
        except Exception:
            return ""


async def main() -> None:
    queue: asyncio.Queue[Any] = asyncio.Queue()
    worker = TrendsCollectionWorker(queue)
    # res = await worker._get_trends()
    res = await worker._get_posts("China")
    print("Raw res")
    pprint(res)
    cleaned_posts = worker._clean_get_posts_response(res)
    pprint(cleaned_posts)


if __name__ == "__main__":
    asyncio.run(main())
