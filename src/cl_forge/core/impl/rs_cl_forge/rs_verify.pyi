class PpuException(Exception):  # noqa: N818
    """Base class for all exceptions raised by the PPU."""

class UnknownFormat(PpuException):
    """Raised when the given PPU does not match any known format."""

class InvalidLength(PpuException):
    """Raised when PPU letters or digraphs are of invalid length."""

class UnknownLetter(PpuException):
    """Raised when the given PPU has letters out of the mapping."""

class EmptyLetter(PpuException):
    """Raised when internal mapping functions encounter an empty letter."""

class UnknownDigraph(PpuException):
    """Raised when the given PPU has digraphs out of the mapping."""

class EmptyDigraph(PpuException):
    """Raised when internal mapping functions encounter an empty digraph."""


class VerifierException(Exception): # noqa: N818
    """Base class for all exceptions raised by the verifier."""

class EmptyVerifier(VerifierException):
    """Raised when the given verifier is empty on RUT validation."""

class InvalidVerifier(VerifierException):
    """Raised when the given verifier is invalid on RUT validation."""

class UnexpectedComputation(VerifierException):
    """Raised when the verifier computation fails."""


class GenerateException(Exception): # noqa: N818
    """Base class for all exceptions raised by the RUT generator."""

class InvalidRange(GenerateException):
    """Raised when the generator given lower bound is greater than upper bound."""

class InvalidInput(GenerateException):
    """Raised when generator's given parameters are invalid."""

class InsufficientRange(GenerateException):
    """Raised when the requested amount of RUTs is greater than the available range."""

class UnexpectedGeneration(GenerateException):
    """Raised to support unidentified errors during RUT generation."""