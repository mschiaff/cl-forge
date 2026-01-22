from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core._rs_cl_forge import _rs_verify as _verify  # noqa

    Ppu = _verify.Ppu
    calculate_verifier = _verify.calculate_verifier
    normalize_ppu = _verify.normalize_ppu
    ppu_to_numeric = _verify.ppu_to_numeric
    validate_rut = _verify.validate_rut
    generate = _verify.generate

__all__ = (
    "Ppu",
    "calculate_verifier",
    "normalize_ppu",
    "ppu_to_numeric",
    "validate_rut",
    "generate",
)


def __getattr__(name: str):
    if name in __all__:
        from .core._rs_cl_forge import _rs_verify as _verify  # noqa
        return getattr(_verify, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")