from .geometry import Geometry  # noqa: F401
from .components.point import Point  # noqa: F401
from .components.linestring import LineString  # noqa: F401
from .components.polygon import Polygon, EmptyPolygon  # noqa: F401
from .buffer import Circle, Square  # noqa: F401
from .background import BackGround  # noqa: F401


import numpy
from dataclasses import dataclass

micro = 1e-6


@dataclass
class CircleOpticalStructure():
    name: str
    """ Name of the structure """
    index: float
    """ Refractive index of the structure """
    radius: float
    """ Radius of the circle representing the slice of the structure """
    position: tuple
    """ Center position of the circle """
    is_graded: bool = False
    """ True if the structure is refractive index graded """
    delta_n: float = None
    """ Delta refractvive index of the grading """

    def __post_init__(self) -> None:
        self.polygon = Circle(position=self.position, radius=self.radius)

    def compute_index_from_NA(self) -> float:
        index = numpy.sqrt(self.NA**2 + self.exterior_structure.index**2)

        return index

    def get_V_number(self, wavelength: float) -> float:
        delta_index = numpy.sqrt(self.index**2 - self.exterior_structure.index**2)

        V = 2 * numpy.pi / wavelength * delta_index * self.radius

        return V

    def scale(self, factor: float) -> None:
        self.radius *= factor
        self.__post_init__()


# -
