#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Defines unit tests for :mod:`colour.metadata.common` module.
"""

from __future__ import division, unicode_literals

import unittest

import colour
from colour.metadata.common import (
    parse_parameters_field_metadata,
    parse_returns_field_metadata,
    parse_notes_field_metadata,
    set_metadata,
    filter_metadata_registry)
from colour.metadata.common import MethodMetadata, TypeMetadata

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013-2016 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['TestParseParametersFieldMetadata',
           'TestParseReturnsFieldMetadata',
           'TestParseNotesFieldMetadata',
           'TestSetMetadata',
           'TestFilterMetadataRegistry']


class TestParseParametersFieldMetadata(unittest.TestCase):
    """
    Defines :func:`colour.metadata.common.parse_parameters_field_metadata`
    definition units tests methods.
    """

    def test_parse_parameters_field_metadata(self):
        """
        Tests :func:`colour.metadata.common.parse_parameters_field_metadata`
        definition.
        """

        field = (['Y', 'numeric or array_like, Luminance, Y, 100'],
                 '*luminance* :math:`Y`.')
        self.assertTupleEqual(
            tuple(parse_parameters_field_metadata(field)),
            ('Luminance', 'Y', '100'))

        field = (['Y', 'numeric or array_like'],
                 '*luminance* :math:`Y`.')
        self.assertIsNone(parse_parameters_field_metadata(field))


class TestParseReturnsFieldMetadata(unittest.TestCase):
    """
    Defines :func:`colour.metadata.common.parse_returns_field_metadata`
    definition units tests methods.
    """

    def test_parse_returns_field_metadata(self):
        """
        Tests :func:`colour.metadata.common.parse_returns_field_metadata`
        definition.
        """

        field = (['numeric or array_like, Lightness, W, 100'],
                 '*Lightness* :math:`W`.')
        self.assertTupleEqual(
            tuple(parse_returns_field_metadata(field)),
            ('Lightness', 'W', '100'))

        field = (['numeric or array_like'],
                 '*Lightness* :math:`W`.')
        self.assertIsNone(parse_returns_field_metadata(field))


class TestParseNotesFieldMetadata(unittest.TestCase):
    """
    Defines :func:`colour.metadata.common.parse_notes_field_metadata`
    definition units tests methods.
    """

    def test_parse_notes_field_metadata(self):
        """
        Tests :func:`colour.metadata.common.parse_notes_field_metadata`
        definition.
        """

        field = (['method', 'Wyszecki 1963, Wyszecki (1963)'], '')
        self.assertTupleEqual(
            tuple(parse_notes_field_metadata(field)),
            ('Wyszecki 1963', 'Wyszecki (1963)'))

        field = (['method', 'Wyszecki 1963'], '')
        self.assertIsNone(parse_notes_field_metadata(field))


class TestSetMetadata(unittest.TestCase):
    """
    Defines :func:`colour.metadata.common.set_metadata` definition units
    tests methods.
    """

    def test_set_metadata(self):
        """
        Tests :func:`colour.metadata.common.set_metadata` definition.
        """

        def fn_a(argument_1):
            """
            Summary of docstring.

            Description of docstring.

            Parameters
            ----------
            argument_1 : object, Type, Symbol, Scale
                Description of `argument_1`.

            Returns
            -------
            object, Type, Symbol, Scale
                Description of `object`.

            Notes
            -----
            method : Method Name, Method Strict Name
            """

            return argument_1

        set_metadata(fn_a)

        self.assertTrue(hasattr(fn_a, '__metadata__'))
        self.assertDictEqual(
            dict(fn_a.__metadata__),
            {'method': MethodMetadata(
                name='Method Name', strict_name='Method Strict Name'),
                'parameters': [TypeMetadata(
                    type_='Type', symbol='Symbol', scale='Scale')],
                'returns': TypeMetadata(
                    type_='Type', symbol='Symbol', scale='Scale')})


class TestFilterMetadataRegistry(unittest.TestCase):
    """
    Defines :func:`colour.metadata.common.filter_metadata_registry`
    definition units tests methods.
    """

    def test_filter_metadata_registry(self):
        """
        Tests :func:`colour.metadata.common.filter_metadata_registry`
        definition.
        """

        self.assertSetEqual(
            set(filter_metadata_registry(parameters_type='Luminance')),
            set([colour.lightness_Glasser1958,
                 colour.lightness_Wyszecki1963,
                 colour.lightness_CIE1976]))

        self.assertSetEqual(
            set(filter_metadata_registry(returns_type='Luminance')),
            set([colour.luminance_ASTMD153508,
                 colour.luminance_Newhall1943,
                 colour.luminance_CIE1976]))

        self.assertSetEqual(
            set(filter_metadata_registry(method_name='CIE 1976')),
            set([colour.luminance_CIE1976,
                 colour.lightness_CIE1976]))

        if __name__ == '__main__':
            unittest.main()
