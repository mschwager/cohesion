#!/usr/bin/env python3

import os


def get_file_contents(filename):
    with open(filename) as fd:
        return fd.read()


def is_python_file(filename):
    return filename.endswith('.py')


def recursively_get_files_from_directory(directory):
    return [
        os.path.join(root, filename)
        for root, directories, filenames in os.walk(directory)
        for filename in filenames
    ]


def recursively_get_python_files_from_directory(directory):
    return [
        filename
        for filename in recursively_get_files_from_directory(directory)
        if is_python_file(filename)
    ]
