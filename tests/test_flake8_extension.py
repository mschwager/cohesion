#!/usr/bin/env python

import textwrap
import sys
import os
import unittest

from cohesion import parser

# Since flake8_extension imports cohesion we cannot add it to the
# module, and thus must come up with some tricks to import it
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "lib",
        "cohesion"
    )
)

import flake8_extension


class TestFlake8Extension(unittest.TestCase):

    def assertEmpty(self, iterable):
        self.assertEqual(len(iterable), 0)

    def test_flake8_extension_empty(self):
        python_string = textwrap.dedent("")

        ast_node = parser.get_ast_node_from_string(python_string)
        checker = flake8_extension.CohesionChecker(ast_node, "unused")
        checker.cohesion_below = 0.0

        result = list(checker.run())

        self.assertEmpty(result)

    def test_flake8_extension_basic(self):
        python_string = textwrap.dedent("""
        class Cls(object):
            pass
        """)

        ast_node = parser.get_ast_node_from_string(python_string)
        checker = flake8_extension.CohesionChecker(ast_node, "unused")
        checker.cohesion_below = 0.0

        result = list(checker.run())
        expected = [
            (
                2,
                0,
                flake8_extension.CohesionChecker._error_tmpl.format(0.0),
                flake8_extension.CohesionChecker
            ),
        ]

        self.assertEqual(result, expected)

    def test_flake8_extension_high(self):
        python_string = textwrap.dedent("""
        class Cls(object):
            def func(self):
                self.variable = 'foo'
        """)

        ast_node = parser.get_ast_node_from_string(python_string)
        checker = flake8_extension.CohesionChecker(ast_node, "unused")
        checker.cohesion_below = 50.0

        result = list(checker.run())

        self.assertEmpty(result)

    def test_flake8_extension_low(self):
        python_string = textwrap.dedent("""
        class Cls(object):
            variable1 = 'foo'
            variable2 = 'bar'
            def func(self):
                self.variable2 = 'baz'
        """)

        ast_node = parser.get_ast_node_from_string(python_string)
        checker = flake8_extension.CohesionChecker(ast_node, "unused")
        checker.cohesion_below = 75.0

        result = list(checker.run())
        expected = [
            (
                2,
                0,
                flake8_extension.CohesionChecker._error_tmpl.format(50.0),
                flake8_extension.CohesionChecker
            ),
        ]

        self.assertEqual(result, expected)

    def test_flake8_extension_bad_option_type(self):
        python_string = textwrap.dedent("""
        class Cls(object):
            def func(self):
                self.variable = 'foo'
        """)

        ast_node = parser.get_ast_node_from_string(python_string)
        checker = flake8_extension.CohesionChecker(ast_node, "unused")
        checker.cohesion_below = str(0.0)

        result = list(checker.run())

        self.assertEmpty(result)


if __name__ == "__main__":
    unittest.main()
