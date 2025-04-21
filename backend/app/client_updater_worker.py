import asyncio
import logging
import random
from typing import Any

from fastapi import WebSocket

from app.globals import POSTS_UPDATE_RATE
from app.helpers import get_client_ip

logger: logging.Logger = logging.getLogger(__name__)


class ClientUpdaterWorker:
    NUMBER_OF_MOST_POPOPULAR_POSTS_TO_KEEP_PER_TREND = 10

    def __init__(self, queue: asyncio.Queue[Any]):
        self._connected_clients: list[WebSocket] = []
        self._queue: asyncio.Queue[Any] = queue
        self._trends_message: Any
        self._posts_messages: list[Any] = list()
        self._currently_displayed_posts_indexes: list[int] = list()
        for _ in range(100):
            self._posts_messages.append(list())
            self._currently_displayed_posts_indexes.append(0)

    async def start(self) -> None:
        self._queue_listener_worker_task = asyncio.create_task(
            self._queue_listener_worker()
        )
        self._posts_updater_worker_task = asyncio.create_task(
            self._posts_updater_worker()
        )
        await asyncio.gather(
            self._queue_listener_worker_task,
            self._posts_updater_worker_task,
            return_exceptions=False,
        )

    async def close(self) -> None:
        connected_clients_iterable: list[WebSocket] = self._connected_clients
        for client in connected_clients_iterable:
            try:
                await client.close()
            except Exception:
                pass
            finally:
                self._connected_clients.remove(client)
        self._queue_listener_worker_task.cancel()
        self._posts_updater_worker_task.cancel()
        await asyncio.gather(
            self._queue_listener_worker_task,
            self._posts_updater_worker_task,
            return_exceptions=True,
        )

    async def add_client(self, websocket: WebSocket):
        logger.info(
            "Client attempts to connect",
            extra={
                "ip": get_client_ip(websocket),
            },
        )
        try:
            await websocket.accept()
            for _ in range(3):
                try:
                    await websocket.send_json(self._trends_message)
                    for trend_id, _ in enumerate(self._posts_messages):
                        await self._send_current_post(
                            trend_id=trend_id, to_client=websocket
                        )
                    break
                except Exception:
                    await asyncio.sleep(1)
        except Exception:
            await self._close_client_connection(websocket)
            return
        self._connected_clients.append(websocket)
        logger.info(
            "Client connected",
            extra={
                "ip": get_client_ip(websocket),
                "total_clients": len(self._connected_clients),
            },
        )

    async def _posts_updater_worker(self) -> None:
        choices = list(POSTS_UPDATE_RATE.keys())
        weights: list[float] = [1 / POSTS_UPDATE_RATE[x] for x in choices]
        while True:
            try:
                await asyncio.sleep(random.randint(2, 5))
                trend_index_to_update: list[int] = random.choices(choices, weights, k=1)
                await self._send_current_post(trend_index_to_update[0])
                self._update_currently_displayed_post_index_for(
                    trend_index_to_update[0]
                )
            except Exception:
                logger.exception("Exception in _posts_updater_worker")

    async def _queue_listener_worker(self):
        while True:
            try:
                await asyncio.sleep(10)
                if not self._queue.empty():
                    message: Any = await self._queue.get()
                    if message["message-type"] == "trends_list":
                        self._trends_message = message
                        await self._send_current_trends()
                    elif message["message-type"] == "trend_posts":
                        trend_id: int = message["data"]["trend_id"]
                        self._process_trend_posts_message(message)
                        await self._send_current_post(trend_id)
                        self._update_currently_displayed_post_index_for(trend_id)
            except Exception:
                logger.exception("Exception in  _queue_listener_worker")

    def _process_trend_posts_message(self, trend_posts_message: Any):
        trend_id: int = trend_posts_message["data"]["trend_id"]
        posts: list[Any] = trend_posts_message["data"]["posts"]
        posts.sort(key=lambda x: x["favorites"], reverse=True)
        trend_posts_message["data"]["posts"] = posts[
            : self.NUMBER_OF_MOST_POPOPULAR_POSTS_TO_KEEP_PER_TREND
        ]
        self._posts_messages[trend_id] = trend_posts_message

    async def _send_current_trends(self):
        clients_to_remove: list[WebSocket] = []
        for client in self._connected_clients:
            try:
                await client.send_json(self._trends_message)
            except Exception:
                await self._close_client_connection(client)
                clients_to_remove.append(client)
        for client in clients_to_remove:
            self._connected_clients.remove(client)

    async def _send_current_post(
        self, trend_id: int, to_client: WebSocket | None = None
    ) -> None:
        clients_to_remove: list[WebSocket] = []
        clients_to_send_post_to: list[WebSocket] = []
        if to_client:
            clients_to_send_post_to.append(to_client)
        else:
            clients_to_send_post_to = self._connected_clients

        if not self._posts_messages[trend_id]:
            return None
        trend_posts_message = self._posts_messages[trend_id]
        if not trend_posts_message["data"]["posts"]:
            return None
        post_to_send = trend_posts_message["data"]["posts"][
            self._currently_displayed_posts_indexes[trend_id]
        ]

        for client in clients_to_send_post_to:
            try:
                await client.send_json(
                    {
                        "message-type": "trend_posts",
                        "data": {"trend_id": trend_id, "post": post_to_send},
                    }
                )
            except Exception:
                await self._close_client_connection(client)
                clients_to_remove.append(client)
        for client in clients_to_remove:
            self._connected_clients.remove(client)

    async def _close_client_connection(self, client: WebSocket) -> None:
        try:
            await asyncio.wait_for(client.close(), 5)
        except Exception:
            pass
        finally:
            logger.info(
                "Client disconnected",
                extra={
                    "ip": get_client_ip(client),
                },
            )

    def _update_currently_displayed_post_index_for(self, trend_id: int) -> None:
        if self._posts_messages[trend_id]:
            if self._posts_messages[trend_id].get("data", {}).get("posts", []):
                self._currently_displayed_posts_indexes[trend_id] = random.randint(
                    0, len(self._posts_messages[trend_id]["data"]["posts"]) - 1
                )
