# -*- coding: utf-8 -*-

"""A collection of functionality for the tools in bin/."""


def format_version(version):
    """Format a version number used by bibpy's accompanying tools."""
    return '%(prog)s v{0}'.format(version)


def always_true(value):
    """A function that always returns True."""
    return True


def always_false(value):
    """A function that always returns False."""
    return False


def compose_predicates(predicates, pred_combiner):
    """Return a function that composes all the given predicates."""
    def composed_predicates(value):
        return pred_combiner(pred(value) for pred in predicates)

    return composed_predicates
