"""
Define the unit tests for the :mod:`colour.quality.CIE2017` module.

Notes
-----
-   Reference data was created using the official Excel spreadsheet, published
    by the CIE at this URL: http://files.cie.co.at/933_TC1-90.zip.
"""

from __future__ import annotations

import numpy as np
import pytest

from colour.colorimetry import (
    SDS_ILLUMINANTS,
    SpectralDistribution,
    SpectralShape,
    reshape_sd,
    sd_blackbody,
)
from colour.quality.cfi2017 import (
    CCT_reference_illuminant,
    colour_fidelity_index_CIE2017,
    sd_reference_illuminant,
)
from colour.utilities import ColourUsageWarning

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "DATA_SD_SAMPLE_5NM",
    "SD_SAMPLE_5NM",
    "DATA_SD_SAMPLE_1NM",
    "SD_SAMPLE_1NM",
    "TestColourFidelityIndexCIE2017",
    "TestCctReferenceIlluminant",
    "TestSdReferenceIlluminant",
]

DATA_SD_SAMPLE_5NM: dict = {
    380: 0.000,
    385: 0.000,
    390: 0.001,
    395: 0.001,
    400: 0.002,
    405: 0.005,
    410: 0.010,
    415: 0.021,
    420: 0.042,
    425: 0.080,
    430: 0.140,
    435: 0.225,
    440: 0.337,
    445: 0.479,
    450: 0.604,
    455: 0.633,
    460: 0.551,
    465: 0.436,
    470: 0.346,
    475: 0.282,
    480: 0.237,
    485: 0.213,
    490: 0.210,
    495: 0.226,
    500: 0.260,
    505: 0.311,
    510: 0.372,
    515: 0.436,
    520: 0.499,
    525: 0.559,
    530: 0.612,
    535: 0.658,
    540: 0.698,
    545: 0.735,
    550: 0.771,
    555: 0.804,
    560: 0.836,
    565: 0.868,
    570: 0.898,
    575: 0.926,
    580: 0.952,
    585: 0.974,
    590: 0.989,
    595: 0.998,
    600: 1.000,
    605: 0.992,
    610: 0.978,
    615: 0.957,
    620: 0.927,
    625: 0.888,
    630: 0.844,
    635: 0.799,
    640: 0.750,
    645: 0.698,
    650: 0.644,
    655: 0.591,
    660: 0.539,
    665: 0.488,
    670: 0.440,
    675: 0.395,
    680: 0.354,
    685: 0.316,
    690: 0.281,
    695: 0.249,
    700: 0.220,
    705: 0.194,
    710: 0.171,
    715: 0.150,
    720: 0.131,
    725: 0.115,
    730: 0.100,
    735: 0.088,
    740: 0.077,
    745: 0.067,
    750: 0.059,
    755: 0.052,
    760: 0.046,
    765: 0.040,
    770: 0.035,
    775: 0.031,
    780: 0.027,
}

SD_SAMPLE_5NM: SpectralDistribution = SpectralDistribution(DATA_SD_SAMPLE_5NM)

DATA_SD_SAMPLE_1NM: dict = {
    380: 0.000,
    381: 0.000,
    382: 0.000,
    383: 0.000,
    384: 0.000,
    385: 0.000,
    386: 0.000,
    387: 0.000,
    388: 0.000,
    389: 0.001,
    390: 0.001,
    391: 0.001,
    392: 0.001,
    393: 0.001,
    394: 0.001,
    395: 0.001,
    396: 0.001,
    397: 0.002,
    398: 0.002,
    399: 0.002,
    400: 0.002,
    401: 0.003,
    402: 0.003,
    403: 0.004,
    404: 0.004,
    405: 0.005,
    406: 0.006,
    407: 0.007,
    408: 0.008,
    409: 0.009,
    410: 0.010,
    411: 0.012,
    412: 0.014,
    413: 0.016,
    414: 0.018,
    415: 0.021,
    416: 0.024,
    417: 0.028,
    418: 0.032,
    419: 0.037,
    420: 0.042,
    421: 0.048,
    422: 0.055,
    423: 0.063,
    424: 0.071,
    425: 0.080,
    426: 0.091,
    427: 0.102,
    428: 0.114,
    429: 0.127,
    430: 0.140,
    431: 0.155,
    432: 0.171,
    433: 0.188,
    434: 0.206,
    435: 0.225,
    436: 0.245,
    437: 0.266,
    438: 0.289,
    439: 0.312,
    440: 0.337,
    441: 0.364,
    442: 0.391,
    443: 0.420,
    444: 0.449,
    445: 0.479,
    446: 0.508,
    447: 0.535,
    448: 0.561,
    449: 0.585,
    450: 0.604,
    451: 0.620,
    452: 0.631,
    453: 0.636,
    454: 0.637,
    455: 0.633,
    456: 0.623,
    457: 0.610,
    458: 0.593,
    459: 0.573,
    460: 0.551,
    461: 0.528,
    462: 0.504,
    463: 0.481,
    464: 0.458,
    465: 0.436,
    466: 0.415,
    467: 0.396,
    468: 0.378,
    469: 0.361,
    470: 0.346,
    471: 0.331,
    472: 0.318,
    473: 0.305,
    474: 0.293,
    475: 0.282,
    476: 0.271,
    477: 0.261,
    478: 0.252,
    479: 0.244,
    480: 0.237,
    481: 0.230,
    482: 0.225,
    483: 0.220,
    484: 0.216,
    485: 0.213,
    486: 0.211,
    487: 0.209,
    488: 0.209,
    489: 0.209,
    490: 0.210,
    491: 0.212,
    492: 0.214,
    493: 0.217,
    494: 0.221,
    495: 0.226,
    496: 0.231,
    497: 0.237,
    498: 0.244,
    499: 0.252,
    500: 0.260,
    501: 0.269,
    502: 0.279,
    503: 0.289,
    504: 0.300,
    505: 0.311,
    506: 0.322,
    507: 0.334,
    508: 0.347,
    509: 0.359,
    510: 0.372,
    511: 0.384,
    512: 0.397,
    513: 0.410,
    514: 0.423,
    515: 0.436,
    516: 0.449,
    517: 0.462,
    518: 0.474,
    519: 0.487,
    520: 0.499,
    521: 0.512,
    522: 0.524,
    523: 0.536,
    524: 0.548,
    525: 0.559,
    526: 0.570,
    527: 0.581,
    528: 0.592,
    529: 0.602,
    530: 0.612,
    531: 0.622,
    532: 0.632,
    533: 0.641,
    534: 0.650,
    535: 0.658,
    536: 0.667,
    537: 0.675,
    538: 0.683,
    539: 0.691,
    540: 0.698,
    541: 0.706,
    542: 0.714,
    543: 0.721,
    544: 0.728,
    545: 0.735,
    546: 0.743,
    547: 0.750,
    548: 0.757,
    549: 0.764,
    550: 0.771,
    551: 0.777,
    552: 0.784,
    553: 0.791,
    554: 0.798,
    555: 0.804,
    556: 0.811,
    557: 0.817,
    558: 0.824,
    559: 0.830,
    560: 0.836,
    561: 0.843,
    562: 0.849,
    563: 0.855,
    564: 0.861,
    565: 0.868,
    566: 0.874,
    567: 0.880,
    568: 0.886,
    569: 0.892,
    570: 0.898,
    571: 0.904,
    572: 0.909,
    573: 0.915,
    574: 0.921,
    575: 0.926,
    576: 0.931,
    577: 0.937,
    578: 0.942,
    579: 0.947,
    580: 0.952,
    581: 0.956,
    582: 0.961,
    583: 0.965,
    584: 0.970,
    585: 0.974,
    586: 0.977,
    587: 0.981,
    588: 0.984,
    589: 0.986,
    590: 0.989,
    591: 0.991,
    592: 0.993,
    593: 0.995,
    594: 0.996,
    595: 0.998,
    596: 0.999,
    597: 1.000,
    598: 1.000,
    599: 1.000,
    600: 1.000,
    601: 0.999,
    602: 0.998,
    603: 0.996,
    604: 0.995,
    605: 0.992,
    606: 0.990,
    607: 0.988,
    608: 0.985,
    609: 0.981,
    610: 0.978,
    611: 0.974,
    612: 0.970,
    613: 0.966,
    614: 0.962,
    615: 0.957,
    616: 0.952,
    617: 0.946,
    618: 0.940,
    619: 0.934,
    620: 0.927,
    621: 0.920,
    622: 0.912,
    623: 0.904,
    624: 0.896,
    625: 0.888,
    626: 0.880,
    627: 0.871,
    628: 0.862,
    629: 0.853,
    630: 0.844,
    631: 0.835,
    632: 0.826,
    633: 0.817,
    634: 0.808,
    635: 0.799,
    636: 0.789,
    637: 0.780,
    638: 0.770,
    639: 0.760,
    640: 0.750,
    641: 0.740,
    642: 0.730,
    643: 0.719,
    644: 0.709,
    645: 0.698,
    646: 0.687,
    647: 0.677,
    648: 0.666,
    649: 0.655,
    650: 0.644,
    651: 0.634,
    652: 0.623,
    653: 0.612,
    654: 0.602,
    655: 0.591,
    656: 0.581,
    657: 0.570,
    658: 0.560,
    659: 0.549,
    660: 0.539,
    661: 0.529,
    662: 0.518,
    663: 0.508,
    664: 0.498,
    665: 0.488,
    666: 0.478,
    667: 0.468,
    668: 0.459,
    669: 0.449,
    670: 0.440,
    671: 0.430,
    672: 0.421,
    673: 0.412,
    674: 0.403,
    675: 0.395,
    676: 0.386,
    677: 0.378,
    678: 0.370,
    679: 0.361,
    680: 0.354,
    681: 0.346,
    682: 0.338,
    683: 0.331,
    684: 0.323,
    685: 0.316,
    686: 0.309,
    687: 0.302,
    688: 0.295,
    689: 0.288,
    690: 0.281,
    691: 0.275,
    692: 0.268,
    693: 0.262,
    694: 0.255,
    695: 0.249,
    696: 0.243,
    697: 0.237,
    698: 0.231,
    699: 0.225,
    700: 0.220,
    701: 0.214,
    702: 0.209,
    703: 0.204,
    704: 0.199,
    705: 0.194,
    706: 0.189,
    707: 0.184,
    708: 0.180,
    709: 0.175,
    710: 0.171,
    711: 0.166,
    712: 0.162,
    713: 0.158,
    714: 0.154,
    715: 0.150,
    716: 0.146,
    717: 0.142,
    718: 0.138,
    719: 0.135,
    720: 0.131,
    721: 0.128,
    722: 0.124,
    723: 0.121,
    724: 0.118,
    725: 0.115,
    726: 0.111,
    727: 0.108,
    728: 0.106,
    729: 0.103,
    730: 0.100,
    731: 0.098,
    732: 0.095,
    733: 0.092,
    734: 0.090,
    735: 0.088,
    736: 0.085,
    737: 0.083,
    738: 0.081,
    739: 0.079,
    740: 0.077,
    741: 0.075,
    742: 0.073,
    743: 0.071,
    744: 0.069,
    745: 0.067,
    746: 0.066,
    747: 0.064,
    748: 0.062,
    749: 0.061,
    750: 0.059,
    751: 0.058,
    752: 0.056,
    753: 0.055,
    754: 0.053,
    755: 0.052,
    756: 0.051,
    757: 0.049,
    758: 0.048,
    759: 0.047,
    760: 0.046,
    761: 0.045,
    762: 0.043,
    763: 0.042,
    764: 0.041,
    765: 0.040,
    766: 0.039,
    767: 0.038,
    768: 0.037,
    769: 0.036,
    770: 0.035,
    771: 0.034,
    772: 0.033,
    773: 0.032,
    774: 0.031,
    775: 0.031,
    776: 0.030,
    777: 0.029,
    778: 0.028,
    779: 0.028,
    780: 0.027,
}

SD_SAMPLE_1NM: SpectralDistribution = SpectralDistribution(DATA_SD_SAMPLE_1NM)


class TestColourFidelityIndexCIE2017:
    """
    Define :func:`colour.quality.CIE2017.colour_fidelity_index_CIE2017`
    definition unit tests methods.
    """

    def test_colour_fidelity_index_CIE2017(self):
        """
        Test :func:`colour.quality.CIE2017.colour_fidelity_index_CIE2017`
        definition.
        """

        for sd in [SD_SAMPLE_5NM, SD_SAMPLE_1NM]:
            specification = colour_fidelity_index_CIE2017(sd, additional_data=True)
            np.testing.assert_allclose(specification.R_f, 81.6, atol=0.1)
            np.testing.assert_allclose(
                specification.R_s,
                [
                    89.5,
                    80.5,
                    81.5,
                    79.4,
                    65.9,
                    79.4,
                    73.2,
                    68.5,
                    95.9,
                    76.3,
                    71.9,
                    71.8,
                    83.3,
                    93.0,
                    89.2,
                    72.9,
                    75.1,
                    85.8,
                    75.1,
                    63.4,
                    69.4,
                    71.4,
                    89.7,
                    76.8,
                    67.6,
                    75.5,
                    92.7,
                    87.7,
                    81.1,
                    95.0,
                    83.3,
                    74.4,
                    90.4,
                    80.4,
                    89.0,
                    86.9,
                    85.0,
                    95.7,
                    98.5,
                    96.3,
                    98.7,
                    88.4,
                    85.2,
                    99.6,
                    90.4,
                    88.6,
                    94.3,
                    85.3,
                    86.4,
                    90.0,
                    89.3,
                    88.0,
                    83.6,
                    89.6,
                    86.7,
                    81.4,
                    80.2,
                    80.6,
                    88.5,
                    89.7,
                    84.2,
                    84.2,
                    79.4,
                    71.3,
                    72.8,
                    65.8,
                    64.1,
                    71.7,
                    77.4,
                    68.0,
                    63.2,
                    87.1,
                    62.4,
                    92.7,
                    67.3,
                    67.6,
                    80.0,
                    70.4,
                    89.0,
                    87.0,
                    81.5,
                    94.2,
                    94.3,
                    89.4,
                    79.3,
                    76.6,
                    83.7,
                    87.7,
                    76.7,
                    88.6,
                    76.2,
                    68.5,
                    80.1,
                    65.3,
                    74.9,
                    83.9,
                    88.6,
                    84.2,
                    77.4,
                ],
                atol=0.1,
            )

        specification = colour_fidelity_index_CIE2017(
            SDS_ILLUMINANTS["FL1"], additional_data=True
        )
        np.testing.assert_allclose(specification.R_f, 80.6, atol=0.1)
        np.testing.assert_allclose(
            specification.R_s,
            [
                85.1,
                68.9,
                73.9,
                79.7,
                51.6,
                77.8,
                52.1,
                47.8,
                95.3,
                68.9,
                67.3,
                63.6,
                71.3,
                91.1,
                79.0,
                63.2,
                72.8,
                78.4,
                75.2,
                60.4,
                68.0,
                67.3,
                88.6,
                78.4,
                68.7,
                75.7,
                91.0,
                91.5,
                78.3,
                83.0,
                82.3,
                78.7,
                85.8,
                85.6,
                92.3,
                94.6,
                88.3,
                87.8,
                97.4,
                94.4,
                95.4,
                93.3,
                90.5,
                99.5,
                88.9,
                87.6,
                94.3,
                77.7,
                88.0,
                89.6,
                91.0,
                87.3,
                81.3,
                83.8,
                85.2,
                78.1,
                78.2,
                79.5,
                86.9,
                94.4,
                87.4,
                93.7,
                88.6,
                77.9,
                74.5,
                78.2,
                77.2,
                79.7,
                86.3,
                76.3,
                81.6,
                91.0,
                73.3,
                98.1,
                81.9,
                77.4,
                86.9,
                79.4,
                90.2,
                91.1,
                80.6,
                96.6,
                95.1,
                89.3,
                84.2,
                72.5,
                78.6,
                75.5,
                74.4,
                75.3,
                91.4,
                58.2,
                74.6,
                52.6,
                67.0,
                76.2,
                88.9,
                75.2,
                55.5,
            ],
            atol=0.1,
        )

        specification = colour_fidelity_index_CIE2017(
            SDS_ILLUMINANTS["FL2"], additional_data=True
        )
        np.testing.assert_allclose(specification.R_f, 70.1, atol=0.1)
        np.testing.assert_allclose(
            specification.R_s,
            [
                78.9,
                59.0,
                66.9,
                65.7,
                35.8,
                66.1,
                40.4,
                34.7,
                95.1,
                53.5,
                47.4,
                44.6,
                64.1,
                86.6,
                71.6,
                48.8,
                56.1,
                68.9,
                56.8,
                43.9,
                46.9,
                46.5,
                80.0,
                62.6,
                48.1,
                58.4,
                82.0,
                84.6,
                61.5,
                69.6,
                67.5,
                62.3,
                73.9,
                73.6,
                85.9,
                87.5,
                79.4,
                76.0,
                96.6,
                92.8,
                90.5,
                89.1,
                83.0,
                99.4,
                83.1,
                80.7,
                86.8,
                66.1,
                79.6,
                80.7,
                81.3,
                76.1,
                68.7,
                76.8,
                77.0,
                66.1,
                65.5,
                67.4,
                78.8,
                90.1,
                77.5,
                86.9,
                76.8,
                59.7,
                61.2,
                57.9,
                56.2,
                62.0,
                72.9,
                57.7,
                63.7,
                84.0,
                52.7,
                96.2,
                66.6,
                56.6,
                76.2,
                63.3,
                81.8,
                84.5,
                73.5,
                93.9,
                90.9,
                85.7,
                80.5,
                63.5,
                73.7,
                69.0,
                66.1,
                67.5,
                92.6,
                51.3,
                69.5,
                40.7,
                61.5,
                70.2,
                80.0,
                67.0,
                45.0,
            ],
            atol=0.1,
        )

    def test_raise_exception_colour_fidelity_index_CFI2017(self):
        """
        Test :func:`colour.quality.CIE2017.colour_fidelity_index_CFI2017`
        definition raised exception.
        """

        sd = reshape_sd(SDS_ILLUMINANTS["FL2"], SpectralShape(400, 700, 5))
        pytest.warns(ColourUsageWarning, colour_fidelity_index_CIE2017, sd)

        sd = reshape_sd(SDS_ILLUMINANTS["FL2"], SpectralShape(380, 780, 10))
        pytest.raises(ValueError, colour_fidelity_index_CIE2017, sd)


class TestCctReferenceIlluminant:
    """
    Define :func:`colour.quality.CIE2017.CCT_reference_illuminant`
    definition unit tests methods.
    """

    def test_CCT_reference_illuminant(self):
        """
        Test :func:`colour.quality.CIE2017.CCT_reference_illuminant`
        definition.
        """

        for sd in [SD_SAMPLE_5NM, SD_SAMPLE_1NM]:
            CCT, D_uv = CCT_reference_illuminant(sd)
            np.testing.assert_allclose(CCT, 3287.5, atol=0.5)
            np.testing.assert_allclose(D_uv, -0.000300000000000, atol=0.0005)


class TestSdReferenceIlluminant:
    """
    Define :func:`colour.quality.CIE2017.sd_reference_illuminant`
    definition unit tests methods.
    """

    def test_sd_reference_illuminant(self):
        """
        Test :func:`colour.quality.CIE2017.sd_reference_illuminant`
        definition.
        """

        for sd, shape in [
            (SD_SAMPLE_5NM, SD_SAMPLE_5NM.shape),
            (SD_SAMPLE_1NM, SD_SAMPLE_1NM.shape),
        ]:
            CCT, _D_uv = CCT_reference_illuminant(sd)
            sd_reference = sd_reference_illuminant(CCT, shape)

            np.testing.assert_allclose(
                sd_reference.values,
                sd_blackbody(3288, shape).values,
                atol=1.75,
            )
