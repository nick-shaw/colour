#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CAM02-LCD, CAM02-SCD, and CAM02-UCS Colourspaces
================================================

Defines the *CAM02-LCD*, *CAM02-SCD*, and *CAM02-UCS* colourspaces
transformations:

-   :func:``
-   :func:``
-   :func:``
-   :func:``

See Also
--------
`CAM02-LCD, CAM02-SCD, and CAM02-UCS Colourspaces Jupyter Notebook
<http://nbviewer.jupyter.org/github/colour-science/colour-notebooks/\
blob/master/notebooks/models/cam02_ucs.ipynb>`_

References
----------
.. [1]  Luo, R. M., Cui, G., & Li, C. (2006). Uniform Colour Spaces Based on
        CIECAM02 Colour Appearance Model. Color Research and Application,
        31(4), 320–330. doi:10.1002/col.20227
"""

from __future__ import division, unicode_literals

import numpy as np
from collections import namedtuple

from colour.utilities import CaseInsensitiveMapping, tsplit, tstack

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013-2016 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = []


class UCS_Coefficients_Luo2006(
    namedtuple('UCS_Coefficients_Luo2006',
               ('K_L', 'c_1', 'c_2'))):
    """
    """


UCS_LUO2006 = CaseInsensitiveMapping(
    {'CAM02-LCD': UCS_Coefficients_Luo2006(0.77, 0.007, 0.0053),
     'CAM02-SCD': UCS_Coefficients_Luo2006(1.24, 0.007, 0.0363),
     'CAM02-UCS': UCS_Coefficients_Luo2006(1.00, 0.007, 0.0228)})


def JMh_CIECAM02_to_UCS_Luo2006(
    JMh,
    colourspace=UCS_LUO2006.get('CAM02-UCS')):
    """
    """

    J, M, h = tsplit(JMh)
    K_L, c_1, c_2 = colourspace

    J_p = ((1 + 100 * c_1) * J) / (1 + c_1 * J)
    M_p = (1 / c_2) * np.log(1 + c_2 * M)

    h = np.radians(h)
    a_p = M_p * np.cos(h)
    b_p = M_p * np.sin(h)

    return tstack((J_p, M_p, a_p, b_p))


def UCS_Luo2006_to_JMh_CIECAM02(
    JpMpapbp,
    colourspace=UCS_LUO2006.get('CAM02-UCS')):
    """
    """

    J_p, M_p, a_p, b_p = tsplit(JpMpapbp)
    K_L, c_1, c_2 = colourspace

    J = -J_p / (c_1 * J_p - 1 - 100 * c_1)

    M = (np.exp(M_p / (1 / c_2)) - 1) / c_2

    h = 360 - np.degrees(np.arccos(a_p / M_p)) % 360

    return tstack((J, M, h))


import colour

XYZ = np.array([19.01, 20.00, 21.78])
XYZ_w = np.array([95.05, 100.00, 108.88])
L_A = 318.31
Y_b = 20.0
surround = colour.CIECAM02_VIEWING_CONDITIONS['Average']
s = np.asarray(colour.XYZ_to_CIECAM02(
    XYZ, XYZ_w, L_A, Y_b, surround), np.float_)
JMh = tsplit((s[..., 0], s[..., 5], s[..., 2]))
print(JMh)
JpMpapbp = JMh_CIECAM02_to_UCS_Luo2006(JMh)
print('JpMpapbp', JpMpapbp)
print('JMh', UCS_Luo2006_to_JMh_CIECAM02(JpMpapbp))
