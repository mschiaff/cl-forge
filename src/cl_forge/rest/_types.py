from typing import Annotated

from pydantic import (
    BeforeValidator,
    HttpUrl,
    StringConstraints,
    ValidationError,
)
from pydantic_core import InitErrorDetails, PydanticCustomError


def validate_base_url(value: str) -> str:
    """
    Validate that a base URL is an absolute HTTP or HTTPS URL without query
    parameters or fragments.
    """
    url = HttpUrl(value)
    errors: list[InitErrorDetails] = []

    if url.query:
        errors.append(
            InitErrorDetails(
                type=PydanticCustomError(
                    "url_query",
                    "URL must not contain query parameters. Remove '?{value}' from the URL",
                    {"value": url.query},
                ),
                input=value,
            )
        )

    if url.fragment:
        errors.append(
            InitErrorDetails(
                type=PydanticCustomError(
                    "url_fragment",
                    "URL must not contain fragments. Remove '#{value}' from the URL",
                    {"value": url.fragment},
                ),
                input=value,
            )
        )

    if errors:
        raise ValidationError.from_exception_data(title="BaseUrl", line_errors=errors)

    return url.encoded_string().rstrip("/")


type NonEmptyStr = Annotated[
    str, StringConstraints(min_length=1, strip_whitespace=True), "Non-empty string"
]
"""A non-empty string that has no leading or trailing whitespace."""

type BaseUrl = Annotated[
    str,
    BeforeValidator(validate_base_url),
    "An absolute HTTP or HTTPS URL without query parameters or fragments.",
]
"""An absolute HTTP or HTTPS URL without query parameters or fragments."""
