#!/usr/bin/env python

import cohesion


class CohesionChecker(object):
    name = cohesion.__name__
    version = cohesion.__version__
    off_by_default = True

    _code = 'H601'
    _error_tmpl = 'H601 class has low ({0:.2f}%) cohesion'

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename

    @classmethod
    def add_options(cls, parser):
        flag = '--cohesion-below'
        kwargs = {
            'action': 'store',
            'type': 'float',
            'default': 50.0,
            'help': 'only show cohesion results with this percentage or lower',
            'parse_from_config': 'True',
        }
        config_opts = getattr(parser, 'config_options', None)
        if isinstance(config_opts, list):
            # flake8 2.x
            kwargs.pop('parse_from_config')
            parser.add_option(flag, **kwargs)
            parser.config_options.append('cohesion-below')
        else:
            # flake8 3.x
            parser.add_option(flag, **kwargs)

    @classmethod
    def parse_options(cls, options):
        cls.cohesion_below = options.cohesion_below

    def run(self):
        file_module = cohesion.module.Module(self.tree)
        file_module.filter_below(float(self.cohesion_below))

        for class_name in file_module.classes():
            cohesion_percentage = file_module.class_cohesion_percentage(class_name)
            yield (
                file_module.structure[class_name]['lineno'],
                file_module.structure[class_name]['col_offset'],
                self._error_tmpl.format(cohesion_percentage),
                type(self)
            )
