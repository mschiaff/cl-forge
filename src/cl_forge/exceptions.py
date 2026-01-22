from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core._rs_cl_forge import _rs_cmf as _cmf  # noqa
    from .core._rs_cl_forge import _rs_verify as _verify  # noqa

    CmfClientException = _cmf.CmfClientException
    EmptyPath = _cmf.EmptyPath
    BadStatus = _cmf.BadStatus
    EmptyApiKey = _cmf.EmptyApiKey
    InvalidPath = _cmf.InvalidPath
    ConnectError = _cmf.ConnectError

    PpuException = _verify.PpuException
    UnknownFormat = _verify.UnknownFormat
    InvalidLength = _verify.InvalidLength
    UnknownLetter = _verify.UnknownLetter
    EmptyLetters = _verify.EmptyLetters
    UnknownDigraph = _verify.UnknownDigraph
    EmptyDigraph = _verify.EmptyDigraph

    VerifierException = _verify.VerifierException
    EmptyDigits = _verify.EmptyDigits
    EmptyVerifier = _verify.EmptyVerifier
    InvalidDigits = _verify.InvalidDigits
    InvalidVerifier = _verify.InvalidVerifier
    UnexpectedComputation = _verify.UnexpectedComputation

    GenerateException = _verify.GenerateException
    InvalidRange = _verify.InvalidRange
    InvalidInput = _verify.InvalidInput
    InsufficientRange = _verify.InsufficientRange
    UnexpectedGeneration = _verify.UnexpectedGeneration

__all__ = (
    "CmfClientException",
    "EmptyPath",
    "BadStatus",
    "EmptyApiKey",
    "InvalidPath",
    "ConnectError",
    "PpuException",
    "UnknownFormat",
    "InvalidLength",
    "UnknownLetter",
    "EmptyLetters",
    "UnknownDigraph",
    "EmptyDigraph",
    "VerifierException",
    "EmptyDigits",
    "EmptyVerifier",
    "InvalidDigits",
    "InvalidVerifier",
    "UnexpectedComputation",
    "GenerateException",
    "InvalidRange",
    "InvalidInput",
    "InsufficientRange",
    "UnexpectedGeneration",
)

__cmf_exceptions__ = (
    "CmfClientException",
    "EmptyPath",
    "BadStatus",
    "EmptyApiKey",
    "InvalidPath",
    "ConnectError",
)

__verify_exceptions__ = (
    "PpuException",
    "UnknownFormat",
    "InvalidLength",
    "UnknownLetter",
    "EmptyLetters",
    "UnknownDigraph",
    "EmptyDigraph",
    "VerifierException",
    "EmptyDigits",
    "EmptyVerifier",
    "InvalidDigits",
    "InvalidVerifier",
    "UnexpectedComputation",
    "GenerateException",
    "InvalidRange",
    "InvalidInput",
    "InsufficientRange",
    "UnexpectedGeneration",
)


def __getattr__(name: str):
    if name in __cmf_exceptions__:
        from .core._rs_cl_forge import _rs_cmf as _cmf  # noqa
        return getattr(_cmf, name)
    if name in __verify_exceptions__:
        from .core._rs_cl_forge import _rs_verify as _verify  # noqa
        return getattr(_verify, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")