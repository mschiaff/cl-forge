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


class Ppu:
    """
        Represents a Chilean PPU (vehicle license plate).

        Attributes
        ----------
        raw : str
            The input PPU.
        numeric : int
            The numeric representation of the PPU.
        normalized: str
            The normalized PPU.
        verifier: str
            The calculated verifier digit of the PPU.
        format: str
            The detected format of the PPU. Supported formats:

            - `LLLNN`  -> 3 letters followed by 2 digits
            - `LLLNNN` -> 4 letters followed by 3 digits
            - `LLLLNN` -> 4 letters followed by 2 digits
            - `LLNNNN` -> 2 letters followed by 4 digits
        complete: str
            The normalized PPU with the verifier digit, separated by '-'.
        """

    def __init__(self, ppu: str) -> None:
        """Initializes a PPU instance with the given PPU string.

        Parameters
        ----------
        ppu : str
            Chilean PPU (vehicle license plate).
        """

    def __repr__(self) -> str: ...

    @property
    def raw(self) -> str:
        """The input PPU."""

    @property
    def numeric(self) -> int:
        """The numeric representation of the PPU."""

    @property
    def normalized(self) -> str:
        """The normalized PPU."""

    @property
    def verifier(self) -> str:
        """The calculated verifier digit of the PPU."""

    @property
    def format(self) -> str:
        """The detected format of the PPU."""

    @property
    def complete(self) -> str:
        """The normalized PPU with the verifier digit, separated by '-'."""


def calculate_verifier(digits: int) -> str:
    """
    Calculates the verifier digit (DV) of a Chilean RUT/RUN using Module 11
    algorithm.

    Parameters
    ----------
    digits : int
        Numeric part of the RUT/RUN (digits only).

    Returns
    -------
    str
        Verifier digit: '0'..'9' or 'K'.
    """


def ppu_to_numeric(ppu: str) -> int:
    """
    Converts a Chilean PPU (vehicle license plate) into its numeric
    representation.

    Parameters
    ----------
    ppu : str
        Chilean PPU (vehicle license plate). Supported formats:

        - `LLLNN`  -> 3 letters followed by 2 digits
        - `LLLNNN` -> 4 letters followed by 3 digits
        - `LLLLNN` -> 4 letters followed by 2 digits
        - `LLNNNN` -> 2 letters followed by 4 digits

    Returns
    -------
    str
        Numeric representation of the PPU.
    """


def normalize_ppu(ppu: str) -> str:
    """
    Normalizes a given PPU string to a standard format.

    If the format is recognized as `LLLNN` (3 letters followed by 2 digits),
    the function prepends a '0' after the first 3 characters, resulting in a
    normalized format of `LLL0NN`. Otherwise, the `ppu` is returned as-is, but
    trimmed in uppercase.

    Parameters
    ----------
    ppu : Chilean PPU (vehicle license plate).

    Returns
    -------
    str
        Normalized PPU.
    """


def validate_rut(digits: int, verifier: str) -> bool:
    """
    Validates a Chilean RUT/RUN by checking if the provided verifier digit
    matches the calculated one using Module 11 algorithm.

    Parameters
    ----------
    digits : int
        Numeric part of the RUT/RUN (digits only).
    verifier : str
        Verifier digit to validate against: "0".."9" or "K".

    Returns
    -------
    bool
        `True` if the verifier is valid for the given correlative,
        `False` otherwise.
    """


def generate(
        n: int,
        min: int,  # noqa: A002
        max: int,  # noqa: A002
        seed: int | None = None
) -> list[dict[str, int | str]]:
    """
    Generates a list of unique Chilean RUT/RUN numbers with their verifier
    digits.

    Parameters
    ----------
    n : int
        The number of RUT/RUNs to generate.
    min : int
        The minimum value for the numeric part of the RUT/RUN.
    max : int
        The maximum value for the numeric part of the RUT/RUN.
    seed : int | None
        An optional seed for the random number generator to ensure
        reproducibility. If `None`, a random seed is used.

    Returns
    -------
    list[dict[str, int | str]]
        A list of dictionaries, each containing 'correlative' and 'verifier'
        keys representing the generated RUT/RUN numbers.

    Raises
    ------
    InvalidInput
        - If `n` is less than or equal to 0.
        - If `min` and/or `max` are negative.
        - If `seed` is given and is negative.
    InvalidRange
        If `min` is greater than or equal to `max`.
    InsufficientRange
        If the range between `min` and `max` is too small to generate `n`
        unique RUT/RUNs.
    """