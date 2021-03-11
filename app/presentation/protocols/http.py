from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class HttpResponse:
    status_code: int
    body: dict[str, Any]


@dataclass
class HttpRequest:
    body: Optional[dict[str, Any]] = None
    headers: Optional[Any] = None
    params: Optional[Any] = None
