import math

def area_rectangle(base: float, height: float) -> float:
    return base * height

def area_square(side: float) -> float:
    return side** 2

def area_triangle(base: float, height: float) -> float:
    return (base * height) / 2

def area_circle(radius: float) -> float:
    return math.pi * radius ** 2

def area_trapezoid(base1: float, base2: float, height: float) -> float:
    return ((base1 + base2) * height) / 2
