from dataclasses import dataclass
from typing import Optional


@dataclass
class Response:
    status_code: int
    body: dict[str, str]


@dataclass
class Request:
    body: Optional[dict[str, str]]
