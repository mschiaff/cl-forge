from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from pydantic import SecretStr

from .base import CredentialsProvider

__all__ = ("CredentialType", "DotenvType",)


CredentialType = str | SecretStr | CredentialsProvider
DotenvType = Path | str | Sequence[Path | str]
