from typing import Final

IMAGE_PATH: Final[str]
DATABASE_PATH: Final[str]

def get_database() -> dict[str, dict[str, dict[str, bool]]]: ...
