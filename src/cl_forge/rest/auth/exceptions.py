from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base import DotenvType


class CredentialsError(Exception):
    """Base exception for credential resolution errors."""


class MissingCredentialsError(CredentialsError):
    """Raised when credentials cannot be resolved for a given scope."""

    def __init__(self, env_prefix: str | None = None) -> None:
        self.env_var = f"{env_prefix}API_KEY" if env_prefix else None


class EnvCredentialsError(MissingCredentialsError):
    """Raised when credentials cannot be resolved from environment variables."""

    env_var: str

    def __init__(self, env_prefix: str) -> None:
        super().__init__(env_prefix=env_prefix)

    def __str__(self) -> str:
        return f"Missing or empty {self.env_var!r} environment variable."


class DotEnvCredentialsError(MissingCredentialsError):
    """Raised when credentials cannot be resolved from a .env file."""

    env_var: str

    def __init__(self, env_prefix: str, env_file: DotenvType) -> None:
        super().__init__(env_prefix=env_prefix)
        self.env_file = env_file

    def __str__(self) -> str:
        return (
            f"Missing or empty {self.env_var!r} variable "
            f"in the dotenv file {self.env_file!r}."
        )
