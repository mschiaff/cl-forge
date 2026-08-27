from pydantic.dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ClientConfig:
    timeout: int | float = 10
    http2: bool = True
    retries: int = 3
