#!/usr/bin/env python

import collections
import textwrap
import unittest

from cohesion import module


class TestModule(unittest.TestCase):

    def assertEmpty(self, iterable):
        self.assertEqual(len(iterable), 0)

    def assertCountEqual(self, first, second):
        """
        Test whether two sequences contain the same elements.

        This exists in Python 3, but not Python 2.
        """
        self.assertEqual(
            collections.Counter(list(first)),
            collections.Counter(list(second))
        )

    def test_module_empty(self):
        python_string = textwrap.dedent("")

        python_module = module.Module(python_string)

        result = python_module.classes()

        self.assertEmpty(result)

    def test_module_class_empty(self):
        python_string = textwrap.dedent("""
        class Cls(object):
            pass
        """)

        python_module = module.Module(python_string)

        result = python_module.classes()
        expected = ["Cls"]

        self.assertEqual(result, expected)

    def test_module_function_empty(self):
        python_string = textwrap.dedent("""
        class Cls(object):
            def func(self):
                pass
        """)

        python_module = module.Module(python_string)

        result = python_module.functions("Cls")
        expected = ["func"]

        self.assertEqual(result, expected)

    def test_module_class_variable(self):
        python_string = textwrap.dedent("""
        class Cls(object):
            class_variable = 'foo'
            def func(self):
                pass
        """)

        python_module = module.Module(python_string)

        result = python_module.class_variables("Cls")
        expected = ["class_variable"]

        self.assertEqual(result, expected)

    def test_module_function_variable(self):
        python_string = textwrap.dedent("""
        class Cls(object):
            def func(self):
                self.function_variable = 'foo'
        """)

        python_module = module.Module(python_string)

        result = python_module.function_variables("Cls", "func")
        expected = ["function_variable"]

        self.assertEquals(result, expected)


if __name__ == "__main__":
    unittest.main()
