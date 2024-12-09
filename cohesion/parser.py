#!/usr/bin/env python

import ast

BOUND_METHOD_ARGUMENT_NAME = "self"


def get_object_name(obj):
    """
    Return the name of a given object
    """
    name_dispatch = {
        ast.Name: "id",
        ast.Attribute: "attr",
        ast.Call: "func",
        ast.FunctionDef: "name",
        ast.ClassDef: "name",
        ast.Subscript: "value",
    }

    # This is a new ast type in Python 3
    if hasattr(ast, "arg"):
        name_dispatch[ast.arg] = "arg"

    while not isinstance(obj, str):
        assert type(obj) in name_dispatch
        obj = getattr(obj, name_dispatch[type(obj)])

    return obj


def get_attribute_name_id(attr):
    """
    Return the attribute name identifier
    """
    return attr.value.id if isinstance(attr.value, ast.Name) else None


def is_class_method_bound(method, arg_name=BOUND_METHOD_ARGUMENT_NAME):
    """
    Return whether a class method is bound to the class
    """
    if not method.args.args:
        return False

    first_arg = method.args.args[0]

    first_arg_name = get_object_name(first_arg)

    return first_arg_name == arg_name


def class_method_has_decorator(method, decorator):
    """
    Return whether a class method has a specific decorator
    """
    return decorator in [get_object_name(d) for d in method.decorator_list]


def is_class_method_classmethod(method):
    """
    Return whether a class method is a classmethod
    """
    return class_method_has_decorator(method, "classmethod")


def is_class_method_staticmethod(method):
    """
    Return whether a class method is a staticmethod
    """
    return class_method_has_decorator(method, "staticmethod")


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


def get_instance_variables(node, bound_name_classifier=BOUND_METHOD_ARGUMENT_NAME):
    """
    Return instance variables used in an AST node
    """
    node_attributes = [
        child
        for child in ast.walk(node)
        if isinstance(child, ast.Attribute) and
        get_attribute_name_id(child) == bound_name_classifier
    ]
    node_function_call_names = [
        get_object_name(child)
        for child in ast.walk(node)
        if isinstance(child, ast.Call)
    ]
    node_instance_variables = [
        attribute
        for attribute in node_attributes
        if get_object_name(attribute) not in node_function_call_names
    ]
    return node_instance_variables


def get_all_class_variable_names_used_in_method(method):
    """
    Return the names of all instance variables associated with a
    given method
    """
    return {
        get_object_name(variable)
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
    return {
        get_object_name(variable)
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
