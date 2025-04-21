import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware

from app.client_updater_worker import ClientUpdaterWorker
from app.globals import ALLOWED_ORIGINS
from app.helpers import get_client_ip
from app.logging_config import setup_logging
from app.rate_limiting import is_rate_limited
from app.trends_collection_worker import TrendsCollectionWorker

setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    queue: asyncio.Queue[Any] = asyncio.Queue()
    trends_collection_worker = TrendsCollectionWorker(queue)
    client_updater_worker = ClientUpdaterWorker(queue)
    trends_collection_worker_task: asyncio.Task[None] = asyncio.create_task(
        trends_collection_worker.start()
    )
    client_updater_worker_task: asyncio.Task[None] = asyncio.create_task(
        client_updater_worker.start()
    )
    app.state.client_updater = client_updater_worker
    yield
    await asyncio.wait_for(trends_collection_worker.close(), 10)
    await asyncio.wait_for(client_updater_worker.close(), 10)
    trends_collection_worker_task.cancel()
    client_updater_worker_task.cancel()
    try:
        await asyncio.gather(
            trends_collection_worker_task,
            client_updater_worker_task,
            return_exceptions=True,
        )
    except Exception:
        pass


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    origin: str | None = websocket.headers.get("origin")
    if origin not in ALLOWED_ORIGINS:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        logger.info(
            "Blocked WS due to origin",
            extra={
                "host": get_client_ip(websocket),
                "origin": websocket.headers.get("origin"),
            },
        )
        return

    ip: str = get_client_ip(websocket)
    if not ip:
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        logger.info("Blocked WS due to no found ip")
        return

    if is_rate_limited(ip):
        logger.info(
            "Blocked WS due to exceding rate limit",
            extra={"host": get_client_ip(websocket)},
        )
        await websocket.close(code=status.WS_1013_TRY_AGAIN_LATER)
        return

    await websocket.app.state.client_updater.add_client(websocket)

    try:
        while True:
            await websocket.receive_text()
            await asyncio.sleep(15)
    except WebSocketDisconnect:
        pass
    except Exception:
        await websocket.close()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
