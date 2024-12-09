#!/usr/bin/env python

import os


def get_file_contents(filename):
    """
    Return contents of a file
    """
    with open(filename) as fd:
        return fd.read()


def is_python_file(filename):
    """
    Return whether a file is a Python file or not
    """
    return filename.endswith('.py')


def recursively_get_files_from_directory(directory):
    """
    Return all filenames under recursively found in a directory
    """
    return [
        os.path.join(root, filename)
        for root, directories, filenames in os.walk(directory)
        for filename in filenames
    ]


def recursively_get_python_files_from_directory(directory):
    """
    Return all Python filenames under recursively found in a directory
    """
    return [
        filename
        for filename in recursively_get_files_from_directory(directory)
        if is_python_file(filename)
    ]
