import math
from typing import TypeVar, Type, Callable

INTRO = """\
The program prints the volume, surface area and circumference of a capsule having radius r ranging from 6 to N in increments of 6 and side length a\
"""

N = TypeVar('N', int, float)


def number_input(hint, number_type: Type[N], min=None) -> N:
    try:
        v = number_type(input(hint).strip())
    except ValueError:
        raise SystemExit('Please input a valid number')
    if min is not None and v <= min:
        raise SystemExit(f'Please input a number that is greater than {min}')
    return v


def create_row_formatter(column_widths: list[int]) -> Callable[[list], str]:
    def formatter(values: list):
        return ''.join(str(v).ljust(column_widths[i]) for i, v in enumerate(values))
    return formatter

def main():
    print(INTRO)
    radius_inc_unit = 6
    initial_radius = 6
    max_radius = number_input('Enter the value for N: ', int, min=6)
    side_length = number_input('Enter the length of side a: ', float, min=0)

    # print header
    row_ = create_row_formatter([12, 16, 20, 13])
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

