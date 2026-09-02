from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from pydantic import SecretStr

from cl_forge.rest.auth.base import CredentialsProvider

type CredentialType = str | SecretStr | CredentialsProvider
type DotenvType = Path | str | Sequence[Path | str]
