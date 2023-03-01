import csv
import io
from dataclasses import dataclass
from utils import create_row_formatter
from typing import Callable, Optional


@dataclass
class EmployeeInfo:
    id: str
    employee_name: str
    department: str


@dataclass
class EmployeeAnnualVacations:
    id: str
    employee_id: str
    year: int
    vacation_days: int


def print_table(columns: list[tuple[str, str, Optional[Callable]]], items: list):
    """
    column is defined by a tuple of (name, attribute, formatter)
    """

    column_max_width_map = dict((attr, len(name) + 2) for name, attr, _ in columns)

    # create rows (list of values) from items (list of objects)
    rows = []
    for item in items:
        row = []
        for _, attr, formatter in columns:
            v = str(getattr(item, attr))
            # update max width of the column
            width = len(v) + 2
            if width > column_max_width_map[attr]:
                column_max_width_map[attr] = width

            # append the value to the row
            if formatter is not None:
                v = formatter(v)
            row.append(v)
        rows.append(row)

    # create the formatter for each row
    row_formatter = create_row_formatter(
        [(column_max_width_map[attr], 1) for _, attr, _ in columns], '|', True)

    # draw header and separator of rows
    separator_row = '+' + '+'.join(column_max_width_map[attr] * '-' for _, attr, _ in columns) + '+'

    buf = []
    buf.append(separator_row)
    buf.append(row_formatter([name for name, _, _ in columns]))
    buf.append(separator_row)

    for row in rows:
        buf.append(row_formatter(row))

    buf.append(separator_row)
    print('\n'.join(buf))



def main(file):
    reader = csv.reader(file)
    # skip first line
    next(reader)

    employee_info_table = {}
    employee_annual_vacations_table = {}

    for row in reader:
        employee_id, employee_name, department, _year, _vacation_days = tuple(row)
        # convert year and vacation_days to int
        year = int(_year)
        vacation_days = int(_vacation_days)

        if employee_id not in employee_info_table:
            employee_info_table[employee_id] = EmployeeInfo(employee_id, employee_name, department)

        if employee_id not in employee_annual_vacations_table:
            new_id = len(employee_annual_vacations_table) + 1
            employee_annual_vacations_table[new_id] = EmployeeAnnualVacations(new_id, employee_id, year, vacation_days)

    print('2NF Table: Employee Info')
    print_table([
        ('Employee Id', 'id', None),
        ('Employee Name', 'employee_name', None),
        ('Department', 'department', None),
    ], employee_info_table.values())
    print()

    print('2NF Table: Employee Annual Vacations')
    print_table([
        ('Id', 'id', None),
        ('Employee Id', 'employee_id', None),
        ('Year', 'year', None),
        ('Vacation Days', 'vacation_days', lambda s: 7 * ' ' + s),
    ], employee_annual_vacations_table.values())



if __name__ == '__main__':
    csv_data  = """\
"Employee Id","Employee Name","Department","Year","Vacation Days"
00012,"Luke Ye",Sales,2011,6
00013,"Mark Brown",Marketing,2012,2
00016,"James Tevlin",Engineering,2011,4
00017,"Ross Becker",HR,2012,1
00012,"Luke Ye",Sales,2013,2
00014,"John Smith",Management,2011,10
00013,"Mark Brown",Marketing,2012,5
00016,"James Tevlin",Engineering,2012,3
00017,"Ross Becker",HR,2013,2
00017,"Ross Becker",HR,2012,3
00015,"Mark Brown",Marketing,2013,8
00012,"Luke Ye",Sales,2012,1
00014,"John Smith",Management,2011,3
00015,"Mark Brown",Marketing,2014,2"""

    main(io.StringIO(csv_data))
