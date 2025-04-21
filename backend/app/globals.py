from os import environ, getenv

from dotenv import load_dotenv

load_dotenv()


POSTS_UPDATE_RATE: dict[int, int] = {
    0: 300,
    1: 300,
    2: 300,
    3: 300,
    4: 300,
    5: 600,
    6: 600,
    7: 600,
    8: 600,
    9: 600,
    10: 3600,
    11: 3600,
    12: 3600,
    13: 3600,
    14: 3600,
    15: 3600,
    16: 3600,
    17: 3600,
    18: 3600,
    19: 3600,
    20: 3600,
    21: 3600,
    22: 3600,
    23: 3600,
    24: 3600,
    25: 3600,
    26: 3600,
    27: 3600,
    28: 3600,
    29: 3600,
}

_raw_origins = getenv("ALLOWED_ORIGINS", "")
ALLOWED_ORIGINS: list[str] = [
    origin.strip() for origin in _raw_origins.split(",") if origin
]
API_KEY: str | None = environ.get("API_KEY")
if API_KEY:
    print("API_KEY was retreived ")
else:
    print("API_KEY wasn't found")
