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

"""Unit tests for RCCHamiltonianBlocks."""

from pybest.cache import Cache
from pybest.cc.rcc_cache import RCCHamiltonianBlocks

from .common import check_eri_in_cache, check_fock_in_cache


def test_can_construct_hamiltonian_blocks(linalg, h2o_molecule):
    "Check if Hamiltonian property contains expected blocks."
    model = h2o_molecule["model"]
    kin, nuc, eri = model.ints(linalg_factory=linalg)
    one = kin.copy()
    one.iadd(nuc)
    fock = ["fock_oo", "fock_ov", "fock_vv"]
    ham_eri = [
        "eri_oooo",
        "eri_ooov",
        "eri_oovv",
        "eri_ovov",
        "eri_ovvv",
        "eri_vvov",
    ]
    ham_exc = ["exc_oovv", "exc_ooov"]
    blocks = fock + ham_eri + ham_exc
    norb = {"occ": 5, "virt": 8, "core": 0, "acto": 5, "actv": 8, "act": 13}
    ham = RCCHamiltonianBlocks(blocks, one, eri, model.orb_a, norb)
    assert isinstance(ham.cache, Cache)

    # Check the Fock matrix blocks
    check_fock_in_cache(ham.cache, fock, nocc=5, nvirt=8)
    # Check 2-body Hamiltonian Coulomb and exchange blocks
    check_eri_in_cache(ham.cache, ham_eri + ham_exc, nocc=5, nvirt=8)
