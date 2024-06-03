# Author: Aidan Goldstein

import math


def sphere_volume(radius):
    """
     Returns volume of a sphere given its radius.

     Parameter: radius of a sphere (int or float).

     Returns: volume of sphere (float).
     """

    if radius < 0:
        raise ValueError("A radius cannot be negative value.")

    radius = float(radius)

    return (4.0 / 3.0) * math.pi * (radius ** 3)
