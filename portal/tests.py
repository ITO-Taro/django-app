from django.test import TestCase

from django.test import TestCase
from portal.models import Employee

class EmplTestCase(TestCase):
    def setUp(self):
        Employee.objects.create(emp_id="EE-000TEST", title="BOSS", gender="F", last_name="TEST0", first_name="Test0", salary=1000000, city="Maitland", state="FL")
        Employee.objects.create(emp_id="EE-001TEST", title="KING", gender="M", last_name="TEST1", first_name="Test1", salary=1000000, city="Daytona Beach", state="FL")

    def test_emp_rank(self):
        """Employee's title is correctly identified"""
        boss = Employee.objects.get(title="BOSS")
        king = Employee.objects.get(title="KING")
        self.assertEqual(boss.title, "BOSS")
        self.assertEqual(king.title, "KING")