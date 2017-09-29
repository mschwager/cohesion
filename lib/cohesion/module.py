#!/usr/bin/env python

import collections

from cohesion import parser
from cohesion import filesystem


class Module(object):
    def __init__(self, module_contents):
        file_ast_node = parser.get_ast_node_from_string(module_contents)

        self.structure = self._create_structure(file_ast_node)

    def classes(self):
        return list(self.structure.keys())

    def functions(self, class_name):
        return list(self.structure[class_name]["functions"].keys())

    def class_variables(self, class_name):
        return self.structure[class_name]["variables"]

    def function_variables(self, class_name, function_name):
        return self.structure[class_name]["functions"][function_name]["variables"]

    @classmethod
    def from_file(cls, filename):
        file_contents = filesystem.get_file_contents(filename)

        return cls(file_contents)

    @staticmethod
    def _create_structure(file_ast_node):
        module_classes = parser.get_module_classes(file_ast_node)

        result = collections.defaultdict(dict)

        for module_class in module_classes:
            class_name = parser.get_object_name(module_class)

            class_variable_names = list(parser.get_all_class_variable_names(module_class))

            class_methods = parser.get_class_methods(module_class)

            class_method_name_to_method = {
                method.name: method
                for method in class_methods
            }

            class_method_name_to_variable_names = {
                method_name: list(parser.get_all_class_variable_names_used_in_method(method))
                for method_name, method in class_method_name_to_method.items()
            }

            class_method_name_to_boundedness = {
                method_name: parser.is_class_method_bound(method)
                for method_name, method in class_method_name_to_method.items()
            }

            class_method_name_to_staticmethodness = {
                method_name: parser.is_class_method_staticmethod(method)
                for method_name, method in class_method_name_to_method.items()
            }

            class_method_name_to_classmethodness = {
                method_name: parser.is_class_method_classmethod(method)
                for method_name, method in class_method_name_to_method.items()
            }

            result[class_name]["variables"] = class_variable_names
            result[class_name]["functions"] = {
                method_name: {
                    "variables": class_method_name_to_variable_names[method_name],
                    "bounded": class_method_name_to_boundedness[method_name],
                    "staticmethod": class_method_name_to_staticmethodness[method_name],
                    "classmethod": class_method_name_to_classmethodness[method_name],
                }
                for method_name in class_method_name_to_method.keys()
            }

        return result
