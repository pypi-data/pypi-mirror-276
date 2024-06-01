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
#


from pybest.cc import (
    RCCD,
    RCCSD,
    RLCCD,
    RLCCSD,
    RfpCCD,
    RfpCCSD,
    RpCCDLCCD,
    RpCCDLCCSD,
)
from pybest.context import context
from pybest.gbasis import (
    compute_cholesky_eri,
    compute_eri,
    compute_kinetic,
    compute_nuclear,
    compute_nuclear_repulsion,
    compute_overlap,
    get_gobasis,
)
from pybest.geminals import ROOpCCD, RpCCD
from pybest.io.molden import load_molden
from pybest.ip_eom import (
    RIPCCD,
    RIPCCSD,
    RIPLCCD,
    RIPLCCSD,
    RDIPpCCD,
    RIPfpCCD,
    RIPfpCCSD,
    RIPfpLCCD,
    RIPfpLCCSD,
    RIPpCCD,
)
from pybest.linalg import (
    CholeskyLinalgFactory,
    DenseFourIndex,
    DenseLinalgFactory,
    DenseTwoIndex,
)
from pybest.occ_model import AufbauOccModel
from pybest.wrappers import RHF


class Molecule:
    def __init__(self, molfile, basis, lf_cls, **kwargs):
        self.mol_name = molfile
        fn = context.get_fn(f"test/{molfile}.xyz")
        self.obasis = get_gobasis(basis, fn, print_basis=False)
        #
        # Define Occupation model, expansion coefficients and overlap
        #
        self.lf = lf_cls(self.obasis.nbasis)
        self.occ_model = AufbauOccModel(self.obasis, **kwargs)
        self.orb = [self.lf.create_orbital(self.obasis.nbasis)]
        self.olp = compute_overlap(self.obasis)
        #
        # Construct Hamiltonian
        #
        kin = compute_kinetic(self.obasis)
        na = compute_nuclear(self.obasis)
        if isinstance(self.lf, CholeskyLinalgFactory):
            er = compute_cholesky_eri(self.obasis, threshold=1e-8)
        elif isinstance(self.lf, DenseLinalgFactory):
            er = compute_eri(self.obasis)
        external = compute_nuclear_repulsion(self.obasis)

        self.hamiltonian = [kin, na, er, external]
        self.one = kin.copy()
        self.one.iadd(na)
        self.two = er

        self.hf = None
        self.pccd = None
        self.oopccd = None
        self.ip_pccd = None
        self.dip_pccd = None
        self.ccd = None
        self.lccd = None
        self.fpccd = None
        self.fplccd = None
        self.ccsd = None
        self.lccsd = None
        self.fpccsd = None
        self.fplccsd = None
        self.ip_ccd = None
        self.ip_fpccd = None
        self.ip_fplccd = None
        self.ip_ccsd = None
        self.ip_fpccsd = None
        self.ip_fplccsd = None
        self.args = (self.olp, *self.orb, *self.hamiltonian, self.t_p)
        self.amplitudes = {"t_1": self.t_1, "t_2": self.t_2, "t_p": self.t_p}

    @property
    def t_p(self):
        if self.pccd is None:
            no, nv = self.occ_model.nacto[0], self.occ_model.nactv[0]
            return DenseTwoIndex(no, nv, label="t_p")
        return self.pccd.t_p

    @property
    def t_1(self):
        mask = (self.ccsd, self.lccsd, self.fpccsd, self.fplccsd)
        for instance in mask:
            # only one instance at a time is not None
            if instance is not None:
                return instance.t_1
        no, nv = self.occ_model.nacto[0], self.occ_model.nactv[0]
        return DenseTwoIndex(no, nv, label="t_1")

    @property
    def t_2(self):
        mask = (
            self.ccd,
            self.lccd,
            self.fpccd,
            self.fplccd,
            self.ccsd,
            self.lccsd,
            self.fpccsd,
            self.fplccsd,
        )
        for instance in mask:
            # only one instance at a time is not None
            if instance is not None:
                return instance.t_2
        no, nv = self.occ_model.nacto[0], self.occ_model.nactv[0]
        return DenseFourIndex(no, nv, no, nv, label="t_2")

    def do_series_calculations(self, *args, **kwargs):
        """Perform a series of calculations. Calculations should always be
        carried out in the order RHF->(pCCD->)CC->IP-CC, where the pCCD step
        can be skipped for CC on RHF.
        The translation is as follows:

        * hf -> RHF
        * pccd -> RpCCD
        * oopccd -> ROOpCCD
        * ccd -> RCCD
        * fpccd -> RfpCCD
        * fplccd -> RpCCDLCCD
        * ip_ccd -> RIPCCD
        * ip_fpccd -> RIPfpCCD
        * ip_fplccd -> RIPfpLCCD
        etc.
        """
        mask = {
            "hf": self.do_rhf,
            "pccd": self.do_pccd,
            "oopccd": self.do_pccd,
            "ccd": self.do_ccd,
            "lccd": self.do_lccd,
            "ccsd": self.do_ccsd,
            "lccsd": self.do_lccsd,
            "fpccd": self.do_fpccd,
            "fpccsd": self.do_fpccsd,
            "fplccd": self.do_fplccd,
            "fplccsd": self.do_fplccsd,
            "ip_ccd": self.do_ip_ccd,
            "ip_lccd": self.do_ip_lccd,
            "ip_lccsd": self.do_ip_lccsd,
            "ip_ccsd": self.do_ip_ccsd,
            "ip_fpccd": self.do_ip_fpccd,
            "ip_fpccsd": self.do_ip_fpccsd,
            "ip_fplccd": self.do_ip_fplccd,
            "ip_fplccsd": self.do_ip_fplccsd,
        }
        for arg in args:
            kwargs_ = kwargs.get(arg, {})
            if arg == "pccd":
                mask[arg](RpCCD, **kwargs_)
            elif arg == "oopccd":
                mask[arg](ROOpCCD, **kwargs_)
            elif "ip" in arg:
                kwargs_["spinfree"] = kwargs.get("spinfree", False)
                mask[arg](**kwargs_)
            else:
                mask[arg](**kwargs_)

    def do_rhf(self):
        """Do RHF calculation"""
        hf = RHF(self.lf, self.occ_model)
        self.hf = hf(*self.hamiltonian, self.olp, *self.orb)

    def do_pccd(self, pccd_cls, **kwargs):
        """Do pCCD calculation based on input class pccd_cls using this class'
        RHF solution.

        In case other orbitals are to be used, they can be passed using the
        `molden` kwarg where we assume that the orbitals are stored as
        `self.mol_name`.molden.
        """
        if self.hf is None:
            raise ValueError("No RHF solution found.")
        # read orbitals if passed
        molden_file = kwargs.pop("molden", False)
        args = ()
        if molden_file:
            molden_fn = context.get_fn(f"test/{self.mol_name}.molden")
            orb_a = load_molden(molden_fn)["orb_a"]
            args = (orb_a,)
        pccd = pccd_cls(self.lf, self.occ_model)
        self.pccd = pccd(*self.hamiltonian, self.hf, *args, **kwargs)
        self.oopccd = self.pccd

    def do_ip_pccd(self, alpha, nroot, nhole):
        """Do IP-pCCD calculation based on input class pccd_cls using this
        class' pCCD solution
        """
        if self.pccd is None:
            raise ValueError("No pCCD solution found.")
        ippccd = RIPpCCD(self.lf, self.occ_model, alpha=alpha)
        self.ip_pccd = ippccd(
            *self.hamiltonian, self.pccd, nroot=nroot, nhole=nhole
        )

    def do_dip_pccd(self, alpha, nroot, nhole):
        """Do DIP-pCCD calculation based on input class pccd_cls using this
        class' pCCD solution
        """
        if self.pccd is None:
            raise ValueError("No pCCD solution found.")
        dippccd = RDIPpCCD(self.lf, self.occ_model, alpha=alpha)
        self.dip_pccd = dippccd(
            *self.hamiltonian,
            self.pccd,
            nroot=nroot,
            nhole=nhole,
            nguessv=nroot * 10,
        )

    def do_ccd(self, **kwargs):
        """Do CCD calculation based on this class' RHF solution"""
        if self.hf is None:
            self.do_rhf()
        ccd = RCCD(self.lf, self.occ_model)
        self.ccd = ccd(*self.hamiltonian, self.hf, threshold_r=1e-6)

    def do_lccd(self, **kwargs):
        """Do LCCD calculation based on this class' RHF solution"""
        if self.hf is None:
            self.do_rhf()
        ccd = RLCCD(self.lf, self.occ_model)
        self.lccd = ccd(*self.hamiltonian, self.hf, threshold_r=1e-6)

    def do_ip_ccd(self, **kwargs):
        """Do IP-CCD calculation based on this class' CCD solution"""
        alpha = kwargs.get("alpha", 1)
        spin_free = kwargs.get("spinfree")
        nroot = kwargs.get("nroot")
        nhole = kwargs.get("nhole", 2)
        nguessv = kwargs.get("nguessv", nroot * 10)
        if self.ccd is None:
            self.do_ccd()
        ippccd = RIPCCD(
            self.lf, self.occ_model, alpha=alpha, spinfree=spin_free
        )
        self.ip_ccd = ippccd(
            *self.hamiltonian,
            self.ccd,
            nroot=nroot,
            nhole=nhole,
            tolerancev=1e-8,
            nguessv=nguessv,
        )

    def do_ip_lccd(self, **kwargs):
        """Do IP-LCCD calculation based on this class' LCCD solution"""
        alpha = kwargs.get("alpha", 1)
        spin_free = kwargs.get("spinfree")
        nroot = kwargs.get("nroot")
        nhole = kwargs.get("nhole", 2)
        nguessv = kwargs.get("nguessv", nroot * 10)
        if self.lccd is None:
            self.do_lccd()
        ippccd = RIPLCCD(
            self.lf, self.occ_model, alpha=alpha, spinfree=spin_free
        )
        self.ip_lccd = ippccd(
            *self.hamiltonian,
            self.lccd,
            nroot=nroot,
            nhole=nhole,
            tolerancev=1e-8,
            nguessv=nguessv,
        )

    def do_fpccd(self, **kwargs):
        """Do fpCCD calculation based on this class' pCCD solution"""
        if self.pccd is None:
            raise ValueError("No pCCD solution found.")
        ccd = RfpCCD(self.lf, self.occ_model)
        self.fpccd = ccd(*self.hamiltonian, self.pccd, threshold_r=1e-6)

    def do_ip_fpccd(self, **kwargs):
        """Do IP-fpCCD calculation based on this class' fpCCD solution"""
        if self.fpccd is None:
            raise ValueError("No fpCCD solution found.")
        alpha = kwargs.get("alpha", 1)
        spin_free = kwargs.get("spinfree")
        nroot = kwargs.get("nroot")
        nhole = kwargs.get("nhole", 2)
        nguessv = kwargs.get("nguessv", nroot * 10)
        ippccd = RIPfpCCD(
            self.lf, self.occ_model, alpha=alpha, spinfree=spin_free
        )
        self.ip_ccd = ippccd(
            *self.hamiltonian,
            self.fpccd,
            nroot=nroot,
            nhole=nhole,
            tolerancev=1e-8,
            nguessv=nguessv,
        )

    def do_fplccd(self, **kwargs):
        """Do fpLCCD calculation based on this class' pCCD solution"""
        if self.pccd is None:
            raise ValueError("No pCCD solution found.")
        ccd = RpCCDLCCD(self.lf, self.occ_model)
        self.fplccd = ccd(*self.hamiltonian, self.pccd, threshold_r=1e-6)

    def do_ip_fplccd(self, **kwargs):
        """Do IP-fpLCCD calculation based on this class' fpLCCD solution"""
        if self.fplccd is None:
            raise ValueError("No fpLCCD solution found.")
        alpha = kwargs.get("alpha", 1)
        spin_free = kwargs.get("spinfree")
        nroot = kwargs.get("nroot")
        nhole = kwargs.get("nhole", 2)
        nguessv = kwargs.get("nguessv", nroot * 10)
        ippccd = RIPfpLCCD(
            self.lf, self.occ_model, alpha=alpha, spinfree=spin_free
        )
        self.ip_ccd = ippccd(
            *self.hamiltonian,
            self.fplccd,
            nroot=nroot,
            nhole=nhole,
            tolerancev=1e-8,
            nguessv=nguessv,
        )

    def do_ccsd(self, **kwargs):
        """Do CCSD calculation using this class' RHF solution"""
        if self.hf is None:
            self.do_rhf()
        ccsd = RCCSD(self.lf, self.occ_model)
        self.ccsd = ccsd(*self.hamiltonian, self.hf, threshold_r=1e-6)

    def do_lccsd(self, **kwargs):
        """Do LCCSD calculation using this class' RHF solution"""
        if self.hf is None:
            self.do_rhf()
        ccsd = RLCCSD(self.lf, self.occ_model)
        options = {"solver": "krylov", "threshold_r": 1e-6}
        self.lccsd = ccsd(*self.hamiltonian, self.hf, **options)

    def do_ip_ccsd(self, **kwargs):
        """Do IP-CCSD calculation using this class' CCSD solution"""
        alpha = kwargs.get("alpha", 1)
        spin_free = kwargs.get("spinfree")
        nroot = kwargs.get("nroot")
        nhole = kwargs.get("nhole", 2)
        nguessv = kwargs.get("nguessv", nroot * 10)
        if self.ccsd is None:
            self.do_ccsd()
        ippccsd = RIPCCSD(
            self.lf, self.occ_model, alpha=alpha, spinfree=spin_free
        )
        self.ip_ccsd = ippccsd(
            *self.hamiltonian,
            self.ccsd,
            nroot=nroot,
            nhole=nhole,
            tolerancev=1e-8,
            nguessv=nguessv,
        )

    def do_ip_lccsd(self, **kwargs):
        """Do IP-LCCSD calculation using this class' LCCSD solution"""
        alpha = kwargs.get("alpha", 1)
        spin_free = kwargs.get("spinfree")
        nroot = kwargs.get("nroot")
        nhole = kwargs.get("nhole", 2)
        nguessv = kwargs.get("nguessv", nroot * 10)
        if self.lccsd is None:
            self.do_lccsd()
        ippccsd = RIPLCCSD(
            self.lf, self.occ_model, alpha=alpha, spinfree=spin_free
        )
        self.ip_lccsd = ippccsd(
            *self.hamiltonian,
            self.lccsd,
            nroot=nroot,
            nhole=nhole,
            tolerancev=1e-8,
            nguessv=nguessv,
        )

    def do_fpccsd(self, **kwargs):
        """Do fpCCSD calculation using this class' pCCD solution"""
        if self.pccd is None:
            raise ValueError("No pCCD solution found.")
        ccsd = RfpCCSD(self.lf, self.occ_model)
        self.fpccsd = ccsd(*self.hamiltonian, self.pccd, threshold_r=1e-6)

    def do_ip_fpccsd(self, **kwargs):
        """Do IP-fpCCSD calculation using this class' fpCCSD solution"""
        if self.fpccsd is None:
            raise ValueError("No CCD solution found.")
        alpha = kwargs.get("alpha", 1)
        spin_free = kwargs.get("spinfree")
        nroot = kwargs.get("nroot")
        nhole = kwargs.get("nhole", 2)
        nguessv = kwargs.get("nguessv", nroot * 10)
        ippccsd = RIPfpCCSD(
            self.lf, self.occ_model, alpha=alpha, spinfree=spin_free
        )
        self.ip_fpccsd = ippccsd(
            *self.hamiltonian,
            self.fpccsd,
            nroot=nroot,
            nhole=nhole,
            tolerancev=1e-8,
            nguessv=nguessv,
        )

    def do_fplccsd(self, **kwargs):
        """Do fpLCCSD calculation using this class' pCCD solution"""
        if self.pccd is None:
            raise ValueError("No pCCD solution found.")
        ccsd = RpCCDLCCSD(self.lf, self.occ_model)
        self.fplccsd = ccsd(*self.hamiltonian, self.pccd, threshold_r=1e-6)

    def do_ip_fplccsd(self, **kwargs):
        """Do IP-fpLCCSD calculation using this class' fpLCCSD solution"""
        if self.fplccsd is None:
            raise ValueError("No fpLCCD solution found.")
        alpha = kwargs.get("alpha", 1)
        spin_free = kwargs.get("spinfree")
        nroot = kwargs.get("nroot")
        nhole = kwargs.get("nhole", 2)
        nguessv = kwargs.get("nguessv", nroot * 10)
        ippccsd = RIPfpLCCSD(
            self.lf, self.occ_model, alpha=alpha, spinfree=spin_free
        )
        self.ip_fplccsd = ippccsd(
            *self.hamiltonian,
            self.fplccsd,
            nroot=nroot,
            nhole=nhole,
            tolerancev=1e-8,
            nguessv=nguessv,
        )
