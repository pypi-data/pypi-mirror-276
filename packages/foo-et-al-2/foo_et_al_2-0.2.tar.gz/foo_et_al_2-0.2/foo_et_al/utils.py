from math import pi as PI

def vol_sphere(radius):
    "Calculates the volume of a sphere given a radius."

    if radius is None:
        raise ValueError("The radius must be a non-negative number.")
    if radius < 0:
        raise ValueError("The radius must be non-negative.")

    return 4 / 3 * PI * radius ** 3