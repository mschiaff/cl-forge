from __future__ import annotations

from pydantic.type_adapter import TypeAdapter

from .annotate import DateLike, RutLike, TenderStatusLike

__all__ = ("DateLikeAdapter", "RutLikeAdapter", "TenderStatusLikeAdapter",)


DateLikeAdapter: TypeAdapter[str] = TypeAdapter(DateLike)
RutLikeAdapter: TypeAdapter[str] = TypeAdapter(RutLike)
TenderStatusLikeAdapter: TypeAdapter[str] = TypeAdapter(TenderStatusLike)
