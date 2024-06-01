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
"""
Variables used in this module:
 :ncore:     number of frozen core orbitals
 :nacto:     number of active occupied orbitals in the principal configuration
 :nvirt:     number of virtual orbitals in the principal configuration
 :nactv:     number of active virtual orbitals in the principal configuration
 :nact:      total number of active orbitals (nacto+nactv)
 :e_ci:      eigenvalues of CI Hamiltonian (IOData container attribute)
 :civ:       eigenvectors of CI Hamiltonian (IOData container attribute)

 Indexing convention:
  :i,j,k,..: occupied orbitals of principal configuration
  :a,b,c,..: virtual orbitals of principal configuration
"""

from pybest.ci.sd_base import SD
from pybest.log import log


class SDRCIS(SD):
    """Slater Determinant Restricted Configuration Interaction Singles child class.
    Contains all required methods to diagonalize the RCIS Hamiltonian using SD basis.
    """

    @SD.dimension.setter
    def dimension(self, new=None):
        rci = self.instance
        if new is not None:
            self._dimension = self.set_dimension(new, rci.nacto, rci.nactv)
        else:
            log.warn(
                "The dimension may be wrong!"
                "Please set the dimension property with one of the strings (RCIS, RCID, RCISD)"
            )

    def compute_h_diag(self, *args):
        """Used by the davidson module for pre-conditioning."""
        rci = self.instance
        #
        # Auxiliary objects
        #
        fock = rci.from_cache("fock")
        govvo = rci.from_cache("govvo")
        govov = rci.from_cache("govov")

        hdiag = rci.lf.create_one_index(self.dimension)
        tmp = rci.lf.create_two_index(rci.nacto, rci.nactv)

        # 1 <ia|ai>
        govvo.contract("abba->ab", out=tmp, factor=1.0, select="einsum")

        # 2 <ia|ia>
        govov.contract("abab->ab", out=tmp, factor=-2.0, select="einsum")

        # 3 fii
        fii = rci.lf.create_one_index(rci.nacto)
        fock.copy_diagonal(out=fii, begin=0, end=rci.nacto)
        tmp.iadd_expand_one_to_two("a->ab", fii, factor=-1.0)

        # 4 faa
        faa = rci.lf.create_one_index(rci.nactv)
        fock.copy_diagonal(out=faa, begin=rci.nacto, end=rci.nacto + rci.nactv)
        tmp.iadd_expand_one_to_two("b->ab", faa, factor=1.0)

        hdiag.set_element(0, 0)
        hdiag.assign(tmp.ravel(), begin0=1)

        return hdiag

    def build_subspace_hamiltonian(self, bvector, hamiltonian, *args):
        """
        Used by the davidson module to construct subspace Hamiltonian

        **Arguments:**

        bvector:
            (OneIndex object) contains current approximation to CI coefficients

        hamiltonian:
            (OneIndex object) used by the Davidson module and contains
            diagonal approximation to the full matrix
        """
        rci = self.instance
        nacto = rci.nacto
        nactv = rci.nactv
        #
        # Integrals
        #
        fock = rci.from_cache("fock")
        govvo = rci.from_cache("govvo")
        govov = rci.from_cache("govov")

        #
        # Ranges
        #
        ov = rci.get_range("ov")
        oo = rci.get_range("oo")
        vv = rci.get_range("vv")
        ov2 = rci.get_range("ov", start=2)

        sigma_s = rci.lf.create_one_index(self.dimension)
        b_s = rci.lf.create_two_index(nacto, nactv)
        sigma = rci.lf.create_two_index(nacto, nactv)

        #
        # local variables
        #
        b_s.assign(bvector, begin2=1)
        c_0 = bvector.get_element(0)

        # 1) fjb * cjb
        sum0 = fock.contract("ab,ab", b_s, **ov) * 2.0
        # 2) <aj|ib> * cjb
        govvo.contract("abcd,ac->db", b_s, sigma, factor=2.0)
        # 3) <aj|bi> * cjb
        govov.contract("abcd,ad->cb", b_s, sigma, factor=-1.0)
        # 4) fab * cib
        fock.contract("ab,cb->ca", b_s, sigma, factor=1.0, **vv)
        # 5) fij * cja
        fock.contract("ab,bc->ac", b_s, sigma, factor=-1.0, **oo)
        # 6) fia * c0
        sigma.iadd(fock, factor=c_0, **ov2)

        sigma_s.set_element(0, sum0)
        sigma_s.assign(sigma.ravel(), begin0=1)
        return sigma_s

    def get_index_s(self, index):
        """Get index for single excitation."""
        rci = self.instance
        b = index % rci.nactv
        j = ((index - b) / rci.nactv) % rci.nacto
        return int(j), int(b)
