from .base import RateList, RateRecord


class TipRecord(RateRecord):
    """Represents a single TIP rate record."""


class TipList(RateList[TipRecord]):
    """Represents a collection of TIP rate records."""


class TmcRecord(RateRecord):
    """Represents a single TMC rate record."""


class TmcList(RateList[TmcRecord]):
    """Represents a collection of TMC rate records."""
