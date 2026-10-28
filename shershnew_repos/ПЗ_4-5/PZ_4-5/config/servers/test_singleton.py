from django.test import SimpleTestCase
from .singleton import SlowQueryMonitor


class SingletonTest(SimpleTestCase):
    def test_single_instance(self):
        m1 = SlowQueryMonitor()
        m2 = SlowQueryMonitor()
        self.assertIs(m1, m2)
        self.assertEqual(id(m1), id(m2))

    def test_shared_state(self):
        m1 = SlowQueryMonitor()
        m1.clear()
        m1.log_query("SELECT 1", 2000)
        m2 = SlowQueryMonitor()
        self.assertEqual(len(m2.get_queries()), 1)