from django.test import SimpleTestCase
from .models import QueryReportFactory, DailyReport, WeeklyReport, MonthlyReport


class FactoryTest(SimpleTestCase):
    def test_daily(self):
        r = QueryReportFactory.create("daily", [])
        self.assertIsInstance(r, DailyReport)

    def test_weekly(self):
        r = QueryReportFactory.create("weekly", [])
        self.assertIsInstance(r, WeeklyReport)

    def test_monthly(self):
        r = QueryReportFactory.create("monthly", [])
        self.assertIsInstance(r, MonthlyReport)

    def test_unknown_type(self):
        with self.assertRaises(ValueError):
            QueryReportFactory.create("yearly", [])