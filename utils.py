from typing import TypeVar, Type, Callable, Iterator


def esc(*codes: int) -> str:
    """Produces an ANSI escape code from a list of integers"""
    return '\x1b[{}m'.format(';'.join(str(c) for c in codes))


class ColorCode:
    FG_GREEN = esc(32)
    FG_END = esc(39)


def colored_input(hint) -> str:
    # add code for color start after the hint
    v = input(hint + ColorCode.FG_GREEN)
    # add code for color end after getting the input, without a newline
    print(ColorCode.FG_END, end='')
    # convert the input to the desired type
    return v


N = TypeVar('N', int, float)


def number_input(hint, number_type: Type[N], min=None) -> N:
    v = None
    while v is None:
        try:
            v = number_type(colored_input(hint).strip())
        except ValueError:
            print('Please input a valid number')
            continue
        if min is not None and v < min:
            print(f'Please input a number that is greater than or equal to {min}')
            continue
    return v


def str_input(hint, min_length=1) -> str:
    v = ''
    while not v:
        v = colored_input(hint).strip()
        if len(v) < min_length:
            print(f'Please input a string that is at least {min_length} characters long')
            continue
    return v


def create_row_formatter(columns: list[tuple[int, int]], delimeter='', wrap=False) -> Callable[[list], str]:
    """Create a formatter for rows in a table,
    each column is defined by a tuple of (width, left_padding)
    """
    def formatter(values: Iterator):
        l = []
        length = len(values)
        for i, v in enumerate(values):
            width, left_padding = columns[i]
            text = f'{" " * left_padding}{v}'.ljust(width)
            l.append(text)
        row = delimeter.join(l)
        if wrap:
            row = delimeter + row + delimeter
        return row
    return formatter
