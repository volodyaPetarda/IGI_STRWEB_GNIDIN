from abc import ABC, abstractmethod
from math import pi, sqrt, sin, radians, cos
import matplotlib.pyplot as plt


class GeometricFigure(ABC):
    @abstractmethod
    def area(self):
        pass


class HelloWorldPrinter:
    def print_hello_world(self):
        print("Hello, World!")


class Rhombus(GeometricFigure, HelloWorldPrinter):
    name = "Rhombus"

    def __init__(self, side_length, angle, color):
        self.side_length = side_length
        self.angle = angle
        self.color = color

    def area(self):
        return self.side_length ** 2 * sin(radians(self.angle))

    def draw(self):
        half_diagonal1 = self.side_length * sin(radians(self.angle / 2))
        half_diagonal2 = self.side_length * cos(radians(self.angle / 2))

        x = [half_diagonal2, 0, -half_diagonal2, 0, half_diagonal2]
        y = [0, half_diagonal1, 0, -half_diagonal1, 0]

        plt.fill(x, y, color=self.color)
        plt.axis('equal')

    def get_info(self):
        return "Rhombus with side length {} and angle {} degrees, color: {}, area: {}".format(
            self.side_length, self.angle, self.color, self.area()
        )
