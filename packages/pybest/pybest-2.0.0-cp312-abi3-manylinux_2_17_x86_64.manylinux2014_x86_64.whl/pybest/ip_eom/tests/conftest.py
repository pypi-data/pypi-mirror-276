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

import pytest

from .common import Molecule


#
# Define fixtures for testing: NO^{-}
#
@pytest.fixture
def no_1m(linalg):
    """Returns instance of Molecule for NO^- that contains all information
    to perform several calculations (integrals, methods, etc.)."""
    return Molecule("no", "cc-pvdz", linalg, charge=-1, ncore=0)


#
# Define fixtures for testing: C^{2-}
#
@pytest.fixture
def c_2m(linalg):
    """Returns instance of Molecule for C^2- that contains all information
    to perform several calculations (integrals, methods, etc.)."""
    return Molecule("c", "cc-pvdz", linalg, charge=-2, ncore=0)


#
# Define fixtures for testing: Be_2
#
@pytest.fixture
def be_2(linalg_slow):
    """Returns instance of Molecule for Be_2 that contains all information
    to perform several calculations (integrals, methods, etc.) and the
    corresponding solutions."""
    molecule = Molecule("be2", "cc-pvdz", linalg_slow, ncore=0)
    results = {
        "e_hf": -28.948818627810,
        "e_oopccd": -28.997549647067,
        "e_ccd": -29.0386605786,
        "e_fpccd": -29.0366116300,
        "e_fplccd": -29.0374085873,
        "e_ip_ccd": [
            2.309341e-01,
            2.662573e-01,
            3.080507e-01,
            3.455325e-01,
        ],
        "e_ip_fpccd": [
            2.265904e-01,
            2.636954e-01,
            3.019214e-01,
            3.376309e-01,
        ],
        "e_ip_fplccd": [
            2.270267e-01,
            2.644758e-01,
            3.027015e-01,
            3.384222e-01,
        ],
        "e_ccsd": -29.0396637656,
        "e_lccsd": -29.0380068187,
        "e_fpccsd": -29.0367717243,
        "e_fplccsd": -29.0376846918,
        "e_ip_ccsd": [
            2.317876e-01,
            2.683284e-01,
            3.106148e-01,
            3.465028e-01,
        ],
        "e_ip_lccsd": [
            2.257639e-01,
            2.671789e-01,
            3.077205e-01,
            3.316917e-01,
        ],
        "e_ip_fpccsd": [
            2.276117e-01,
            2.653681e-01,
            3.042440e-01,
        ],
        "e_ip_fplccsd": [
            2.281413e-01,
            2.664327e-01,
            3.053801e-01,
        ],
    }
    return {"molecule": molecule, "results": results}
