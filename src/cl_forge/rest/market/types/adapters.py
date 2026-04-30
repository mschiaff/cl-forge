from __future__ import annotations

from pydantic.type_adapter import TypeAdapter

from .annotate import DateLike, RutLike, StatusLike

__all__ = ("DateLikeAdapter", "RutLikeAdapter", "StatusLikeAdapter",)


DateLikeAdapter: TypeAdapter[str] = TypeAdapter(DateLike)
RutLikeAdapter: TypeAdapter[str] = TypeAdapter(RutLike)
StatusLikeAdapter: TypeAdapter[str] = TypeAdapter(StatusLike)
