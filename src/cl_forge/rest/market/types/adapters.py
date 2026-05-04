from __future__ import annotations

from pydantic.type_adapter import TypeAdapter

from .annotate import DateLike, OrderStatusLike, RutLike, TenderStatusLike

__all__ = (
    "DateLikeAdapter",
    "OrderStatusLikeAdapter",
    "RutLikeAdapter",
    "TenderStatusLikeAdapter",
)


DateLikeAdapter: TypeAdapter[str] = TypeAdapter(DateLike)
RutLikeAdapter: TypeAdapter[str] = TypeAdapter(RutLike)
OrderStatusLikeAdapter: TypeAdapter[str] = TypeAdapter(OrderStatusLike)
TenderStatusLikeAdapter: TypeAdapter[str] = TypeAdapter(TenderStatusLike)
