from fastapi import WebSocket


def get_client_ip(client: WebSocket) -> str:
    try:
        forwarded_for: str | None = client.headers.get("x-forwarded-for")
        ip: str = (
            forwarded_for.split(",")[0].strip() if forwarded_for else client.client.host
        )
        return ip
    except Exception:
        return ""
