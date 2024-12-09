#!/usr/bin/env python

from __future__ import print_function

import argparse
import json

from . import filesystem
from . import module


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
        class_output_string = "Class: {} ({}:{})".format(
            class_name,
            class_structure["lineno"],
            class_structure["col_offset"]
        )
        leftpad_print(class_output_string, leftpad_length=2)

        for function_name, function_structure in class_structure["functions"].items():
            function_variable_percentage = percentage(
                len(function_structure["variables"]),
                len(class_structure["variables"])
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
                    len(function_structure["variables"]),
                    len(class_structure["variables"])
                )
            else:
                function_output_string = "{0} {1}/{2} {3:.2f}%".format(
                    function_output_string,
                    len(function_structure["variables"]),
                    len(class_structure["variables"]),
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

        leftpad_print("Total: {}%".format(class_structure["cohesion"]), leftpad_length=4)


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

    def percentage(value):
        error_message = 'invalid percentage {!r} please specify a number between 0 and 100'.format(value)
        try:
            float_value = float(value)
        except ValueError:
            raise argparse.ArgumentTypeError(error_message)

        if not 0.0 <= float_value <= 100.0:
            raise argparse.ArgumentTypeError(error_message)

        return float_value

    filters_group = p.add_mutually_exclusive_group()
    filters_group.add_argument(
        '-b',
        '--below',
        action='store',
        type=percentage,
        default=None,
        help='only show results with this percentage or lower'
    )
    filters_group.add_argument(
        '-a',
        '--above',
        action='store',
        type=percentage,
        default=None,
        help='only show results with this percentage or higher'
    )

    args = p.parse_args()

    return args


def main():
    args = parse_args()

    if args.files:
        files = args.files
    elif args.directory:
        files = filesystem.recursively_get_python_files_from_directory(args.directory)

    file_modules = {
        filename: module.Module.from_file(filename)
        for filename in files
    }

    for filename, file_module in file_modules.items():
        if args.below:
            file_module.filter_below(args.below)
        elif args.above:
            file_module.filter_above(args.above)

        if args.debug:
            result = json.dumps(
                file_module.structure,
                cls=ModuleStructureEncoder,
                indent=4,
                separators=(',', ': ')
            )
            print(result)
        else:
            print_module_structure(filename, file_module.structure, args.verbose)


if __name__ == "__main__":
    main()
