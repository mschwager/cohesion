#!/usr/bin/env python

from __future__ import print_function

import argparse
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cohesion import parser
from cohesion import filesystem


def percentage(part, whole):
    if not whole:
        return 0.0

    return 100.0 * float(part) / float(whole)


def print_module_cohesion(module_ast_node, verbose=False):
    module_classes = parser.get_module_classes(module_ast_node)

    for module_class in module_classes:
        class_variable_names = parser.get_all_class_variable_names(module_class)

        class_methods = parser.get_class_methods(module_class)

        class_method_name_to_method = {
            method.name: method
            for method in class_methods
        }

        class_method_name_to_variable_names_used = {
            method_name: parser.get_all_class_variable_names_used_in_method(method)
            for method_name, method in class_method_name_to_method.items()
        }

        class_method_boundedness = {
            method_name: parser.is_class_method_bound(method)
            for method_name, method in class_method_name_to_method.items()
        }

        print("  Class: {}".format(module_class.name))

        total_method_percentage = 0.0
        for class_method_name in sorted(class_method_name_to_method.keys()):
            method_variable_names = class_method_name_to_variable_names_used[class_method_name]
            method_variable_count = len(method_variable_names)
            class_variable_count = len(class_variable_names)

            if class_method_boundedness[class_method_name]:
                method_percentage = percentage(
                    method_variable_count,
                    class_variable_count
                )
            else:
                method_percentage = 0.0

            print("    Function: {0} {1}/{2} {3:.2f}%".format(
                class_method_name,
                method_variable_count,
                class_variable_count,
                method_percentage
            ))

            if verbose:
                for variable_name in sorted(class_variable_names):
                    variable_in_method = variable_name in method_variable_names
                    print("      Variable: {0} {1}".format(variable_name, variable_in_method))

            total_method_percentage += method_percentage

        class_percentage = total_method_percentage / len(class_methods) if class_methods else 0.0
        print("    Total: {0:.2f}%".format(class_percentage))


def parse_args():
    p = argparse.ArgumentParser(description='''
        A tool for measuring Python class cohesion.
        ''', formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='print more verbose output'
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
        print("File: {}".format(filename))
        print_module_cohesion(file_ast_node, args.verbose)


if __name__ == "__main__":
    main()
