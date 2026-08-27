from typing import Annotated, Any

from pydantic import Field

from cl_forge.rest.cmf.models.base import IndexList, IndexRecord, RateList, RateRecord

type RecordModel = IndexRecord | RateRecord
type ListModel = IndexList[Any] | RateList[Any]

type Year = Annotated[int, Field(ge=0), "Year"]
type Month = Annotated[int, Field(ge=1, le=12), "Month"]
type Day = Annotated[int, Field(ge=1, le=31), "Day"]

type YearMonth = Annotated[tuple[Year, Month], "YearMonth"]
type YearMonthDay = Annotated[tuple[Year, Month, Day], "YearMonthDay"]
