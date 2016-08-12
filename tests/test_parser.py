#!/usr/bin/env python3

import ast
import unittest

from cohesion import parser


class TestParser(unittest.TestCase):

    def assertEmpty(self, iterable):
        self.assertEqual(len(iterable), 0)

    @staticmethod
    def unindent_string(string):
        """
        Block strings of code will complain about indentation in the
        containing function. Let's fix that up
        """
        return "\n".join(s[8:] for s in string.split("\n"))

    def test_valid_syntax(self):
        python_string = self.unindent_string("""
        a = 5
        """)

        result = parser.get_ast_node_from_string(python_string)
        expected = ast.Module

        self.assertIsInstance(result, expected)

    def test_invalid_syntax(self):
        python_string = self.unindent_string("""
        a )= 5
        """)

        with self.assertRaises(SyntaxError):
            parser.get_ast_node_from_string(python_string)

    def test_get_module_classes_empty(self):
        python_string = self.unindent_string("""
        def func(arg1):
            print("Hi")
        """)

        node = parser.get_ast_node_from_string(python_string)
        result = parser.get_module_classes(node)

        self.assertEmpty(result)

    def test_get_module_classes_single(self):
        python_string = self.unindent_string("""
        class Cls(object):
            pass
        """)

        node = parser.get_ast_node_from_string(python_string)
        classes = parser.get_module_classes(node)
        result = [cls.name for cls in classes]
        expected = ["Cls"]

        self.assertEqual(result, expected)

    def test_get_module_classes_multiple(self):
        python_string = self.unindent_string("""
        class Cls1(object):
            pass
        class Cls2(object):
            pass
        """)

        node = parser.get_ast_node_from_string(python_string)
        classes = parser.get_module_classes(node)
        result = [cls.name for cls in classes]
        expected = ["Cls1", "Cls2"]

        self.assertEqual(result, expected)

    def test_get_class_methods_empty(self):
        python_string = self.unindent_string("""
        class Cls(object):
            pass
        """)

        node = parser.get_ast_node_from_string(python_string)
        result = [
            method
            for cls in parser.get_module_classes(node)
            for method in parser.get_class_methods(cls)
        ]

        self.assertEmpty(result)

    def test_get_class_methods_single(self):
        python_string = self.unindent_string("""
        class Cls(object):
            def func1(self, arg1):
                pass
        """)

        node = parser.get_ast_node_from_string(python_string)
        methods = [
            method
            for cls in parser.get_module_classes(node)
            for method in parser.get_class_methods(cls)
        ]
        result = [method.name for method in methods]
        expected = ["func1"]

        self.assertEqual(result, expected)

    def test_get_class_methods_multiple(self):
        python_string = self.unindent_string("""
        class Cls1(object):
            def func1(self, arg1):
                pass
            def func2(self, arg1):
                pass
        class Cls2(object):
            def func3(self, arg1):
                pass
        """)

        node = parser.get_ast_node_from_string(python_string)
        methods = [
            method
            for cls in parser.get_module_classes(node)
            for method in parser.get_class_methods(cls)
        ]
        result = [method.name for method in methods]
        expected = ["func1", "func2", "func3"]

        self.assertEqual(result, expected)

    def test_get_class_methods_avoid_nested(self):
        python_string = self.unindent_string("""
        class Cls(object):
            def func1(self, arg1):
                def func2(arg2):
                    pass
                print("Hi")
        """)

        node = parser.get_ast_node_from_string(python_string)
        methods = [
            method
            for cls in parser.get_module_classes(node)
            for method in parser.get_class_methods(cls)
        ]
        result = [method.name for method in methods]
        expected = ["func1"]

        self.assertEqual(result, expected)

    def test_get_class_methods_avoid_lambda(self):
        python_string = self.unindent_string("""
        class Cls(object):
            def func1(self, arg1):
                func2 = lambda arg: arg
                pass
        """)

        node = parser.get_ast_node_from_string(python_string)
        methods = [
            method
            for cls in parser.get_module_classes(node)
            for method in parser.get_class_methods(cls)
        ]
        result = [method.name for method in methods]
        expected = ["func1"]

        self.assertEqual(result, expected)

    def test_bound_method_is_bound(self):
        python_string = self.unindent_string("""
        class Cls(object):
            def func(self, arg1):
                pass
        """)

        node = parser.get_ast_node_from_string(python_string)
        methods = [
            method
            for cls in parser.get_module_classes(node)
            for method in parser.get_class_methods(cls)
            if parser.is_class_method_bound(method)
        ]
        result = [method.name for method in methods]
        expected = ["func"]

        self.assertEqual(result, expected)

    def test_bound_method_non_default_name(self):
        python_string = self.unindent_string("""
        class Cls(object):
            def func(this, arg1):
                pass
        """)

        node = parser.get_ast_node_from_string(python_string)
        methods = [
            method
            for cls in parser.get_module_classes(node)
            for method in parser.get_class_methods(cls)
            if parser.is_class_method_bound(method, arg_name="this")
        ]
        result = [method.name for method in methods]
        expected = ["func"]

        self.assertEqual(result, expected)

    def test_bound_method_static(self):
        python_string = self.unindent_string("""
        class Cls(object):
            @staticmethod
            def func(arg1):
                pass
        """)

        node = parser.get_ast_node_from_string(python_string)
        methods = [
            method
            for cls in parser.get_module_classes(node)
            for method in parser.get_class_methods(cls)
            if parser.is_class_method_bound(method)
        ]
        result = [method.name for method in methods]

        self.assertEmpty(result)

    def test_bound_method_unbound(self):
        python_string = self.unindent_string("""
        class Cls(object):
            def func(arg1):
                pass
        """)

        node = parser.get_ast_node_from_string(python_string)
        methods = [
            method
            for cls in parser.get_module_classes(node)
            for method in parser.get_class_methods(cls)
            if parser.is_class_method_bound(method)
        ]
        result = [method.name for method in methods]

        self.assertEmpty(result)

    def test_get_instance_variables_from_class_single(self):
        python_string = self.unindent_string("""
        class Cls(object):
            def __init__(self):
                self.attr = 5
        """)

        node = parser.get_ast_node_from_string(python_string)
        instance_variables = parser.get_instance_variables(node)
        result = [instance_variable.attr for instance_variable in instance_variables]
        expected = ["attr"]

        self.assertEqual(result, expected)

    def test_get_instance_variables_from_class_multiple(self):
        python_string = self.unindent_string("""
        class Cls(object):
            def __init__(self):
                self.attr1 = 5
                self.attr2 = 6
        """)

        node = parser.get_ast_node_from_string(python_string)
        instance_variables = parser.get_instance_variables(node)
        result = [instance_variable.attr for instance_variable in instance_variables]
        expected = ["attr1", "attr2"]

        self.assertEqual(result, expected)

    def test_get_instance_variables_from_class_multiple_same_line(self):
        python_string = self.unindent_string("""
        class Cls(object):
            def __init__(self):
                self.attr1 = self.attr2 = 5
        """)

        node = parser.get_ast_node_from_string(python_string)
        instance_variables = parser.get_instance_variables(node)
        result = [instance_variable.attr for instance_variable in instance_variables]
        expected = ["attr1", "attr2"]

        self.assertEqual(result, expected)

    def test_get_instance_variables_from_class_avoid_class_variable(self):
        python_string = self.unindent_string("""
        class Cls(object):
            attr = 5
        """)

        node = parser.get_ast_node_from_string(python_string)
        instance_variables = parser.get_instance_variables(node)
        result = [instance_variable.attr for instance_variable in instance_variables]

        self.assertEmpty(result)

    def test_get_class_variables_from_class_single(self):
        python_string = self.unindent_string("""
        class Cls(object):
            attr = 5
        """)

        node = parser.get_ast_node_from_string(python_string)
        classes = parser.get_module_classes(node)
        class_variables = [
            class_variable
            for cls in classes
            for class_variable in parser.get_class_variables(cls)
        ]
        result = [class_variable.id for class_variable in class_variables]
        expected = ["attr"]

        self.assertEqual(result, expected)

    def test_get_class_variables_from_class_multiple_targets(self):
        python_string = self.unindent_string("""
        class Cls(object):
            attr1 = attr2 = 5
        """)

        node = parser.get_ast_node_from_string(python_string)
        classes = parser.get_module_classes(node)
        class_variables = [
            class_variable
            for cls in classes
            for class_variable in parser.get_class_variables(cls)
        ]
        result = [class_variable.id for class_variable in class_variables]
        expected = ["attr1", "attr2"]

        self.assertEqual(result, expected)

    def test_get_class_variables_from_class_avoid_instance_variable(self):
        python_string = self.unindent_string("""
        class Cls(object):
            def __init__(self):
                self.attr = 5
        """)

        node = parser.get_ast_node_from_string(python_string)
        classes = parser.get_module_classes(node)
        class_variables = [
            class_variable
            for cls in classes
            for class_variable in parser.get_class_variables(cls)
        ]
        result = [class_variable.id for class_variable in class_variables]

        self.assertEmpty(result)


if __name__ == "__main__":
    unittest.main()