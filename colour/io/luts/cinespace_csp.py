# -*- coding: utf-8 -*-
"""
Cinespace .csp LUT Format Input / Output Utilities
==================================================

Defines *Cinespace* *.csp* *LUT* Format related input / output utilities
objects.

-   :func:`colour.io.write_LUT_Cinespace`

References
----------
-   :cite: https://sourceforge.net/p/cinespacelutlib/code/HEAD/tree/trunk/
"""

from __future__ import division, unicode_literals

from colour.io.luts import LUT1D, LUT2D, LUT3D, LUTSequence
from colour.utilities import tsplit
import numpy as np

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013-2018 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['write_LUT_Cinespace']


def write_LUT_Cinespace(LUT, path, decimals=7):
    """
    Writes given *LUT* to given  *Cinespace* *.csp* *LUT* file.

    Parameters
    ----------
    LUT : LUT1D or LUT2D or LUT3D or LUTSequence
        :class:`LUT1D`, :class:`LUT2D` or :class:`LUT3D` or
        :class:`LUTSequence` class instance to write at given path.
    path : unicode
        *LUT* path.
    decimals : int, optional
        Formatting decimals.

    Returns
    -------
    bool
        Definition success.

    Examples
    --------
    Writing a 2D *Cinespace* *.csp* *LUT*:

    >>> from colour.algebra import spow
    >>> domain = np.array([[-0.1, -0.2, -0.4], [1.5, 3.0, 6.0]])
    >>> LUT = LUT2D(
    ...     spow(LUT2D.linear_table(16, domain), 1 / 2.2),
    ...     'My LUT',
    ...     domain,
    ...     comments=['A first comment.', 'A second comment.'])
    >>> write_LUT_Cinespace(LUT, 'My_LUT.cube')  # doctest: +SKIP

    Writing a 3D *Cinespace* *.csp* *LUT*:

    >>> domain = np.array([[-0.1, -0.2, -0.4], [1.5, 3.0, 6.0]])
    >>> LUT = LUT3D(
    ...     spow(LUT3D.linear_table(16, domain), 1 / 2.2),
    ...     'My LUT',
    ...     domain,
    ...     comments=['A first comment.', 'A second comment.'])
    >>> write_LUT_Cinespace(LUT, 'My_LUT.cube')  # doctest: +SKIP
    """

    has_3D, has_2D, non_uniform = False, False, False

    if isinstance(LUT, LUTSequence):
        assert (len(LUT) == 2 and
                (isinstance(LUT[0], LUT1D) or isinstance(LUT[0], LUT2D)) and
                isinstance(LUT[1], LUT3D)), \
                'LUTSequence must be 1D+3D or 2D+3D!'
        has_2D = True
        has_3D = True
        name = LUT[1].name
        if isinstance(LUT[0], LUT1D):
            LUT[0] = LUT[0].as_LUT(LUT2D)

    elif isinstance(LUT, LUT1D):
        if LUT.is_domain_explicit():
            non_uniform = True
        name = LUT.name
        LUT = LUTSequence(LUT.as_LUT(LUT2D), LUT3D())
        has_2D = True

    elif isinstance(LUT, LUT2D):
        if LUT.is_domain_explicit():
            non_uniform = True
        name = LUT.name
        LUT = LUTSequence(LUT, LUT3D())
        has_2D = True

    elif isinstance(LUT, LUT3D):
        name = LUT.name
        LUT = LUTSequence(LUT2D(), LUT)
        has_3D = True

    else:
        assert False, 'LUT must be 1D, 2D, 3D, 1D+3D or 2D+3D!'

    if has_2D:
        assert 2 <= LUT[0].size <= 65536, \
            'Shaper size must be in domain [2, 65536]!'
    if has_3D:
        assert 2 <= LUT[1].size <= 256, 'Cube size must be in domain [2, 256]!'

    def _ragged_size(table):
        r, g, b = tsplit(table)
        r_len = r.shape[-1] - np.sum(np.isnan(r))
        g_len = g.shape[-1] - np.sum(np.isnan(g))
        b_len = b.shape[-1] - np.sum(np.isnan(b))
        return [r_len, g_len, b_len]

    def _format_array(array):
        """
        Formats given array as a *Cinespace* *.cube* data row.
        """

        return '{1:0.{0}f} {2:0.{0}f} {3:0.{0}f}'.format(decimals, *array)

    def _format_tuple(array):
        """
        Formats given array as 2 space separated values to *decimals* precison.
        """

        return '{1:0.{0}f} {2:0.{0}f}'.format(decimals, *array)

    with open(path, 'w') as csp_file:
        csp_file.write('CSPLUTV100\n')

        if has_3D:
            csp_file.write('3D\n\n')
        else:
            csp_file.write('1D\n\n')

        csp_file.write('BEGIN METADATA\n')
        csp_file.write('{0}\n'.format(name))

        if LUT[0].comments:
            for comment in LUT[0].comments:
                csp_file.write('{0}\n'.format(comment))

        if LUT[1].comments:
            for comment in LUT[1].comments:
                csp_file.write('{0}\n'.format(comment))

        csp_file.write('END METADATA\n\n')

        if has_3D or non_uniform:
            if has_2D:
                for i in range(3):
                    if LUT[0].is_domain_explicit():
                        size = _ragged_size(LUT[0].domain)[i]
                        table_min = np.nanmin(LUT[0].table)
                        table_max = np.nanmax(LUT[0].table)
                    else:
                        size = LUT[0].size
                    csp_file.write('{0}\n'.format(size))
                    for j in range(size):
                        if LUT[0].is_domain_explicit():
                            entry = LUT[0].domain[j][i]
                        else:
                            entry = (LUT[0].domain[0][i] + j *
                                     (LUT[0].domain[1][i] -
                                     LUT[0].domain[0][i]) /
                                     (LUT[0].size - 1))
                        csp_file.write('{0:.{1}f} '.format(entry, decimals))
                    csp_file.write('\n')
                    for j in range(size):
                        entry = LUT[0].table[j][i]
                        if non_uniform:
                            entry -= table_min
                            entry /= (table_max - table_min)
                        csp_file.write('{0:.{1}f} '.format(entry, decimals))
                    csp_file.write('\n')
            else:
                for i in range(3):
                    csp_file.write('2\n')
                    csp_file.write('{0}\n'.format(
                                   _format_tuple([LUT[1].domain[0][i],
                                                 LUT[1].domain[1][i]])))
                    csp_file.write('0.0 1.0\n')
            if non_uniform:
                csp_file.write('\n{0}\n'.format(2))
                row = [table_min, table_min, table_min]
                csp_file.write('{0}\n'.format(_format_array(row)))
                row = [table_max, table_max, table_max]
                csp_file.write('{0}\n'.format(_format_array(row)))
            else:
                csp_file.write('\n{0} {1} {2}\n'.format(LUT[1].size,
                                                        LUT[1].size,
                                                        LUT[1].size))
                table = LUT[1].table.reshape((-1, 3), order='F')
                for row in table:
                    csp_file.write('{0}\n'.format(_format_array(row)))

        else:
            for i in range(3):
                csp_file.write('2\n')
                csp_file.write('{0}\n'.format(
                               _format_tuple([LUT[0].domain[0][i],
                                             LUT[0].domain[1][i]])))
                csp_file.write('0.0 1.0\n')
            csp_file.write('\n{0} {1} {2}\n'.format(LUT[0].size,
                                                    LUT[0].size,
                                                    LUT[0].size))
            table = LUT[0].table
            for row in table:
                csp_file.write('{0}\n'.format(_format_array(row)))

    return True
