from __future__ import annotations

from cl_forge.rest.cmf.models.base import RateCollection, RateRecord


class TipRecord(RateRecord):
    """Represents a single TIP rate record."""

class TipCollection(RateCollection[TipRecord]):
    """Represents a collection of TIP rate records."""


class TmcRecord(RateRecord):
    """Represents a single TMC rate record."""

class TmcCollection(RateCollection[TmcRecord]):
    """Represents a collection of TMC rate records."""
