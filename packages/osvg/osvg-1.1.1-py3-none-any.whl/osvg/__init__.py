"""
Object-oriented SVG Drawing Tool
"""

from .elements.svg import SVG, ViewBox
from .elements.group import Group
from .positions import (
    Position,
    ShiftedPosition,
    PolarShiftedPosition,
    RotatedPosition,
    Distance,
    AngleDegree,
)
from .float import (
    Const,
)
from .float_math import (
    InvertedSign,
    Cos,
    Sin,
    Cot,
    Tan,
    FunctFloat,
    Prod,
    Sum,
    Min,
    LowestAbs,
    Max,
)
from .elements.elementbase import (
    Height,
    Width,
)
from .elements.circle import Circle
from .elements.ellipse import Ellipse
from .elements.rectangle import Rectangle, SCRectangle
from .elements.polyline import Polyline
from .elements.line import Line
from .elements.line_marker import (
    CircleMarker,
    ArrowMarker,
    LightArrowMarker,
    SkinnyArrowMarker,
)
from .style import (
    FillColor,
    FillOpacity,
    StrokeDashArray,
    StrokeColor,
    StrokeLineCap,
    StrokeLineJoin,
    StrokeOpacity,
    StrokeWidth,
    Style,
)

__version__ = "1.1.1"
version_info = (1, 1, 1)
