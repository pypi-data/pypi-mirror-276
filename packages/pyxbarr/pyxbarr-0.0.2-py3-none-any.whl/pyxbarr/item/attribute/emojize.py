from typing import Any

from pyxbarr.item.attribute.__base__ import Attribute, INVALID_ATTRIBUTE_VALUE


class EmojizeAttribute(Attribute):
    """
    Controls whether the text should be emojized or not.
    """

    def parse(self, value: Any):
        try:
            return bool(value)
        except ValueError:
            return INVALID_ATTRIBUTE_VALUE
