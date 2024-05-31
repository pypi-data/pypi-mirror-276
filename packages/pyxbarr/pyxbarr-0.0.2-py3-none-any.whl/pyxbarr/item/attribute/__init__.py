from pyxbarr.item.attribute.__base__ import AttributeName, Attribute
from pyxbarr.item.attribute.alternative import AlternativeAttribute
from pyxbarr.item.attribute.ansi import AnsiAttribute
from pyxbarr.item.attribute.color import ColorAttribute
from pyxbarr.item.attribute.disabled import DisabledAttribute
from pyxbarr.item.attribute.dropdown import DropdownAttribute
from pyxbarr.item.attribute.emojize import EmojizeAttribute
from pyxbarr.item.attribute.font import FontAttribute
from pyxbarr.item.attribute.href import HrefAttribute
from pyxbarr.item.attribute.image import ImageAttribute
from pyxbarr.item.attribute.key import KeyAttribute
from pyxbarr.item.attribute.length import LengthAttribute
from pyxbarr.item.attribute.parmas import ParamsAttribute
from pyxbarr.item.attribute.refresh import RefreshAttribute
from pyxbarr.item.attribute.shell import ShellAttribute
from pyxbarr.item.attribute.size import SizeAttribute
from pyxbarr.item.attribute.template_image import TemplateImageAttribute
from pyxbarr.item.attribute.terminal import TerminalAttribute
from pyxbarr.item.attribute.trim import TrimAttribute

# All valid attributes that xbar can handle.
# New attributes should be added here.
ATTRIBUTES = [
    AnsiAttribute,
    AlternativeAttribute,
    ColorAttribute,
    DisabledAttribute,
    DropdownAttribute,
    EmojizeAttribute,
    FontAttribute,
    HrefAttribute,
    ImageAttribute,
    KeyAttribute,
    LengthAttribute,
    ParamsAttribute,
    RefreshAttribute,
    ShellAttribute,
    SizeAttribute,
    TemplateImageAttribute,
    TerminalAttribute,
    TrimAttribute,
]

ATTRIBUTES_MAPPING = {
    attribute.name: attribute
    for attribute in ATTRIBUTES
}
