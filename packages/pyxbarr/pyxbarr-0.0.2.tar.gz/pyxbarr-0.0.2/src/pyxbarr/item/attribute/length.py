from typing import Any

from pyxbarr.item.attribute.__base__ import Attribute, INVALID_ATTRIBUTE_VALUE


class LengthAttribute(Attribute):
    """
    Controls the length of the item.
    """

    def parse(self, value: Any):
        try:
            return int(value)
        except ValueError:
            try:
                return int(float(value))
            except ValueError:
                pass

            return INVALID_ATTRIBUTE_VALUE
