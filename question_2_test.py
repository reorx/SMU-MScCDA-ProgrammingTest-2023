import unittest
from question_2 import Project, analyse_projects


def create_project(name, upfront_cost, rate_of_return_percent, duration_in_years, cash_io_of_years):
    p = Project()
    p.name = name
    p.upfront_cost = upfront_cost
    p.rate_of_return_percent = rate_of_return_percent
    p.duration_in_years = duration_in_years
    p.cash_io_of_years = cash_io_of_years
    return p


p_mars = create_project(
    'Mars',
    35000.0,
    12.0,
    3,
    [10000.0, 27000.0, 19000.0],
)


p_inception = create_project(
    'Inception',
    35000.0,
    12.0,
    2,
    [27000.0, 27000.0],
)


class TestQuestion2(unittest.TestCase):
    def test_project_mars(self):

        expected_output = """\
                        Mars
----------------------------------------------------------
Year    |         Cash         |  PV Factor  |  Amount
        |    Inflows/Outflows  |
----------------------------------------------------------
1       |      $10,000.00      |    0.8929   |  $8,928.57 
2       |      $27,000.00      |    0.7972   |  $21,524.23
3       |      $19,000.00      |    0.7118   |  $13,523.82
Total Income: $56,000.00
Present Value of Future Benefits: $43,976.63
Present Value of Future Costs: $35,000.00
Net Present Value(NPV): $8,976.63"""

        self.maxDiff = None
        self.assertEqual(p_mars.calculate_result(), expected_output)

    def test_project_inception(self):

        expected_output = """\
                        Inception
----------------------------------------------------------
Year    |         Cash         |  PV Factor  |  Amount
        |    Inflows/Outflows  |
----------------------------------------------------------
1       |      $27,000.00      |    0.8929   |  $24,107.14
2       |      $27,000.00      |    0.7972   |  $21,524.23
Total Income: $54,000.00
Present Value of Future Benefits: $45,631.38
Present Value of Future Costs: $35,000.00
Net Present Value(NPV): $10,631.38"""
        self.maxDiff = None
        self.assertEqual(p_inception.calculate_result(), expected_output)

    def test_analyse_2_projects(self):
        highest_income_p, highest_npv_p = analyse_projects([p_mars, p_inception])
        self.assertEqual(highest_income_p.name, p_mars.name)
        self.assertEqual(highest_npv_p.name, p_inception.name)
