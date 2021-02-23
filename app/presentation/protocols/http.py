from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Response:
    status_code: int
    body: dict[str, Any]


@dataclass
class Request:
    body: Optional[dict[str, Any]]
