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
# TODO: enable when, python3.7 is minimal python supported
# from __future__ import annotations

import pytest

from pybest.context import context
from pybest.exceptions import ArgumentError
from pybest.gbasis import Basis, get_gobasis
from pybest.linalg import DenseLinalgFactory
from pybest.occ_model import AufbauSpinOccModel

###############################################################################
## Tests for AufbauSpinOccModel ###############################################
###############################################################################

# All electrons are put into the alpha orbitals here
test_spin_aufbau = [
    # basis, molecule, charge, #unpaired electrons (alpha), ncore
    (
        "cc-pvdz",
        "test/water.xyz",
        {"ncore": 0},
        {
            "occ": [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], []],
            "charge": 0,
            "nel": 10,
            "nbasis": [24, 24],
            "nact": [24, 24],
            "nocc": [10, 0],
            "nvirt": [14, 24],
            "nacto": [10, 0],
            "nactv": [14, 24],
            "ncore": [0, 0],
            "nspin": [10, 0],
        },
    ),
    (
        "cc-pvdz",
        "test/water.xyz",
        {"charge": 1, "ncore": 0},
        {
            "occ": [[1, 1, 1, 1, 1, 1, 1, 1, 1], []],
            "charge": 1,
            "nel": 9,
            "nbasis": [24, 24],
            "nact": [24, 24],
            "nocc": [9, 0],
            "nvirt": [15, 24],
            "nacto": [9, 0],
            "nactv": [15, 24],
            "ncore": [0, 0],
            "nspin": [9, 0],
        },
    ),
    (
        "cc-pvdz",
        "test/water.xyz",
        {"ncore": 1},
        {
            "occ": [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], []],
            "charge": 0,
            "nel": 10,
            "nbasis": [24, 24],
            "nact": [23, 23],
            "nocc": [10, 0],
            "nvirt": [14, 24],
            "nacto": [9, -1],
            "nactv": [14, 24],
            "ncore": [1, 1],
            "nspin": [10, 0],
        },
    ),
    (
        "cc-pvdz",
        "test/water.xyz",
        {"charge": 1, "ncore": 1},
        {
            "occ": [[1, 1, 1, 1, 1, 1, 1, 1, 1], []],
            "charge": 1,
            "nel": 9,
            "nbasis": [24, 24],
            "nact": [23, 23],
            "nocc": [9, 0],
            "nvirt": [15, 24],
            "nacto": [8, -1],
            "nactv": [15, 24],
            "ncore": [1, 1],
            "nspin": [9, 0],
        },
    ),
]

###############################################################################
## Tests for AufbauSpinOccModel ###############################################
###############################################################################


@pytest.mark.parametrize("basis,mol,kwargs,expected", test_spin_aufbau)
def test_spin_occ_gobasis(basis, mol, kwargs, expected):
    """Test AufbauSpin model for gobasis, charge, alpha, and ncore arguments as
    input."""
    fn_xyz = context.get_fn(mol)
    gobasis = get_gobasis(basis, fn_xyz, print_basis=False)
    lf = DenseLinalgFactory(gobasis.nbasis)
    # either restricted (alpha=0) or unrestricted orbitals (alpha>0)
    norbs = 2
    orb = [lf.create_orbital() for n in range(norbs)]

    occ_model = AufbauSpinOccModel(gobasis, **kwargs)
    occ_model.assign_occ_reference(*orb)

    for key, value in expected.items():
        if key == "occ":
            # check occupation numbers of each orbital (alpha, beta)
            assert len(orb) == len(value)
            for orb_, el in zip(orb, value):
                if el:
                    assert abs(orb_.occupations[: len(el)] - el).max() < 1e-10
        else:
            # check all other attributes
            assert getattr(occ_model, key) == value


@pytest.mark.parametrize("basis,mol,kwargs,expected", test_spin_aufbau)
def test_spin_occ_lf(basis, mol, kwargs, expected):
    """Test AufbauSpin model for lf, nocc_a/nocc_b, and ncore arguments as
    input."""
    fn_xyz = context.get_fn(mol)
    gobasis = get_gobasis(basis, fn_xyz, print_basis=False)
    lf = DenseLinalgFactory(gobasis.nbasis)
    # either restricted (alpha=0) or unrestricted orbitals (alpha>0)
    norbs = 2
    orb = [lf.create_orbital() for n in range(norbs)]

    occ_model = AufbauSpinOccModel(lf, **kwargs, nel=expected["nel"])
    occ_model.assign_occ_reference(*orb)

    for key, value in expected.items():
        if key == "occ":
            # check occupation numbers of each orbital (alpha, beta)
            assert len(orb) == len(value)
            for orb_, el in zip(orb, value):
                if el:
                    assert abs(orb_.occupations[: len(el)] - el).max() < 1e-10
        else:
            # check all other attributes
            assert getattr(occ_model, key) == value


#
# Invalid calls, all test should raise an error
#

test_molecules = [
    (
        "cc-pvdz",
        "test/water.xyz",
    ),
]


test_wrong_arguments = [
    ({"nocc_a": 4.1}),
    ({"alpha": 0}),
    ({"nocc_b": 0}),
    ({"unrestricted": 0}),
]


@pytest.mark.parametrize("basis,mol", test_molecules)
@pytest.mark.parametrize("kwargs", test_wrong_arguments)
@pytest.mark.parametrize("factory", [Basis, DenseLinalgFactory])
def test_spin_occ_arguments_gobasis(basis, mol, kwargs, factory):
    """Test AufbauSpin model for proper keyword arguments."""
    fn_xyz = context.get_fn(mol)
    gobasis = get_gobasis(basis, fn_xyz, print_basis=False)

    # maps factory class to it's fixture instance
    factory_map = {
        Basis: gobasis,
        DenseLinalgFactory: DenseLinalgFactory(gobasis.nbasis),
    }

    with pytest.raises(ArgumentError):
        assert AufbauSpinOccModel(factory_map[factory], **kwargs)


#
# Test all valid kwargs
#

test_kwargs = [
    (
        "cc-pvdz",
        "test/water.xyz",
        {"charge": 0, "nel": 10, "ncore": 0},
    ),
]


@pytest.mark.parametrize("basis,mol,kwargs", test_kwargs)
@pytest.mark.parametrize("factory", [Basis, DenseLinalgFactory])
def test_occ_spin_kwargs(basis, mol, kwargs, factory):
    """Test AufbauSpin model for gobasis, nocc_a/nocc_b, and ncore arguments as
    input.
    """
    fn_xyz = context.get_fn(mol)
    gobasis = get_gobasis(basis, fn_xyz, print_basis=False)

    # maps factory class to it's fixture instance
    factory_map = {
        Basis: gobasis,
        DenseLinalgFactory: DenseLinalgFactory(gobasis.nbasis),
    }

    assert isinstance(
        AufbauSpinOccModel(factory_map[factory], **kwargs), AufbauSpinOccModel
    )


#
# Test assign_occ_reference for AufbauSpinOccModel
#

test_spin_occ_energy = [
    # basis, molecule, kwargs, orbital energies, expected values
    (
        "sto-6g",
        "test/li.xyz",
        {"nel": 3, "ncore": 0},
        [
            [-10, -5, -1, 2, 3],
            [-9, -4, 1, 3, 4],
        ],  # orb energies for alpha, beta
        {
            "occ": [[1, 1], [1]],
            "charge": 0,
            "nel": 3,
            "nbasis": [5, 5],
            "nact": [5, 5],
            "nocc": [2, 1],
            "nvirt": [3, 4],
            "nacto": [2, 1],
            "nactv": [3, 4],
            "ncore": [0, 0],
        },
    ),
    (
        "sto-6g",
        "test/li.xyz",
        {"nel": 3, "ncore": 0},
        [
            [-10, -1, -1, 2, 3],
            [-9, -4, 1, 3, 4],
        ],  # orb energies for alpha, beta
        {
            "occ": [[1], [1, 1]],
            "charge": 0,
            "nel": 3,
            "nbasis": [5, 5],
            "nact": [5, 5],
            "nocc": [1, 2],
            "nvirt": [4, 3],
            "nacto": [1, 2],
            "nactv": [4, 3],
            "ncore": [0, 0],
        },
    ),
    (
        "sto-6g",
        "test/li.xyz",
        {"nel": 3, "ncore": 1},
        [
            [-10, -5, -1, 2, 3],
            [-9, -4, 1, 3, 4],
        ],  # orb energies for alpha, beta
        {
            "occ": [[1, 1], [1]],
            "charge": 0,
            "nel": 3,
            "nbasis": [5, 5],
            "nact": [4, 4],
            "nocc": [2, 1],
            "nvirt": [3, 4],
            "nacto": [1, 0],
            "nactv": [3, 4],
            "ncore": [1, 1],
        },
    ),
    (
        "sto-6g",
        "test/li.xyz",
        {"nel": 2, "charge": 1, "ncore": 0},
        [
            [-10, -5, -1, 2, 3],
            [-9, -4, 1, 3, 4],
        ],  # orb energies for alpha, beta
        {
            "occ": [[1], [1]],
            "charge": 1,
            "nel": 2,
            "nbasis": [5, 5],
            "nact": [5, 5],
            "nocc": [1, 1],
            "nvirt": [4, 4],
            "nacto": [1, 1],
            "nactv": [4, 4],
            "ncore": [0, 0],
        },
    ),
    (
        "sto-6g",
        "test/li.xyz",
        {"nel": 2, "charge": 1, "ncore": 0},
        [
            [-10, -9.5, -1, 2, 3],
            [-9, -4, 1, 3, 4],
        ],  # orb energies for alpha, beta
        {
            "occ": [[1, 1], [0]],
            "charge": 1,
            "nel": 2,
            "nbasis": [5, 5],
            "nact": [5, 5],
            "nocc": [2, 0],
            "nvirt": [3, 5],
            "nacto": [2, 0],
            "nactv": [3, 5],
            "ncore": [0, 0],
        },
    ),
]


@pytest.mark.parametrize(
    "basis,mol,kwargs,energies,expected", test_spin_occ_energy
)
@pytest.mark.parametrize("factory", [Basis, DenseLinalgFactory])
def test_spin_occ_assign_reference(
    basis, mol, kwargs, energies, expected, factory
):
    """Test AufbauSpin model for gobasis arguments as input."""
    fn_xyz = context.get_fn(mol)
    gobasis = get_gobasis(basis, fn_xyz, print_basis=False)
    lf = DenseLinalgFactory(gobasis.nbasis)
    # either restricted (alpha=0) or unrestricted orbitals (alpha>0)
    norbs = 2
    orb = [lf.create_orbital() for n in range(norbs)]
    for energy, orb_ in zip(energies, orb):
        orb_.energies[:] = energy

    # maps factory class to it's fixture instance
    factory_map = {
        Basis: gobasis,
        DenseLinalgFactory: DenseLinalgFactory(gobasis.nbasis),
    }

    occ_model = AufbauSpinOccModel(factory_map[factory], **kwargs)

    occ_model.assign_occ_reference(*orb)
    assert isinstance(occ_model, AufbauSpinOccModel)

    for key, value in expected.items():
        if key == "occ":
            # check occupation numbers of each orbital (alpha, beta)
            assert len(orb) == len(value)
            for orb_, el in zip(orb, value):
                if el:
                    assert abs(orb_.occupations[: len(el)] - el).max() < 1e-10
        else:
            # check all other attributes
            assert getattr(occ_model, key) == value


def test_spin_ncore(ncore_test_with_atoms):
    """Test to see if it will automatically calculate the value of frozen core orbitals for AufbauSpinOccModel"""
    basis, mol, expected = ncore_test_with_atoms
    gobasis = get_gobasis(basis, mol, print_basis=False)

    occ_model = AufbauSpinOccModel(gobasis)

    assert occ_model.ncore[0] == expected
