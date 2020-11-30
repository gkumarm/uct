"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class TodoIndexViewTestCase(TestCase):
    def test_index(self):
        resp = self.client.get('/todo_index/')
        self.assertEqual(resp.status_code, 200)