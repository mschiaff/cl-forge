from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._rs_cl_forge import market as _rs_market

    MarketClient = _rs_market.MarketClient

__all__ = (
    "MarketClient",
)

def __getattr__(name: str):
    if name in __all__:
        from ._rs_cl_forge import market as _rs_market
        return getattr(_rs_market, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")