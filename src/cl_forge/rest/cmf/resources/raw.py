from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cl_forge.rest.cmf.resources.base import BaseRawResource

if TYPE_CHECKING:
    from cl_forge.rest.cmf.types import CmfTransport


class RawJsonResource(BaseRawResource):
    def get(self, path: str) -> dict[str, Any]:
        return self._get(path, raw="json")


class RawXmlResource(BaseRawResource):
    def get(self, path: str) -> str:
        return self._get(path, raw="xml")


class RawResource:
    def __init__(
            self,
            transport: CmfTransport,
    ) -> None:
        self.json = RawJsonResource(transport)
        self.xml = RawXmlResource(transport)
