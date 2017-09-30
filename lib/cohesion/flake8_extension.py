#!/usr/bin/env python

from cohesion import module


class CohesionChecker(object):
    name = 'cohesion'
    version = '0.7.0'
    off_by_default = True

    _code = 'C501'
    _error_tmpl = 'C501 has class {!r}'

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename

    @classmethod
    def add_options(cls, parser):
        flag = '--argument'
        kwargs = {
            'action': 'store_true',
            'parse_from_config': 'True',
        }
        config_opts = getattr(parser, 'config_options', None)
        if isinstance(config_opts, list):
            # flake8 2.x
            kwargs.pop('parse_from_config')
            parser.add_option(flag, **kwargs)
            parser.config_options.append('argument')
        else:
            # flake8 3.x
            parser.add_option(flag, **kwargs)

    @classmethod
    def parse_options(cls, options):
        cls.argument = options.argument

    def run(self):
        file_module = module.Module.from_file(self.filename)

        if not self.argument:
            for class_name in file_module.classes():
                output = self._error_tmpl.format(class_name)
                yield (
                    file_module.structure[class_name]['lineno'],
                    file_module.structure[class_name]['col_offset'],
                    output,
                    type(self)
                )