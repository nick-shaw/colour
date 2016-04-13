#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Common Metadata
===============

Defines the objects implementing the base metadata system support:

-   :func:`filter_metadata_registry`
"""

from __future__ import division, unicode_literals

import re
import sys
from collections import defaultdict, namedtuple

from colour.metadata.docstring import DocstringFields
from colour.utilities import Structure

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013-2016 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['METADATA_REGISTRY',
           'TypeMetadata',
           'MethodMetadata',
           'parse_parameters_field_metadata',
           'parse_returns_field_metadata',
           'parse_notes_field_metadata',
           'set_metadata',
           'install_metadata',
           'filter_metadata_registry']

if sys.version_info[0] >= 3:
    _DOCSTRING_ATTRIBUTE = '__doc__'
else:
    _DOCSTRING_ATTRIBUTE = 'func_doc'

METADATA_REGISTRY = []
"""
Registry for objects with defined metadata.

METADATA_REGISTRY : list
"""


class TypeMetadata(
    namedtuple('TypeMetadata',
               ('type', 'symbol', 'scale'))):
    """
    Defines the metadata class for types.

    Parameters
    ----------
    type : unicode
        Type name.
    symbol : unicode
        Type symbol.
    scale : unicode
        Scale hint to convert in [0, 1] range.
    """

    def __new__(cls, type_, symbol, scale=None):
        """
        Returns a new instance of the :class:`TypeMetadata` class.
        """

        return super(TypeMetadata, cls).__new__(
            cls, type_, symbol, scale)


class MethodMetadata(
    namedtuple('MethodMetadata',
               ('name', 'strict_name'))):
    """
    Defines the metadata class for methods.

    Parameters
    ----------
    name : unicode
        Method name.
    strict_name : unicode
        Method strict name.
    """

    def __new__(cls, name, strict_name=None):
        """
        Returns a new instance of the :class:`MethodMetadata` class.
        """

        return super(MethodMetadata, cls).__new__(
            cls, name, strict_name)


def parse_parameters_field_metadata(field):
    """
    Parses given *Parameters* field metadata from callable docstring.

    Parameters
    ----------
    field : unicode
        *Parameter* field metadata.

    Returns
    -------
    TypeMetadata
        Type metadata object.
    """

    summary, _description = field
    tokens = [token.strip() for token in summary[1].split(',')]
    if len(tokens) in (4, 5):
        return TypeMetadata(*tokens[-3:])


def parse_returns_field_metadata(field):
    """
    Parses given *Returns* field metadata from callable docstring.

    Parameters
    ----------
    field : unicode
        *Returns* field metadata.

    Returns
    -------
    TypeMetadata
        Type metadata object.
    """

    summary, _description = field
    tokens = [token.strip() for token in summary[0].split(',')]
    if len(tokens) == 4:
        return TypeMetadata(*tokens[-3:])


def parse_notes_field_metadata(field):
    """
    Parses given *Notes* field metadata from callable docstring.

    Parameters
    ----------
    field : unicode
        *Notes* field metadata.

    Returns
    -------
    MethodMetadata
        Method metadata object.
    """

    summary, _description = field
    if 'method' in summary:
        tokens = [token.strip() for token in summary[1].split(',')]
        if len(tokens) == 2:
            return MethodMetadata(*tokens)


def set_metadata(callable_):
    """
    Sets given callable with given metadata.

    Parameters
    ----------
    callable_ : callable, optional
        Callable to store within the metadata.

    Returns
    -------
    bool
        Definition success.

    Examples
    --------
    >>> from pprint import pprint
    >>> def fn_a(argument_1):
    ...     '''
    ...     Summary of docstring.
    ...
    ...     Description of docstring.
    ...
    ...     Parameters
    ...     ----------
    ...     argument_1 : object, Type, Symbol, Scale
    ...         Description of `argument_1`.
    ...
    ...     Returns
    ...     -------
    ...     object, Type, Symbol, Scale
    ...         Description of `object`.
    ...
    ...     Notes
    ...     -----
    ...     method : Method Name, Method Strict Name
    ...     '''
    ...
    ...     return argument_1
    >>> set_metadata(fn_a)
    True
    >>> pprint(dict(fn_a.__metadata__))  # doctest: +SKIP
    {u'method': MethodMetadata(\
name=u'Method Name', strict_name=u'Method Strict Name'),
     u'parameters': [TypeMetadata(\
type=u'Type', symbol=u'Symbol', scale=u'Scale')],
     u'returns': TypeMetadata(type=u'Type', symbol=u'Symbol', scale=u'Scale')}
    """

    if getattr(callable_, _DOCSTRING_ATTRIBUTE) is None:
        return False

    fields = DocstringFields(getattr(callable_, _DOCSTRING_ATTRIBUTE))
    metadata = defaultdict(list)
    for parameter in fields.parameters:
        field_metadata = parse_parameters_field_metadata(parameter)
        if field_metadata is not None:
            metadata['parameters'].append(field_metadata)

    if fields.returns:
        field_metadata = parse_returns_field_metadata(fields.returns[0])
        if field_metadata is not None:
            metadata['returns'] = field_metadata

    for note in fields.notes:
        field_metadata = parse_notes_field_metadata(note)
        if field_metadata is not None:
            metadata['method'] = field_metadata

    if metadata:
        global METADATA_REGISTRY

        METADATA_REGISTRY.append(callable_)

        callable_.__metadata__ = metadata

    return True


def install_metadata():
    """
    Installs the metadata in objects exposed in *Colour* base namespace.

    Returns
    -------
    bool
        Definition success.
    """

    import colour

    for object_ in colour.__dict__.values():
        if hasattr(object_, _DOCSTRING_ATTRIBUTE):
            set_metadata(object_)

    return True


def filter_metadata_registry(flags=re.IGNORECASE, **kwargs):
    """
    Filters the metadata registry :attr:`METADATA_REGISTRY` attribute and
    returns matching objects.

    Parameters
    ----------
    flags : int
        Regular expression flags.
    \**kwargs : dict, optional
        **{'parameters_type', 'parameters_symbol', 'parameters_scale',
        'parameters_any_type', 'parameters_any_symbol',
        'parameters_any_scale', 'returns_type', 'returns_symbol',
        'returns_scale', 'method_name', 'method_strict_name'}**
        Keywords arguments such as ``{'parameters_type' : unicode,
        'parameters_symbol' : unicode, 'parameters_scale' : unicode,
        'parameters_any_type' : unicode, 'parameters_any_symbol' : unicode,
        'parameters_any_scale' : unicode, 'returns_type' : unicode,
        'returns_symbol' : unicode, 'returns_scale' : unicode,
        'method_name' : unicode, 'method_strict_name' : unicode}``

    Returns
    -------
    list
        Filtered objects with defined metadata.
    """

    patterns = Structure(
        **{'parameters_type': None,
           'parameters_symbol': None,
           'parameters_scale': None,
           'parameters_any_type': None,
           'parameters_any_symbol': None,
           'parameters_any_scale': None,
           'returns_type': None,
           'returns_symbol': None,
           'returns_scale': None,
           'method_name': None,
           'method_strict_name': None})
    patterns.update(kwargs)

    filtered = []

    def apply_filters(metadata, active_patterns):

        for pattern in active_patterns:
            if patterns[pattern] is None:
                continue

            attribute = getattr(metadata, pattern.split('_')[-1])
            if re.search(patterns[pattern], attribute, flags):
                filtered.append(callable_)

    for callable_ in METADATA_REGISTRY:
        callable_metadata = callable_.__metadata__
        for i, metadata in enumerate(callable_metadata['parameters']):
            # Applying filters on first callable argument.
            if i == 0:
                apply_filters(
                    metadata,
                    [pattern for pattern in patterns
                     if 'parameters' in pattern and 'any' not in pattern])

            apply_filters(
                metadata,
                [pattern for pattern in patterns
                 if 'parameters' in pattern and 'any' in pattern])

        if callable_metadata['returns']:
            apply_filters(
                callable_metadata['returns'],
                [pattern for pattern in patterns if 'returns' in pattern])

        if callable_metadata['method']:
            apply_filters(
                callable_metadata['method'],
                [pattern for pattern in patterns if 'method' in pattern])

    return filtered
