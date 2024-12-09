#!/usr/bin/env python

import os
import textwrap
import unittest

from cohesion import filesystem

from pyfakefs import fake_filesystem_unittest


class TestFilesystem(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    def tearDown(self):
        # It is no longer necessary to add self.tearDownPyfakefs()
        pass

    def test_get_file_contents(self):
        filename = os.path.join("directory", "filename.py")

        contents = textwrap.dedent("""
        class Cls(object):
            pass
        """)

        self.fs.create_file(
            filename,
            contents=contents
        )
        result = filesystem.get_file_contents(filename)

        self.assertEqual(result, contents)

    def test_recursively_get_files_from_directory(self):
        filenames = [
            os.path.join(".", "filename.txt"),
            os.path.join(".", "directory", "inner_file.txt"),
            os.path.join(".", "directory", "nested", "deep_file.py"),
        ]

        for filename in filenames:
            self.fs.create_file(filename, contents='')

        result = filesystem.recursively_get_files_from_directory('.')

        self.assertCountEqual(result, filenames)

    def test_recursively_get_python_files_from_directory(self):
        filenames = [
            os.path.join(".", "filename.txt"),
            os.path.join(".", "upper.py"),
            os.path.join(".", "directory", "inner_file.txt"),
            os.path.join(".", "directory", "nested", "deep_file.py"),
        ]

        for filename in filenames:
            self.fs.create_file(filename, contents='')

        result = filesystem.recursively_get_python_files_from_directory('.')
        expected = [
            os.path.join(".", "upper.py"),
            os.path.join(".", "directory", "nested", "deep_file.py"),
        ]

        self.assertCountEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
