#!/usr/bin/env python3

import ast

BOUND_METHOD_ARGUEMENT_NAME = "self"


def is_class_method_bound(method, arg_name=BOUND_METHOD_ARGUEMENT_NAME):
    """
    Return whether a class method is bound to the class
    """
    return method.args.args and method.args.args[0].arg == arg_name


def get_class_methods(cls):
    """
    Return methods associated with a given class
    """
    return [
        node
        for node in cls.body
        if isinstance(node, ast.FunctionDef)
    ]


def get_class_variables(cls):
    """
    Return class variables associated with a given class
    """
    return [
        target
        for node in cls.body
        if isinstance(node, ast.Assign)
        for target in node.targets
    ]


def get_instance_variables(node):
    """
    Return instance variables used in an AST node
    """
    return [
        child
        for child in ast.walk(node)
        if isinstance(child, ast.Attribute)
    ]


def get_all_class_variable_names_used_in_method(method):
    """
    Return the names of all instance variables associated with a
    given method
    """
    return {
        variable.attr
        for variable in get_instance_variables(method)
    }


def get_all_class_variables(cls):
    """
    Return class and instance variables associated with a given class
    """
    return get_class_variables(cls) + get_instance_variables(cls)


def get_all_class_variable_names(cls):
    """
    Return the names of all class and instance variables associated with a
    given class
    """
    def name_getter(variable):
        assert isinstance(variable, (ast.Name, ast.Attribute)), "Unknown variable type"
        if isinstance(variable, ast.Name):
            return variable.id
        elif isinstance(variable, ast.Attribute):
            return variable.attr

    return {
        name_getter(variable)
        for variable in get_all_class_variables(cls)
    }


def get_module_classes(node):
    """
    Return classes associated with a given module
    """
    return [
        child
        for child in ast.walk(node)
        if isinstance(child, ast.ClassDef)
    ]


def get_ast_node_from_string(string):
    """
    Return an AST node from a string
    """
    return ast.parse(string)
