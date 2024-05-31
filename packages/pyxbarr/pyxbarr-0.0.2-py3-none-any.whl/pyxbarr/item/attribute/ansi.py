from typing import Any

from pyxbarr.item.attribute.__base__ import Attribute, INVALID_ATTRIBUTE_VALUE


class AnsiAttribute(Attribute):
    """
    Controls whether to interpret the text as ANSI or not.
    """

    def parse(self, value: Any):
        try:
            return bool(value)
        except ValueError:
            return INVALID_ATTRIBUTE_VALUE
