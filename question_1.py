import math
from utils import create_row_formatter, number_input


INTRO = """\
The program prints the volume, surface area and circumference of a capsule having radius r ranging from 6 to N in increments of 6 and side length a\
"""


def main():
    print(INTRO)
    radius_inc_unit = 6
    initial_radius = 6
    max_radius = number_input('Enter the value for N: ', int, min=6)
    side_length = number_input('Enter the length of side a: ', float, min=0)

    # print header
    row_ = create_row_formatter([(12, 0), (16, 0), (20, 0), (13, 0)])
    header = row_(['Radius', 'Volume', 'Surface Area', 'Circumference'])
    print(header)
    print(len(header) * '-')

    # loop radius from initial to max
    radius = initial_radius
    while radius <= max_radius:
        # calculate values
        circumference = 2 * math.pi * radius
        surface_area = 4 * math.pi * (radius**2) + circumference * side_length
        volume = side_length * math.pi * (radius**2) + (4/3) * math.pi * (radius**3)
        # print row
        print(row_([radius, f'{volume:.3f}', f'{surface_area:.4f}', f'{circumference:.4f}']))
        radius += radius_inc_unit


if __name__ == '__main__':
    main()
