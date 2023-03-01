import csv
import io
from utils import create_row_formatter
from typing import Callable, Any


class BaseTable:
    columns: list[str]
    row_map: dict[Any, tuple]
    rows: list[tuple]
    column_formatter_map: dict[int, Callable] = {}

    def __init__(self) -> None:
        self.row_map = {}
        self.rows = []

    def add_row(self, row_id, row: tuple):
        """Idempotently add a row, if row_id is in row_map, do nothing"""
        if row_id in self.row_map:
            return
        self.row_map[row_id] = row
        self.rows.append(row)
    
    def format_columns_in_row(self, row: tuple):
        new_row = []
        for index, value in enumerate(row):
            if index in self.column_formatter_map:
                value = self.column_formatter_map[index](value)
            new_row.append(value)
        return new_row
    
    def print(self):
        column_max_width_map = dict((index, len(name) + 2) for index, name in enumerate(self.columns))

        # loop rows to update max width of each column
        for row in self.rows:
            for index, value in enumerate(row):
                width = len(str(value)) + 2
                if width > column_max_width_map[index]:
                    column_max_width_map[index] = width

        # create the formatter for each row
        format_row = create_row_formatter(
            [(column_max_width_map[index], 1) for index, _ in enumerate(self.columns)], '|', True)

        # draw header and separator of rows
        separator_row = '+' + '+'.join(column_max_width_map[index] * '-' for index, _ in enumerate(self.columns)) + '+'

        buf = []
        buf.append(separator_row)
        buf.append(format_row(self.columns))
        buf.append(separator_row)

        for row in self.rows:
            buf.append(format_row(self.format_columns_in_row(row)))

        buf.append(separator_row)
        print('\n'.join(buf))


class EmployeeInfoTable(BaseTable):
    columns = ['Employee Id', 'Employee Name', 'Department']


class EmployeeVacationsTable(BaseTable):
    columns = ['Employee ID', 'Year', 'Vacation Days']

    column_formatter_map = {
        # add spaces to the left of the value of 'Vacation Days' column
        2: lambda s: 7 * ' ' + str(s),
    }


class EmployeeTotalVacationsTable(BaseTable):
    columns = ['Employee ID', 'Employee Name', 'Department', 'Year', 'Vacation Days']

    column_formatter_map = {
        # add spaces to the left of the value of 'Vacation Days' column
        4: lambda s: 7 * ' ' + str(s),
    }


def main():
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

    reader = csv.reader(io.StringIO(csv_data))
    # skip first line
    next(reader)

    employee_info_table = EmployeeInfoTable()
    employee_vacations_table = EmployeeVacationsTable()

    for row in reader:
        employee_id, employee_name, department, _year, _vacation_days = tuple(row)
        # convert year and vacation_days to int
        year = int(_year)
        vacation_days = int(_vacation_days)

        employee_info_table.add_row(employee_id, [employee_id, employee_name, department])

        new_id = len(employee_vacations_table.row_map) + 1
        employee_vacations_table.add_row(new_id, [employee_id, year, vacation_days])

    print('2NF Table: Employee Info')
    employee_info_table.print()
    print()

    print('2NF Table: Employee Annual Vacations')
    employee_vacations_table.print()
    print()

    # calculate (employee_id, year) total vacation days
    employ_total_vacations_counter = {}
    for row in employee_vacations_table.rows:
        employee_id, year, vacation_days = row
        key = (employee_id, year)
        if key not in employ_total_vacations_counter:
            employ_total_vacations_counter[key] = 0
        employ_total_vacations_counter[key] += vacation_days
    
    # add rows to EmployeeTotalVacationsTable
    employ_total_vacations_table = EmployeeTotalVacationsTable()
    for key, total_vacations in employ_total_vacations_counter.items():
        employee_id, year = key
        _, employee_name, department = employee_info_table.row_map[employee_id]
        employ_total_vacations_table.add_row(key, [employee_id, employee_name, department, year, total_vacations])

    # sort by employee_name (column 1) and year (column 3)
    employ_total_vacations_table.rows.sort(key=lambda x: (x[1], x[3]))

    print('Total vacation days per year for each employee:')
    employ_total_vacations_table.print()


if __name__ == '__main__':
    main()
