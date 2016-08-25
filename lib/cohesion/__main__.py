#!/usr/bin/env python

from __future__ import print_function

import argparse
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cohesion import parser
from cohesion import filesystem


class ModuleStructureEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def percentage(part, whole):
    if not whole:
        return 0.0

    return 100.0 * float(part) / float(whole)


def leftpad_print(s, leftpad_length=0):
    print(" " * leftpad_length + s)


def print_module_structure(filename, module_structure, verbose=False):
    leftpad_print("File: {}".format(filename), leftpad_length=0)

    for class_name, class_structure in module_structure.items():
        leftpad_print("Class: {}".format(class_name), leftpad_length=2)

        class_variable_count = len(class_structure["variables"])

        total_function_variable_percentage = 0.0
        for function_name, function_structure in class_structure["functions"].items():
            function_variable_count = len(function_structure["variables"])
            function_variable_percentage = percentage(
                function_variable_count,
                class_variable_count
            )

            function_output_string = "Function: {}".format(function_name)
            if function_structure["staticmethod"]:
                function_output_string = "{} staticmethod".format(function_output_string)
            elif function_structure["classmethod"]:
                function_output_string = "{} classmethod".format(function_output_string)
            elif not function_structure["bounded"]:
                function_variable_percentage = 0.0
                function_output_string = "{0} {1}/{2} 0.0%".format(
                    function_output_string,
                    function_variable_count,
                    class_variable_count
                )
            else:
                function_output_string = "{0} {1}/{2} {3:.2f}%".format(
                    function_output_string,
                    function_variable_count,
                    class_variable_count,
                    function_variable_percentage
                )

            leftpad_print(function_output_string, leftpad_length=4)

            if verbose:
                for class_variable_name in sorted(class_structure["variables"]):
                    if class_variable_name in function_structure["variables"]:
                        leftpad_print(
                            "Variable: {} True".format(class_variable_name),
                            leftpad_length=6
                        )
                    else:
                        leftpad_print(
                            "Variable: {} False".format(class_variable_name),
                            leftpad_length=6
                        )

            total_function_variable_percentage += function_variable_percentage

        class_function_count = len(class_structure["functions"])
        if class_function_count:
            class_variable_percentage = total_function_variable_percentage / class_function_count
        else:
            class_variable_percentage = 0.0

        leftpad_print("Total: {0:.2f}%".format(class_variable_percentage), leftpad_length=4)


def get_module_structure(module_ast_node):
    module_classes = parser.get_module_classes(module_ast_node)

    result = {}
    for module_class in module_classes:
        class_name = parser.get_object_name(module_class)

        class_variable_names = parser.get_all_class_variable_names(module_class)

        class_methods = parser.get_class_methods(module_class)

        class_method_name_to_method = {
            method.name: method
            for method in class_methods
        }

        class_method_name_to_variable_names = {
            method_name: parser.get_all_class_variable_names_used_in_method(method)
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

        result[class_name] = {}
        result[class_name]["variables"] = class_variable_names
        result[class_name]["functions"] = {}
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


def parse_args():
    p = argparse.ArgumentParser(description='''
        A tool for measuring Python class cohesion.
        ''', formatter_class=argparse.RawTextHelpFormatter)

    output_group = p.add_mutually_exclusive_group()
    output_group.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='print more verbose output'
    )
    output_group.add_argument(
        '-x',
        '--debug',
        action='store_true',
        help='print debugging output'
    )

    files_group = p.add_mutually_exclusive_group(required=True)
    files_group.add_argument(
        '-f',
        '--files',
        action='store',
        nargs='+',
        help='analyze these Python files'
    )
    files_group.add_argument(
        '-d',
        '--directory',
        action='store',
        help='recursively analyze this directory of Python files'
    )

    args = p.parse_args()

    return args


def main():
    args = parse_args()

    if args.files:
        files = args.files
    elif args.directory:
        files = filesystem.recursively_get_python_files_from_directory(args.directory)

    file_contents = {
        filename: filesystem.get_file_contents(filename)
        for filename in files
    }

    file_ast_nodes = {
        filename: parser.get_ast_node_from_string(contents)
        for filename, contents in file_contents.items()
    }

    for filename, file_ast_node in file_ast_nodes.items():
        module_structure = get_module_structure(file_ast_node)

        if args.debug:
            print(json.dumps(
                module_structure,
                cls=ModuleStructureEncoder,
                indent=4,
                separators=(',', ': ')
            ))
        else:
            print_module_structure(filename, module_structure, args.verbose)


if __name__ == "__main__":
    main()
