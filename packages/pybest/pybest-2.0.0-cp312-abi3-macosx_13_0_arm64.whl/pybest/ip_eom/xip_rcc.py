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
various CC reference functions.

Various IP flavors are selected from two classes:
 * RIPLCCD:   selects a specific single IP method based on LCCD
 * RIPLCCSD:  selects a specific single IP method based on LCCSD
 * RIPCCD:    selects a specific single IP method based on CCD
 * RIPCCSD:   selects a specific single IP method based on CCSD
"""

from pybest.exceptions import ArgumentError
from pybest.ip_eom.sip_rccd1 import RIPCCD1, RIPLCCD1
from pybest.ip_eom.sip_rccd1_sf import RIPCCD1SF, RIPLCCD1SF
from pybest.ip_eom.sip_rccsd1 import RIPCCSD1, RIPLCCSD1
from pybest.ip_eom.sip_rccsd1_sf import RIPCCSD1SF, RIPLCCSD1SF


class RIPLCCD:
    """
    Restricted Single Ionization Potential Equation of Motion Coupled Cluster
    class restricted to single IP for an LCCD reference function

    This class overwrites __new__ to create an instance of the proper IP-LCCD
    class for a user-specified number of unpaired electrons, which are passed
    using the keyword argument alpha:
        * alpha=1: RIPLCCD1

    The return value of __new__() is the new object instance. It has no other
    purpose.
    """

    long_name = "Ionization Potential Equation of Motion Linearized Coupled Cluster Doubles"
    acronym = "IP-EOM-LCCD"
    reference = "LCCD"
    order = "IP"

    def __new__(cls, *args, **kwargs):
        """Called to create a new instance of class RIPLCCD1 (alpha=1).
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
                return RIPLCCD1SF(*args, **kwargs)
            return RIPLCCD1(*args, **kwargs)
        raise ArgumentError(
            f"Unknown value of {alpha} for kwarg alpha. Supported values "
            "are 1."
        )


class RIPLCCSD:
    """
    Restricted Single Ionization Potential Equation of Motion Coupled Cluster
    class restricted to single IP for a LCCSD reference function

    This class overwrites __new__ to create an instance of the proper IP-LCCSD
    class for a user-specified number of unpaired electrons, which are passed
    using the keyword argument alpha:
        * alpha=1: RIPLCCSD1

    The return value of __new__() is the new object instance. It has no other
    purpose.
    """

    long_name = (
        "Ionization Potential Equation of Motion Linearized Coupled Cluster "
        "Singles Doubles"
    )
    acronym = "IP-EOM-LCCSD"
    reference = "LCCSD"
    order = "IP"

    def __new__(cls, *args, **kwargs):
        """Called to create a new instance of class RIPLCCSD1 (alpha=1).
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
                return RIPLCCSD1SF(*args, **kwargs)
            return RIPLCCSD1(*args, **kwargs)
        raise ArgumentError(
            f"Unknown value of {alpha} for kwarg alpha. Supported values "
            "are 1."
        )


class RIPCCD:
    """
    Restricted Single Ionization Potential Equation of Motion Coupled Cluster
    class restricted to single IP for a CCD reference function

    This class overwrites __new__ to create an instance of the proper IP-CCD
    class for a user-specified number of unpaired electrons, which are passed
    using the keyword argument alpha:
        * alpha=1: RIPCCD1

    The return value of __new__() is the new object instance. It has no other
    purpose.
    """

    long_name = (
        "Ionization Potential Equation of Motion Coupled Cluster Doubles"
    )
    acronym = "IP-EOM-CCD"
    reference = "CCD"
    order = "IP"

    def __new__(cls, *args, **kwargs):
        """Called to create a new instance of class RIPCCD1 (alpha=1).
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
                return RIPCCD1SF(*args, **kwargs)
            return RIPCCD1(*args, **kwargs)
        raise ArgumentError(
            f"Unknown value of {alpha} for kwarg alpha. Supported values "
            "are 1."
        )


class RIPCCSD:
    """
    Restricted Single Ionization Potential Equation of Motion Coupled Cluster
    class restricted to single IP for a CCSD reference function

    This class overwrites __new__ to create an instance of the proper IP-CCSD
    class for a user-specified number of unpaired electrons, which are passed
    using the keyword argument alpha:
        * alpha=1: RIPCCSD1

    The return value of __new__() is the new object instance. It has no other
    purpose.
    """

    long_name = "Ionization Potential Equation of Motion Coupled Cluster Singles Doubles"
    acronym = "IP-EOM-CCSD"
    reference = "CCSD"
    order = "IP"

    def __new__(cls, *args, **kwargs):
        """Called to create a new instance of class RIPCCSD1 (alpha=1).
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
                return RIPCCSD1SF(*args, **kwargs)
            return RIPCCSD1(*args, **kwargs)
        raise ArgumentError(
            f"Unknown value of {alpha} for kwarg alpha. Supported values "
            "are 1."
        )
