"""

    See https://www.cuemath.com/geometry/ellipse/ reference.

    In the above reference, an ellipse around the origin (0,0) is described by the equation x²/a² + y²/b² = 1,
    where b is the minor radius along the y-axis, and a is the major radius along the x-axis. Thus, a ≥ b by our
    definition; if we wish to change the orbit of the ellipse, then we must rotate it instead (note: when a = b,
    the ellipse is a circle).

    Given that we may wish to draw the ellipse at a different centre point, let us consider the same ellipse at centre
    (o_x, o_y). The equation thus becomes:
        (x - o_x)²/a² + (y - o_y)²/b² = 1

    To rotate the ellipse, we apply a matrix rotation: R = [ cosθ -sinθ ]
                                                           [ sinθ  cosθ ]

    such that a point on the line p = [ x, y ] rotated by R becomes:

    Rp = [ cosθ -sinθ ] [ x ] = [ xcosθ - ysinθ ] = [x_r]
         [ sinθ  cosθ ] [ y ]   [ xsinθ + ycosθ ]   [y_r]

    In other words, our original equation becomes:
        (x_r - o_x)²/a² + (y_r - o_y)²/b² = 1

"""
import math

DEBUG = False

# Allow a tolerance as we're dealing with pixels (int) being transformed to floats. The higher this is, the
# thicker the drawn line. 0.00 will mean only a few points will exactly match the line; 0.01 is 1 or 2 pixels thick.
DEFAULT_TOLERANCE = 0.01


class Ellipse:
    def __init__(self, centre: (int, int), a: int, b: int, t: float = DEFAULT_TOLERANCE, theta: float = 0):
        """
        An ellipse described by its centre, a radius, and b radius.

        :param o: Centre point, coordinates in pixels.
        :param a: a radius in pixels
        :param b: b radius in pixels
        :param t: error margin
        :param theta: rotation angle
        """
        if b > a:
            raise ValueError(f"{self.__class__.__name__}.__init__: b radius cannot be greater than a radius")

        self.o = centre
        self.a = a
        self.a2 = a ** 2  # Store this to speed up calculations
        self.b = b
        self.b2 = b ** 2  # Store this to speed up calculations

        self.t = t

        self.theta = theta

        # Calculation cache to speed things up
        self.cache = {}

    def apply_rotation(self, x: int, y: int) -> (float, float):
        """
        (x, y) are rotated around the centre of the Ellipse.

        :param x: x pixel coordinate
        :param y: y pixel coordinate
        :return: New coordinates.
        """
        if self.theta == 0:  # Save time
            return x, y

        # First we must translate the coordinates so that they consider the ellipse's centre to be (0, 0).
        x_o = x - self.o[0]
        y_o = y - self.o[1]

        # Now we apply the rotation matrix
        x_r = x_o * math.cos(self.theta) - y_o * math.sin(self.theta)
        y_r = x_o * math.sin(self.theta) + y_o * math.cos(self.theta)

        # Finally we map them back to pixel coordinates
        return x_r + self.o[0], y_r + self.o[1]

    def ellipse_equation_lhs(self, x: int, y: int) -> float:
        x_r, y_r = self.apply_rotation(x, y)

        return ((x_r - self.o[0]) ** 2 / self.a2) + ((y_r - self.o[1]) ** 2 / self.b2)

    def is_on_line(self, x: int, y: int) -> bool:
        """
        Is the point (x, y) on the ellipse's line?

        :param x: x (in pixels)
        :param y: y (in pixels)
        :return: True if on the ellipse's line, otherwise False.
        """
        # Check the cache to save on compute time
        if (x, y) in self.cache:
            if DEBUG:
                print(f"DEBUG: Cache retrieved: ({x}, {y})")
            return self.cache[(x, y)]

        # Calculate the ellipse equation left hand side and subtract 1.
        d = self.ellipse_equation_lhs(x, y) - 1

        # This should be zero, or within tolerance, if (x,y) are on the line
        on = abs(d) <= self.t  # Boolean value

        # Add to cache
        if DEBUG:
            print(f"DEBUG: Cache saved: ({x}, {y})")
        self.cache[(x, y)] = on

        return on


if __name__ == "__main__":
    e = Ellipse((10, 10), 20, 10)

    print(e.is_on_line(30, 10))
