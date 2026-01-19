from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core._rs_cl_forge import _rs_cmf as _cmf # noqa

    CmfClient = _cmf.CmfClient

__all__ = (
    "CmfClient",
)


def __getattr__(name: str):
    if name in __all__:
        from .core._rs_cl_forge import _rs_cmf as _cmf  # noqa
        return getattr(_cmf, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")