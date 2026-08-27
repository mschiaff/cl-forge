from collections.abc import Mapping
from typing import Annotated, Literal

type UrlSegment = Annotated[str | int, "A segment of a resource path."]
type ResponseFormat = Annotated[Literal["json", "xml"], "Response format for the request."]

type QueryValue = Annotated[str | int | float, "A value for a query parameter."]
type QueryParams = Annotated[Mapping[str, QueryValue], "Query parameters for a request."]
