#!/usr/bin/env python

import os
import textwrap
import unittest

from cohesion import module

from pyfakefs import fake_filesystem_unittest


class TestModule(unittest.TestCase):

    def assertEmpty(self, iterable):
        self.assertEqual(len(iterable), 0)

    def test_module_empty(self):
        python_string = textwrap.dedent("")

        python_module = module.Module.from_string(python_string)

        result = python_module.classes()

        self.assertEmpty(result)

    def test_module_class_empty(self):
        python_string = textwrap.dedent("""
        class Cls(object):
            pass
        """)

        python_module = module.Module.from_string(python_string)

        result = python_module.classes()
        expected = ["Cls"]

        self.assertEqual(result, expected)

    def test_module_class_empty_cohesion_percent(self):
        python_string = textwrap.dedent("""
        class Cls(object):
            pass
        """)

        python_module = module.Module.from_string(python_string)

        result = python_module.class_cohesion_percentage("Cls")
        expected = 0.0

        self.assertEqual(result, expected)

    def test_module_function_empty(self):
        python_string = textwrap.dedent("""
        class Cls(object):
            def func(self):
                pass
        """)

        python_module = module.Module.from_string(python_string)

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

        python_module = module.Module.from_string(python_string)

        result = python_module.class_variables("Cls")
        expected = ["class_variable"]

        self.assertEqual(result, expected)

    def test_module_function_variable(self):
        python_string = textwrap.dedent("""
        class Cls(object):
            def func(self):
                self.function_variable = 'foo'
        """)

        python_module = module.Module.from_string(python_string)

        result = python_module.function_variables("Cls", "func")
        expected = ["function_variable"]

        self.assertEqual(result, expected)

    def test_module_filter_below_false(self):
        python_string = textwrap.dedent("""
        class Cls(object):
            class_variable = 'foo'
            def func(self):
                self.instance_variable = 'bar'
        """)

        python_module = module.Module.from_string(python_string)
        python_module.filter_below(40)

        result = python_module.classes()

        self.assertEmpty(result)

    def test_module_filter_below_true(self):
        python_string = textwrap.dedent("""
        class Cls(object):
            class_variable = 'foo'
            def func(self):
                self.instance_variable = 'bar'
        """)

        python_module = module.Module.from_string(python_string)
        python_module.filter_below(60)

        result = python_module.classes()
        expected = ["Cls"]

        self.assertEqual(result, expected)

    def test_module_filter_below_equal(self):
        python_string = textwrap.dedent("""
        class Cls(object):
            class_variable = 'foo'
            def func(self):
                self.instance_variable = 'bar'
        """)

        python_module = module.Module.from_string(python_string)
        python_module.filter_below(50)

        result = python_module.classes()
        expected = ["Cls"]

        self.assertEqual(result, expected)

    def test_module_filter_above_false(self):
        python_string = textwrap.dedent("""
        class Cls(object):
            class_variable = 'foo'
            def func(self):
                self.instance_variable = 'bar'
        """)

        python_module = module.Module.from_string(python_string)
        python_module.filter_above(60)

        result = python_module.classes()

        self.assertEmpty(result)

    def test_module_filter_above_true(self):
        python_string = textwrap.dedent("""
        class Cls(object):
            class_variable = 'foo'
            def func(self):
                self.instance_variable = 'bar'
        """)

        python_module = module.Module.from_string(python_string)
        python_module.filter_above(40)

        result = python_module.classes()
        expected = ["Cls"]

        self.assertEqual(result, expected)

    def test_module_filter_above_equal(self):
        python_string = textwrap.dedent("""
        class Cls(object):
            class_variable = 'foo'
            def func(self):
                self.instance_variable = 'bar'
        """)

        python_module = module.Module.from_string(python_string)
        python_module.filter_above(50)

        result = python_module.classes()
        expected = ["Cls"]

        self.assertEqual(result, expected)

    def test_module_class_cohesion_percentage(self):
        python_string = textwrap.dedent("""
        class Cls(object):
            class_variable = 'foo'
            def func(self):
                self.instance_variable = 'bar'
        """)

        python_module = module.Module.from_string(python_string)

        result = python_module.class_cohesion_percentage("Cls")
        expected = 50

        self.assertEqual(result, expected)

    def test_module_class_lineno(self):
        python_string = textwrap.dedent("""
        def foo():
            pass
        class Cls(object):
            pass
        """)

        python_module = module.Module.from_string(python_string)

        result = python_module.structure["Cls"]["lineno"]

        # Don't forget the initial newline
        expected = 4

        self.assertEqual(result, expected)

    def test_module_class_col_offset(self):
        python_string = textwrap.dedent("""
        def foo():
            class Cls(object):
                pass
        """)

        python_module = module.Module.from_string(python_string)

        result = python_module.structure["Cls"]["col_offset"]
        expected = 4

        self.assertEqual(result, expected)


class TestModuleFile(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    def tearDown(self):
        # It is no longer necessary to add self.tearDownPyfakefs()
        pass

    def test_module_from_file(self):
        filename = os.path.join("directory", "filename.py")

        contents = textwrap.dedent("""
        class Cls(object):
            pass
        """)

        self.fs.create_file(
            filename,
            contents=contents
        )
        file_module = module.Module.from_file(filename)

        result = file_module.classes()
        expected = ["Cls"]

        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
