# PyBEST: Pythonic Black-box Electronic Structure Tool
# Copyright (C) 2016-- The PyBEST Development Team
#
# This file is part of PyBEST.
#
# PyBEST is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# PyBEST is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
# --
"""Ionization Potential Equation of Motion Coupled Cluster implementations for
various fpCC reference functions.

Various IP flavors are selected from two classes:
 * RIPfpCCD:     selects a specific single IP method based on fpCCD
 * RIPfpCCSD:    selects a specific single IP method based on fpCCSD
 * RIPfpLCCD:    selects a specific single IP method based on fpLCCD
 * RIPfpLCCSD:   selects a specific single IP method based on fpLCCSD
"""

from pybest.exceptions import ArgumentError
from pybest.ip_eom.sip_rccd1 import RIPfpCCD1, RIPfpLCCD1
from pybest.ip_eom.sip_rccd1_sf import RIPfpCCD1SF, RIPfpLCCD1SF
from pybest.ip_eom.sip_rccsd1 import RIPfpCCSD1, RIPfpLCCSD1
from pybest.ip_eom.sip_rccsd1_sf import RIPfpCCSD1SF, RIPfpLCCSD1SF


class RIPfpCCD:
    """
    Restricted Single Ionization Potential Equation of Motion Coupled Cluster
    class restricted to single IP for a fpCCD reference function

    This class overwrites __new__ to create an instance of the proper IP-fpCCD
    class for a user-specified number of unpaired electrons, which are passed
    using the keyword argument alpha:
        * alpha=1: RIPfpCCD1

    The return value of __new__() is the new object instance. It has no other
    purpose.
    """

    long_name = "Ionization Potential Equation of Motion frozen pair Coupled Cluster Doubles"
    acronym = "IP-EOM-fpCCD"
    reference = "fpCCD"
    order = "IP"

    def __new__(cls, *args, **kwargs):
        """Called to create a new instance of class RIPfpCCD1 (alpha=1).
        The return value of __new__() is a new object instance.

        **Arguments**

        cls
            class of which an instance was requested.

        args, kwargs
            remaining arguments that are passed to the object constructor
            expression. They are also used in the call of __init__(self[, ...]),
            which is invoked after __new__(), where self is the new instance
            created.
        """
        alpha = kwargs.pop("alpha", -1)
        spin_free = kwargs.get("spinfree", False)

        if alpha == 1:
            if spin_free:
                return RIPfpCCD1SF(*args, **kwargs)
            return RIPfpCCD1(*args, **kwargs)
        raise ArgumentError(
            f"Unknown value of {alpha} for kwarg alpha. Supported values "
            "are 1."
        )


class RIPfpCCSD:
    """
    Restricted Single Ionization Potential Equation of Motion Coupled Cluster
    class restricted to single IP for a fpCCSD reference function

    This class overwrites __new__ to create an instance of the proper IP-fpCCSD
    class for a user-specified number of unpaired electrons, which are passed
    using the keyword argument alpha:
        * alpha=1: RIPfpCCSD1

    The return value of __new__() is the new object instance. It has no other
    purpose.
    """

    long_name = (
        "Ionization Potential Equation of Motion frozen pair Coupled Cluster "
        "Singles Doubles"
    )
    acronym = "IP-EOM-fpCCSD"
    reference = "fpCCSD"
    order = "IP"

    def __new__(cls, *args, **kwargs):
        """Called to create a new instance of class RIPfpCCSD1 (alpha=1).
        The return value of __new__() is a new object instance.

        **Arguments**

        cls
            class of which an instance was requested.

        args, kwargs
            remaining arguments that are passed to the object constructor
            expression. They are also used in the call of __init__(self[, ...]),
            which is invoked after __new__(), where self is the new instance
            created.
        """
        alpha = kwargs.pop("alpha", -1)
        spin_free = kwargs.get("spinfree", False)
        if alpha == 1:
            if spin_free:
                return RIPfpCCSD1SF(*args, **kwargs)
            return RIPfpCCSD1(*args, **kwargs)
        raise ArgumentError(
            f"Unknown value of {alpha} for kwarg alpha. Supported values "
            "are 1."
        )


class RIPfpLCCD:
    """
    Restricted Single Ionization Potential Equation of Motion Coupled Cluster
    class restricted to single IP for a fpLCCD/pCCD-LCCD reference function

    This class overwrites __new__ to create an instance of the proper IP-fpLCCD
    class for a user-specified number of unpaired electrons, which are passed
    using the keyword argument alpha:
        * alpha=1: RIPfpLCCD1

    The return value of __new__() is the new object instance. It has no other
    purpose.
    """

    long_name = (
        "Ionization Potential Equation of Motion frozen pair Linearized Coupled "
        "Cluster Doubles"
    )
    acronym = "IP-EOM-fpLCCD"
    reference = "fpLCCD"
    order = "IP"

    def __new__(cls, *args, **kwargs):
        """Called to create a new instance of class RIPfpLCCD1 (alpha=1).
        The return value of __new__() is a new object instance.

        **Arguments**

        cls
            class of which an instance was requested.

        args, kwargs
            remaining arguments that are passed to the object constructor
            expression. They are also used in the call of __init__(self[, ...]),
            which is invoked after __new__(), where self is the new instance
            created.
        """
        alpha = kwargs.pop("alpha", -1)
        spin_free = kwargs.get("spinfree", False)

        if alpha == 1:
            if spin_free:
                return RIPfpLCCD1SF(*args, **kwargs)
            return RIPfpLCCD1(*args, **kwargs)
        raise ArgumentError(
            f"Unknown value of {alpha} for kwarg alpha. Supported values "
            "are 1."
        )


class RIPfpLCCSD:
    """
    Restricted Single Ionization Potential Equation of Motion Coupled Cluster
    class restricted to single IP for a fpLCCSD reference function

    This class overwrites __new__ to create an instance of the proper IP-fpLCCSD
    class for a user-specified number of unpaired electrons, which are passed
    using the keyword argument alpha:
        * alpha=1: RIPfpLCCSD1

    The return value of __new__() is the new object instance. It has no other
    purpose.
    """

    long_name = (
        "Ionization Potential Equation of Motion frozen pair Linearized Coupled "
        "Cluster Singles Doubles"
    )
    acronym = "IP-EOM-fpLCCSD"
    reference = "fpLCCSD"
    order = "IP"

    def __new__(cls, *args, **kwargs):
        """Called to create a new instance of class RIPfpLCCSD1 (alpha=1).
        The return value of __new__() is a new object instance.

        **Arguments**

        cls
            class of which an instance was requested.

        args, kwargs
            remaining arguments that are passed to the object constructor
            expression. They are also used in the call of __init__(self[, ...]),
            which is invoked after __new__(), where self is the new instance
            created.
        """
        alpha = kwargs.pop("alpha", -1)
        spin_free = kwargs.get("spinfree", False)
        if alpha == 1:
            if spin_free:
                return RIPfpLCCSD1SF(*args, **kwargs)
            return RIPfpLCCSD1(*args, **kwargs)
        raise ArgumentError(
            f"Unknown value of {alpha} for kwarg alpha. Supported values "
            "are 1."
        )
