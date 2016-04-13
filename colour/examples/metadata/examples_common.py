#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Showcases metadata related examples.
"""

from pprint import pprint

import colour
from colour.utilities.verbose import message_box

message_box('Metadata Examples')

message_box('Filtering definitions with a first *Luminance* argument.')
pprint(colour.filter_metadata_registry(parameters_type='Luminance'))

print('\n')

message_box('Filtering definitions with any *Luminance* argument.')
pprint(colour.filter_metadata_registry(parameters_any_type='Luminance'))

print('\n')

message_box('Filtering definitions returning a *Luminance* value.')
pprint(colour.filter_metadata_registry(returns_type='Luminance'))

print('\n')

message_box('Filtering definitions using *CIE 1976* method.')
pprint(colour.filter_metadata_registry(method_name='CIE 1976'))
