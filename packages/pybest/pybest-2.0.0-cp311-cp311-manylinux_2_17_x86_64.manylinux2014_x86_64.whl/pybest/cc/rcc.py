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
"""Restricted Coupled Cluster Class

Variables used in this module:
 :nocc:      number of occupied orbitals in the principle configuration
 :nvirt:     number of virtual orbitals in the principle configuration
 :ncore:     number of frozen core orbitals in the principle configuration
 :nbasis:    total number of basis functions
 :energy:    the CC energy, dictionary that contains different
             contributions
 :t_1, t_2:  the optimized amplitudes

 Indexing convention:
 :o:        matrix block corresponding to occupied orbitals of principle
            configuration
 :v:        matrix block corresponding to virtual orbitals of principle
            configuration
"""
# NOTE:
# - fix tags for cache instances to allow to take full string not resolved into
#   single characters

import copy
import gc
import pathlib
import time
from abc import ABC, abstractmethod

import numpy as np
from scipy import optimize as opt

from pybest.cache import Cache
from pybest.constants import CACHE_DUMP_ACTIVE_ORBITAL_THRESHOLD as CACHE_THR
from pybest.exceptions import ArgumentError, NonEmptyData, UnknownOption
from pybest.featuredlists import OneBodyHamiltonian, TwoBodyHamiltonian
from pybest.io.checkpoint import CheckPoint
from pybest.io.iodata import IOData
from pybest.linalg import DenseLinalgFactory, TwoIndex
from pybest.log import log
from pybest.solvers import PBQuasiNewton
from pybest.utility import (
    check_options,
    check_type,
    split_core_active,
    transform_integrals,
    unmask,
    unmask_orb,
)


class RCC(ABC):
    """Restricted Coupled Cluster Class

    Purpose:
    Optimize cluster amplitudes and determine energy corrections to some
    reference wave function.

    Currently supported reference wave function models:
        * RHF
        * RAP1roG / pCCD
        * DMRG (requires external file with DMRG-CC amplitudes)

    Currently supported cluster operators:
        * doubles
        * singles and doubles
        * singles and doubles without pair-doubles (frozen-pair flavours)
        * external singles and doubles (tailored flavours)

    """

    acronym = ""
    long_name = ""
    reference = ""
    cluster_operator = ""

    def __init__(self, lf, occ_model, **kwargs):
        """Arguments:

            lf : DenseLinalgFactory or CholeskyLinalgFactory

            occ_model : AufbauOccModel

        Keyword arguments:
            ncore : int
                number of frozen core orbitals

            nact : int
                number of active orbitals
        """
        for kwarg in kwargs:
            if kwarg not in ["ncore", "nact"]:
                raise ArgumentError(f"Keyword {kwarg} not recognized.")
        self._lf = lf
        self._denself = DenseLinalgFactory(lf.default_nbasis)
        self._occ_model = occ_model
        self._cache = Cache()
        self._energy = {"e_ref": 0, "e_corr": 0, "e_tot": 0}

        self._nocc = occ_model.nocc[0]
        self._nvirt = lf.default_nbasis - occ_model.nocc[0]
        self._ncore = occ_model.ncore[0]
        self._nact = kwargs.get("nact", lf.default_nbasis - self._ncore)
        self._nacto = self._nocc - self._ncore
        self._nactv = self._nact - self._nacto
        self._nov = self._nacto * self._nactv

        if self._nvirt < 0:
            raise ValueError(
                "Input error: the number of active virtual orbitals larger"
                "than a number of orbitals."
            )

        self._converged = False
        self._converged_l = False
        self._e_core = 0.0
        self._e_ref = 0.0
        self._iter = 0
        self._iter_l = 0
        self._time = 0.0
        self._filename = f"checkpoint_{self.acronym}.h5"
        self._initguess = "mp2"
        self._maxiter = 100
        self._dump_cache = self._occ_model.nact[0] > CACHE_THR
        # If something is difficult to converge, PBQN will indicate it much
        # faster than Krylov so that we can adjust other solver options
        self._solver = "pbqn"
        self._solver_parameters = {}
        self._threshold_r = 1e-5
        self._threshold_e = 1e-6
        self._diis = {}
        self._diis_l = {}
        self._l = False
        self._tco = None

    ### Instance properties

    @property
    def lf(self):
        """The linalg factory."""
        return self._lf

    @property
    def denself(self):
        """The linalg factory."""
        return self._denself

    @property
    def occ_model(self):
        """The occupation model."""
        return self._occ_model

    @property
    def nocc(self):
        """The number of occupied orbitals."""
        return self._nocc

    @property
    def nvirt(self):
        """The number of virtual orbitals."""
        return self._nvirt

    @property
    def ncore(self):
        """The number of frozen core (uncorrelated) orbitals."""
        return self._ncore

    @property
    def nact(self):
        """The number of active orbitals."""
        return self._nact

    @property
    def nacto(self):
        """The number of active occupied orbitals."""
        return self._nacto

    @property
    def nactv(self):
        """The number of active virtual orbitals."""
        return self._nactv

    @property
    def converged(self):
        """Status of calculations."""
        return self._converged

    @converged.setter
    def converged(self, status):
        assert isinstance(status, bool)
        self._converged = status

    @property
    def converged_l(self):
        """Status of calculation of Lambda equations."""
        return self._converged_l

    @converged_l.setter
    def converged_l(self, status):
        assert isinstance(status, bool)
        self._converged_l = status

    @property
    def e_core(self):
        """Scalar contributions to energy, e.g. in frozen core flavours."""
        return self._e_core

    @e_core.setter
    def e_core(self, core_energy):
        self._e_core = core_energy

    @property
    def e_ref(self):
        """Energy of a reference determinant."""
        return self._e_ref

    @e_ref.setter
    def e_ref(self, reference_energy):
        self._e_ref = reference_energy

    @property
    def iteration(self):
        """Iteration counter."""
        return self._iter

    @property
    def iter_l(self):
        """Iteration counter for Lambda equations."""
        return self._iter_l

    @property
    def time(self):
        """Iteration time counter."""
        return self._time

    @property
    def filename(self):
        """Name of an output file."""
        return self._filename

    @filename.setter
    def filename(self, name):
        self._filename = name

    @property
    def dump_cache(self):
        """Decide whether intermediates are dumped to disk or kept in memory"""
        return self._dump_cache

    @dump_cache.setter
    def dump_cache(self, new):
        self._dump_cache = new

    @property
    def initguess(self):
        """Type of initial guess for amplitudes."""
        return self._initguess

    @initguess.setter
    def initguess(self, initguess="random"):
        available = ["random", "mp2", "constant"]
        if pathlib.Path(str(initguess)).is_file():
            self._initguess = pathlib.Path(initguess)
        elif isinstance(initguess, str) and initguess.lower() in available:
            self._initguess = initguess.lower()
        elif isinstance(initguess, IOData):
            self._initguess = initguess
        elif isinstance(initguess, dict):
            self._initguess = initguess
        else:
            msg = f"Initial guess {initguess} has not been recognized."
            raise UnknownOption(msg)

    @property
    def maxiter(self):
        """Maximum number of iterations."""
        return self._maxiter

    @maxiter.setter
    def maxiter(self, number):
        self._maxiter = int(number)

    @property
    def solver(self):
        """Solver for CC equations."""
        return self._solver

    @solver.setter
    def solver(self, solver):
        """Solver setter for CC equations."""
        self._solver = solver

    @staticmethod
    def _check_diis_options(diis_):
        # Check for possible options
        for name, _ in diis_.items():
            check_options(name, name, "diismax", "diisstart", "diisreset")
        # Check for reasonable values
        if diis_["diismax"] < 0:
            raise UnknownOption("At least one diis vector has to be used!")
        if diis_["diisstart"] < 0:
            raise UnknownOption(
                "First DIIS iteration has to be larger than or equal to 0!"
            )
        check_options("diisreset", diis_["diisreset"], True, False, 0, 1)

    @property
    def diis(self):
        """DIIS options used in PyBEST's internal solvers (dictionary)."""
        return self._diis

    @diis.setter
    def diis(self, diis_):
        # Check for possible options
        self._check_diis_options(diis_)
        self._diis = diis_

    @property
    def diis_l(self):
        """DIIS options used in PBQN solver for Lambda equations (dictionary)."""
        return self._diis_l

    @diis_l.setter
    def diis_l(self, diis_):
        # Check for possible options
        self._check_diis_options(diis_)
        self._diis_l = diis_

    @property
    def solver_parameters(self):
        """Parameters used in SciPy solvers (dictionary)."""
        return self._solver_parameters

    @solver_parameters.setter
    def solver_parameters(self, parameter):
        # Check for possible options
        for name, _ in parameter.items():
            check_options(
                name,
                name,
                "inner_maxiter",
                "inner_method",
                "mix_maxiter",
                "mix_method",
            )
        # Update dictionary
        self._solver_parameters.update(**parameter)
        # Check for reasonable values
        check_type(
            "inner_maxiter", self._solver_parameters["inner_maxiter"], int
        )
        check_type("mix_maxiter", self._solver_parameters["mix_maxiter"], int)
        if self._solver_parameters["inner_maxiter"] < 0:
            raise UnknownOption("At least one inner iterations is required!")
        if self._solver_parameters["mix_maxiter"] < 0:
            raise UnknownOption("At least one inner iterations is required!")
        if self._solver_parameters["inner_method"] not in [
            "minres",
            "lgmres",
            "gmres",
            "bicgstab",
            "cgs",
            "tfqmr",
        ]:
            raise UnknownOption("Approximation to the Jacobian unkown!")

    @property
    def threshold_r(self):
        """Threshold for CC residual vector."""
        return self._threshold_r

    @threshold_r.setter
    def threshold_r(self, value):
        if not isinstance(value, float):
            raise ValueError("Threshold must be a float number.")
        self._threshold_r = value

    @property
    def threshold_e(self):
        """Threshold for CC energy."""
        return self._threshold_e

    @threshold_e.setter
    def threshold_e(self, value):
        if not isinstance(value, float):
            raise ValueError("Threshold must be a float number.")
        self._threshold_e = value

    @property
    def cache(self):
        """A Cache instance that stores the CC Hamiltonian in form of
        computation-friendly blocks and CC RDMs in form of sub-blocks.
        Different tags are used:
        :h: It contains blocks of Fock matrix and two-body electron repulsion
            integrals.
        :d: It contains blocks of matrices and tensors for non-zero elements of
            various N-RDMs.
        """
        return self._cache

    @abstractmethod
    def set_hamiltonian(self, ham_1_ao, ham_2_ao, mos):
        """Saves blocks of Hamiltonian to cache."""

    @abstractmethod
    def set_dm(self, *args):
        """Determine all supported RDMs and put them into the cache."""

    @property
    def jacobian_approximation(self):
        """The level of approximation to the Jacobian."""
        return self._jacobian_approximation

    @jacobian_approximation.setter
    @abstractmethod
    def jacobian_approximation(self, new):
        """Set Jacobian approximation"""

    @property
    def lambda_equations(self):
        """The lambda amplitudes"""
        return self._l

    @lambda_equations.setter
    def lambda_equations(self, args):
        if args is not None:
            self._l = args

    @property
    def tco(self):
        """The tensor contraction operation used"""
        return self._tco

    @tco.setter
    def tco(self, args):
        check_options("tco", args, None, "td", "einsum", "opt_einsum", "cupy")
        self._tco = args

    ### Routines

    def __call__(self, *args, **kwargs):
        """Optimize cluster amplitudes and determine energy correction to some
        Hamiltonian and reference wavefunction.

           Cluster amplitudes are determined by finding the root of a set of
           equations of the form A.x = 0

           Currently supported reference wavefunction models (Psi_0):

               * RHF
               * pCCD/AP1roG (default if geminal coeffs are provided)
               * DMRG (default if dmrg cc amplitudes are provided)

           Arguments:
               ham_1 : DenseTwoIndex
                   One-electron integrals in the AO basis.

               ham_2 : DenseFourIndex or CholeskyFourIndex
                   Electron repulsion integrals in the AO basis.

               orb : DenseOrbital
                   MO coefficients.

            OR

               IOData instance containing all above information.


           Keyword arguments:
           Contains reference energy and solver specific input parameters:

               filename : str
                   path to file where current solution is dumped
                   (default ./checkpoint_method.h5).

               e_ref : float
                   Reference energy (default value 0.0).

               geminal : DenseTwoIndex
                   Geminal amplitudes from pCCD/AP1roG calculations

               initguess : str or numpy.ndarray
                   Initial guess for amplitudes, one of:
                   * "random" - random numbers,
                   * "mp2" - performs MP2 calculations before,
                   * "const" - uses constant number, used for debugging,
                   * path to file - path to .h5 file containing amplitudes
                       (saved as checkpoint_method.h5 by default),
                   * dict of amplitudes {"t_2": DenseFourIndexInstance, ...}
                   * IOData containing amplitudes as attributes (t_1, t_2, ...)

               maxiter : int
                   Maximum number of iterations (default: 100).

               solver : str
                   one of scipy.optimize.root solvers or PyBEST internal solvers
                   (default: "pbqn").

               inner_maxiter : int
                   Maximum number of iteration steps to approximate Jacobian
                   (default: 18). Works only for `solver=`krylov`` and selected
                   `inner_methds` (`minres`, `gmres`)

               inner_method : str
                   Krylov method to use to approximate the Jacobian (default :
                   `minres`). One of `lgmres`, `gmres`, `bicgstab`, `cgs`,
                   `minres`, `tfqmr`.

                mix_maxiter : int
                    Maximum number of PBQN iteration steps if solver=`mix` is
                    selected. If mix_maxiter is larger than maxiter, mix_maxiter
                    is adjusted.

                mix_method : str
                    SciPy.optimize.root solver if solver=`mix` is selected.
                    This solver is chosen after mix_maxiter PBQN steps are
                    performed and the optimization did not converge yet.

               external_file : str
                   Path to file with CC amplitudes from external source.

               threshold_r : float
                   Tolerance for residual vector (default: 1e-5).

               threshold_e : float
                   Tolerance for energy (default: 1e-6).

               diis : dictionary
                   Contains optimization parameters for DIIS used in the PBQN
                   solver, one of:
                   * "diismax" - maximum number of DIIS vectors
                   * "diisreset" -  if true deletes selected DIIS vectors
                   * "diisstart" -  first iteration of DIIS procedure

               diis_l : dictionary
                   Contains optimization parameters for DIIS used in the PBQN
                   solver for the Lambda equations, one of:
                   * "diismax" - maximum number of DIIS vectors
                   * "diisreset" -  if true deletes selected DIIS vectors
                   * "diisstart" -  first iteration of DIIS procedure

               dump_cache :  dump effective Hamiltonian to disk if not needed
                   (default True if nact > CACHE_THR). Only arrays that are
                   at least of size o^2v^2 are dumped. Thus, the keyword
                   has no effect if the CC model in question does not
                   feature any arrays of size o^2v^2 or larger. In each
                   iteration step, these arrays are read from disk and
                   deleted from memory afterward.

        """
        supported_kwargs = [
            "filename",
            "e_ref",
            "geminal",
            "initguess",
            "maxiter",
            "solver",
            "external_file",
            "threshold_r",
            "threshold_e",
            "restart",
            "jacobian",
            "diis",
            "diis_l",
            "tco",
            "lambda_equations",
            "dump_cache",
            "inner_maxiter",
            "inner_method",
            "mix_maxiter",
            "mix_method",
        ]
        for kwarg in kwargs:
            if kwarg not in supported_kwargs:
                raise ArgumentError(f"Keyword {kwarg} not recognized.")
        ham_1, ham_2, orb = self.read_input(*args, **kwargs)
        self.print_info()
        # backup solver information
        solver = self.solver
        #
        # First, generate effective Hamiltonian as we need it to construct
        # an MP2 guess.
        #
        self.set_hamiltonian(ham_1, ham_2, orb)
        #
        # Solve for the CC amplitudes
        #
        self._time = time.time()
        solution = self.compute_amplitudes()

        self.amplitudes = self.unravel(solution.x)
        del solution
        gc.collect()
        #
        # Dump solution
        #
        self.dump_checkpoint(**self.amplitudes)
        #
        # Solve for Lambda equations (only supported for some CC models)
        #
        if self.lambda_equations:
            # reset solver (mix options overwrites attribute)
            self.solver = solver
            if log.do_medium:
                log.hline("~")
                log.hline(" ")
                log("Solving Lambda equations")
                log.hline(" ")
                log.hline("~")
            solution = self.compute_lambdas()
            self.l_amplitudes = self.unravel(solution.x)
            del solution
            gc.collect()
            #
            # Update DMs
            #
            self.set_dm(*args)
            #
            # Dump solution
            #
            self.dump_checkpoint(**self.amplitudes, **self.l_amplitudes)
        energy = self.calculate_energy(self.e_ref)
        self.energy = energy
        #
        # Clear Hamiltonian instance
        #
        self.clear_cache()
        gc.collect()
        #
        # Print final information
        #
        self.print_energy()
        self.print_amplitudes()
        #
        # Load ERI
        #
        ham_2.load_array(ham_2.label)
        #
        # Update output IOData container to contain also orbitals and overlap
        # as they are required by other modules.
        #
        olp = unmask("olp", *args, **kwargs)
        output = {
            **self.energy,
            **self.iodata,
            "orb_a": orb,
            **self.amplitudes,
        }
        if olp:
            output.update({"olp": olp})
        if self.lambda_equations:
            output.update(**self.l_amplitudes)
        #
        # Dump final solution to disk
        #
        self.dump_checkpoint(**output)
        return IOData(**output)

    @property
    @abstractmethod
    def amplitudes(self):
        """Dictionary of amplitudes."""

    @property
    @abstractmethod
    def l_amplitudes(self):
        """Dictionary of Lambda amplitudes."""

    def callback_t(self, amplitudes, residual):
        """Inform about current status of optimization process.

        Arguments:
           amplitudes : numpy.ndarray
               current solution for amplitudes (vectorized)

           residual : numpy.ndarray
               vector of residuals
        """
        amplitudes_dict = self.unravel(amplitudes)
        old_energy = self.energy
        new_energy = self.calculate_energy(
            self.e_ref, skip_seniority=True, **amplitudes_dict
        )
        time_ = time.time() - self._time
        self._iter += 1

        res = np.linalg.norm(residual)
        res_max = np.max(np.absolute(residual))
        diff = old_energy["e_tot"] - new_energy["e_tot"]
        if log.do_medium:
            log(
                f"{self._iter:6} {new_energy['e_tot']:16.10f} {diff:11.2e} "
                f"{new_energy['e_corr']:15.10f} {res:>11.2e} {res_max:>16.2e} "
                f"{time_:>16.4f}"
            )

        self.energy = new_energy
        self._time = time.time()
        self.dump_checkpoint(**amplitudes_dict)
        # explicitly delete elements as we do not want to store them during
        # runtime
        for _, v in amplitudes_dict.items():
            v.__del__()

    def compute_amplitudes(self, amplitudes=None):
        """Solve matrix equation using scipy.optimize.root routine."""
        solution = self.select_solver(amplitudes)

        if solution.success:
            if log.do_medium:
                log(" ")
                log(f"Amplitudes converged in {solution.nit-2} iterations.")
            self.converged = True
        else:
            log(" ")
            log.warn("Program terminated. Amplitudes did not converge.")
        log(" ")
        return solution

    def select_solver(self, amplitudes, select="t"):
        """Select either one of scipy.optimize.root or PyBEST internal routines

        Args:
            amplitudes (OneIndex, np.ndarray, None): some initial amplitudes
            select (str, optional): Choose between CC T (t) and Lambda (l)
                                    equations. Defaults to "t".

        Returns:
            solution: result of optimization generated in solver function
        """
        #
        # PyBEST internal solvers
        #
        if amplitudes is None:
            amplitudes = self.generate_guess(select=select)

        if self.solver in ["mix"]:
            return self.select_mix(amplitudes, select=select)

        if self.solver in ["pbqn"]:
            return self.select_pbqn(amplitudes, select=select)

        return self.select_scipy(amplitudes, select=select)

    def select_scipy(self, amplitudes, select="t"):
        """Use some SciPy solver defined in self.solver.

        Args:
            amplitudes (NIndexObject): The guess amplitudes passed to the SciPy solver

            select (str): Either ``t`` or ``l`` to choose vector function for
                          either CC amplitudes or Lambda equations

        Returns:
            OptimizeResult: The solution of SciPy.root (an OptimizeResult object)
        """
        #
        # SciPy solvers
        # NOTE: the `tol`` parameter does not work properly; `fatol` is set
        # instead. Solvers that do not support this option will print a warning
        print_e = f"{'Total energy':>16} {'Diff':>11} {'Corr. energy':>15}"
        print_e = print_e if select == "t" else ""
        log(
            f"\n{'Iter':>6} {print_e} {'|Residual|':>11s} "
            f"{'max(Residual)':>16s} {'Time':>12}"
        )
        maxiter = "maxfev" if self.solver == "df-sane" else "maxiter"
        # use specific solver options for large systems to prevent memory blowup
        jac_options = {}
        inner_maxiter = self.solver_parameters["inner_maxiter"]
        inner_method = self.solver_parameters["inner_method"]
        if self.solver == "krylov":
            jac_options = {
                "inner_maxiter": inner_maxiter,
                "method": inner_method,
            }
        callback = self.callback_t if select == "t" else self.callback_l
        options = {
            "callback": callback,
            "method": self.solver,
            # "tol": self.threshold_r,
            "options": {
                maxiter: self.maxiter,
                "fatol": self.threshold_r,
                "jac_options": jac_options,
            },
        }

        v_function = self.vfunction if select == "t" else self.vfunction_l
        return opt.root(v_function, self.ravel(amplitudes), **options)

    def select_pbqn(self, amplitudes, **kwargs):
        """Use perturbation-based quasi-Newton solver.

        Args:
            amplitudes (NIndexObject): The guess amplitudes passed to the SciPy solver

            select (str): Either ``t`` or ``l`` to choose vector function for
                          either CC amplitudes or Lambda equations

        Returns:
            IOData: container containing the result
        """
        maxiter = kwargs.get("maxiter", self.maxiter)
        threshold_e = kwargs.get("threshold_e", self.threshold_e)
        threshold_r = kwargs.get("threshold_r", self.threshold_r)
        select = kwargs.get("select", "t")
        #
        # Assign guess amplitudes (required for first iteration) and define
        # options
        #
        if select == "t":
            self.amplitudes = amplitudes
            diis = self.diis
        else:
            self.l_amplitudes = amplitudes
            diis = self.diis_l
        options = {
            "ethreshold": threshold_e,
            "tthreshold": threshold_r,
            "maxiter": maxiter,
            "select": select,
        }
        #
        # Call solver
        #
        qn = PBQuasiNewton(self.lf, **options)
        return qn(self, self.ravel(amplitudes), **diis)

    def select_mix(self, amplitudes, select="t"):
        """Use mixture of perturbation-based quasi-Newton solver and SciPy.
        The first `mix_maxiter` iterations are performed with PBQN, then we
        converge using the `mix_method` solver.

        Returns:
            IOData: container containing the result
        """
        #
        # Start with PBQN solver
        #
        self.solver = "pbqn"
        # Reset mix_maxiter if mix_maxiter > maxiter
        mix_maxiter = self.solver_parameters["mix_maxiter"]
        mix_maxiter = (
            self.maxiter if self.maxiter - 1 < mix_maxiter else mix_maxiter
        )
        solution_pbqn = self.select_pbqn(
            amplitudes, maxiter=mix_maxiter, select=select
        )

        if solution_pbqn.success:
            return solution_pbqn
        if self._iter >= self.maxiter - 1:
            log.warn("Maximum number of iterations reached!")
            return solution_pbqn
        #
        # Switching to SciPy solver defined in `mix_method`
        #
        inner_maxiter = self.solver_parameters["inner_maxiter"]
        inner_method = self.solver_parameters["inner_method"]
        self.solver = self.solver_parameters["mix_method"]
        guess = self.unravel(solution_pbqn.x)
        del solution_pbqn
        log(f"    Switching to {self.solver} solver:")
        if self.solver in ["krylov"]:
            log(f"        inner maxiter: {inner_maxiter}")
            log(f"        inner method:  {inner_method}")
        solution_scipy = self.select_scipy(guess, select=select)
        return solution_scipy

    def callback_l(self, amplitudes, residual):
        """Inform about current status of optimization process.

        Arguments:
           amplitudes : numpy.ndarray
               current solution for amplitudes (vectorized)

           residual : numpy.ndarray
               vector of residuals
        """
        l_amplitudes_dict = self.unravel(amplitudes)
        time_ = time.time() - self._time
        self._iter_l += 1

        res = np.linalg.norm(residual)
        res_max = np.max(np.absolute(residual))
        if log.do_medium:
            log(
                f"{self._iter_l:6} {res:>11.2e} {res_max:>16.2e} {time_:>16.4f}"
            )

        self._time = time.time()
        self.dump_checkpoint(**l_amplitudes_dict)
        # explicitly delete elements as we do not want to store them during
        # runtime
        for _, v in l_amplitudes_dict.items():
            v.__del__()

    def compute_lambdas(self, amplitudes=None):
        """Solve matrix equation using scipy.optimize.root routine."""
        available = ["mp2", "constant", "random"]
        if amplitudes is None and self.initguess in available:
            amplitudes = copy.deepcopy(self.amplitudes)
        solution = self.select_solver(amplitudes, select="l")

        if solution.success:
            if log.do_medium:
                log(" ")
                log(
                    f"Lambda equations converged in {solution.nit-2} iterations."
                )
            self.converged_l = True
        else:
            log(" ")
            log.warn("Program terminated. Lambda equations did not converge.")
        log(" ")
        log.hline("~")
        return solution

    def dump_checkpoint(self, **kwargs):
        """Save data (amplitudes, energies) to disk."""
        data = CheckPoint({**self.energy, **self.iodata, **kwargs})
        if self.lambda_equations and self.iter_l > 0:
            for k, v in self.amplitudes.items():
                data.update(k, v)
        data.to_file(self.filename)

    @property
    def iodata(self):
        """Container for output data"""
        return {
            "method": self.long_name,
            "nocc": self.nocc,
            "nvirt": self.nvirt,
            "nact": self.nact,
            "nacto": self.nacto,
            "nactv": self.nactv,
            "ncore": self.ncore,
            "occ_model": self.occ_model,
            "converged": self.converged,
        }

    @abstractmethod
    def print_amplitudes(self, threshold=1e-4, limit=None):
        """Prints highest amplitudes."""

    def print_info(self):
        """Print information about model."""
        tco = "optimal" if self.tco is None else self.tco

        log(" ")
        log(" ")
        log.hline("=")
        log(" ")
        log("RCC module")
        log(" ")
        log.hline()
        log("PARAMETERS")
        log(f"{'Wave function model':30} {self.acronym}")
        log(f"{'Full name of model':30} {self.long_name}")
        log(f"{'Cluster operator':30} {self.cluster_operator}")
        log(f"{'Total number of electrons':30} {2*self.nocc}")
        log(f"{'Total number of electron pairs':30} {self.nocc}")
        log(f"{'Total number of orbitals':30} {self.nocc + self.nvirt}")
        log(f"{'Number of active orbitals':30} {self.nact}")
        log(f"{'Number of core orbitals':30} {self.ncore}")
        log(f"{'Number of active occupied':30} {self.nacto}")
        log(f"{'Number of active virtual':30} {self.nvirt}")
        log(f"{'Initial guess':30} {self.initguess}")
        log(f"{'Solver:':30} {self.solver}")
        if self.solver in ["krylov"]:
            maxiter = self.solver_parameters["inner_maxiter"]
            method = self.solver_parameters["inner_method"]
            log(f"{'     inner_maxiter':30} {maxiter}")
            log(f"{'     Jacobian method':30} {method}")
        if self.solver in ["pbqn"]:
            log(f"{'     Jacobian method':30} {self.jacobian_approximation}")
        if self.solver in ["mix"]:
            maxiter = self.solver_parameters["inner_maxiter"]
            method = self.solver_parameters["inner_method"]
            mix_method = self.solver_parameters["mix_method"]
            mix_maxiter = self.solver_parameters["mix_maxiter"]
            log(f"{'     1st method':30} PBQN")
            log(f"{'     2nd method':30} {mix_method}")
            log(f"{'     1st maxiter':30} {mix_maxiter}")
            log(f"{'     Jacobian method 1':30} {self.jacobian_approximation}")
            log(f"{'     2nd method':30} {method}")
            log(f"{'     inner_maxiter':30} {maxiter}")
        log("Optimization thresholds:")
        log(f"{'     energy threshold':30} {self.threshold_e}")
        log(f"{'     residual threshold':30} {self.threshold_r}")
        log(f"{'Maximum number of iterations':30} {self.maxiter}")
        log(f"{'Tensor contraction engine':30} {tco}")
        log.hline(".")

    def read_input(self, *args, **kwargs):
        """Identifies OneBodyHamiltonian and TwoBodyHamiltonian terms and
        orbitals (DenseOrbital instance).
        """
        # Obligatory arguments
        orb = unmask_orb(*args)[0]
        one = self.lf.create_two_index(label="one")

        for label in OneBodyHamiltonian:
            one_body_term = unmask(label, *args, **kwargs)
            if isinstance(one_body_term, TwoIndex):
                one.iadd(one_body_term)
        for label in TwoBodyHamiltonian:
            eri = unmask(label, *args, **kwargs)
            if eri is not None:
                break

        if orb is None:
            raise ArgumentError("Orbitals or AO/MO coefficients not found.")
        if eri is None:
            raise ArgumentError("Electron repulsion integrals not found.")

        # Check if ERI should be read from file
        if not hasattr(eri, "_array"):
            eri.load_array(eri.label)

        # Saving options
        self.filename = kwargs.get("filename", self.filename)

        # Other options
        self.maxiter = kwargs.get("maxiter", self.maxiter) + 1
        self.solver = kwargs.get("solver", self.solver)
        self.threshold_r = kwargs.get("threshold_r", self.threshold_r)
        self.threshold_e = kwargs.get("threshold_e", self.threshold_e)
        self.initguess = kwargs.get("initguess", "mp2")
        if self.initguess == "mp2":
            self.initguess = kwargs.get("restart", "mp2")
        # Solver-specific options
        inner_maxiter = kwargs.get("inner_maxiter", 18)
        inner_method = kwargs.get("inner_method", "lgmres")
        mix_maxiter = kwargs.get("mix_maxiter", 20)
        mix_method = kwargs.get("mix_method", "krylov")
        self.solver_parameters = {
            "inner_maxiter": inner_maxiter,
            "inner_method": inner_method,
            "mix_maxiter": mix_maxiter,
            "mix_method": mix_method,
        }
        # DIIS for T equations
        diis = kwargs.get("diis", {})
        diis.setdefault("diismax", 2)
        diis.setdefault("diisstart", 0)
        diis.setdefault("diisreset", False)
        self.diis = diis
        # DIIS for Lambda equations
        diis_l = kwargs.get("diis_l", {})
        diis_l.setdefault("diismax", 2)
        diis_l.setdefault("diisstart", 0)
        diis_l.setdefault("diisreset", False)
        self.diis_l = diis_l
        self.jacobian_approximation = kwargs.get("jacobian", 1)
        self.lambda_equations = kwargs.get("lambda_equations", False)
        # Dump all intermediates to disk if number of active orbitals is
        # greater than CACHE_THR defined in constants.py
        self.dump_cache = kwargs.get(
            "dump_cache", (self.occ_model.nact[0] > CACHE_THR)
        )

        # Reference determinant energy and core energy
        self.e_ref = unmask("e_ref", *args, **kwargs)
        if self.e_ref is None:
            self.e_ref = kwargs.get("e_ref", 0.0)
        self.e_core = unmask("e_core", *args, **kwargs)
        if self.e_core is None:
            self.e_core = kwargs.get("e_core", 0.0)
        return one, eri, orb

    def transform_integrals(self, ham_1_ao, ham_2_ao, mos):
        """Saves Hamiltonian terms in cache.

        Arguments:
        one_body_ham : DenseTwoIndex
            Sum of one-body elements of the electronic Hamiltonian in AO
            basis, e.g. kinetic energy, nuclei--electron attraction energy

        two_body_ham : DenseFourIndex
            Sum of two-body elements of the electronic Hamiltonian in AO
            basis, e.g. electron repulsion integrals.

        mos : DenseOrbital
            Molecular orbitals, e.g. RHF orbitals or pCCD orbitals.
        """
        nbasis = self.nacto + self.nactv
        if ham_1_ao.shape != (nbasis, nbasis) or self.ncore != 0:
            ints = split_core_active(
                ham_1_ao, ham_2_ao, mos, e_core=self.e_core, ncore=self.ncore
            )
            self.e_core = ints.e_core
            ham_1 = ints.one
            ham_2 = ints.two
        else:
            ints = transform_integrals(ham_1_ao, ham_2_ao, mos)
            ham_1 = ints.one[0]
            ham_2 = ints.two[0]
        return ham_1, ham_2

    ###########################################################################
    # Energy
    ###########################################################################

    @property
    def energy(self):
        """Dictionary containing energies"""
        return self._energy

    @energy.setter
    def energy(self, energy_dict):
        self._energy.update(energy_dict)

    @energy.deleter
    def energy(self):
        self._energy = {}

    @abstractmethod
    def calculate_energy(self, e_ref, e_core=0.0, **amplitudes):
        """Computes coupled-cluster energy."""

    def print_energy(self):
        """Prints energy terms."""
        if log.do_medium:
            log.hline("-")
            log(f"{self.acronym} energy")
            log(f"{'Total energy':21} {self.energy['e_tot']:16.8f} a.u.")
            log(f"{'Reference determinant'} {self.energy['e_ref']:16.8f} a.u.")
            log(f"{'Correlation energy':22}{self.energy['e_corr']:16.8f} a.u.")
            self.print_energy_details()
            log.hline("-")
            log(" ")

    @abstractmethod
    def print_energy_details(self):
        """Prints contributions to energy for a specific model."""

    ###########################################################################
    # Initial guess
    ###########################################################################

    def generate_guess(self, **kwargs):
        """Generate the initial guess for CC amplitudes

        Keyword arguments:
            orbital : DenseOrbital
                Expansion coefficients (required for mp2 guess)

            ao1 : DenseTwoIndex
                One-body Hamiltonian in AO basis (required for mp2 guess)

            ao2 : DenseFourIndex or CholeskyFourIndex
                Two-body Hamiltonian in AO basis (required for mp2 guess)

            constant : float
                (optional for constant guess)

            select : str
                (optional to select t or l amplitudes)

        Returns a tuple with some t_1 and t_2 amplitudes.

        """
        if isinstance(self.initguess, IOData):
            select = kwargs.get("select", "t")
            guess = self.get_amplitudes_from_iodata(self.initguess, select)

        elif isinstance(self.initguess, dict):
            select = kwargs.get("select", "t")
            guess = self.get_amplitudes_from_dict(self.initguess, select)

        elif pathlib.Path(self.initguess).is_file():
            select = kwargs.get("select", "t")
            guess = self.read_guess_from_file(select)

        elif self.initguess == "mp2":
            guess = self.generate_mp2_guess()

        elif self.initguess == "random":
            guess = self.generate_random_guess()

        elif self.initguess == "constant":
            constant = kwargs.get("constant", 0.0625)
            guess = self.generate_constant_guess(constant)

        return guess

    @abstractmethod
    def generate_constant_guess(self, constant):
        """Generates NIndex objects filled by one value."""

    @abstractmethod
    def generate_mp2_guess(self):
        """Generates amplitudes from MP2 calculations."""

    @abstractmethod
    def generate_random_guess(self):
        """Generates NIndex objects filled with random values."""

    @abstractmethod
    def read_guess_from_file(self):
        """Reads NIndex objects from file."""

    @abstractmethod
    def get_amplitudes_from_iodata(self, iodata):
        """Reads NIndex objects from IOData instance."""

    @abstractmethod
    def get_amplitudes_from_dict(self, dictionary):
        """Reads NIndex objects from dictionary."""

    def get_range(self, string, offset=0):
        """Returns dictionary with keys beginX, endX, begin(X+1), etc.

        Arguments:
            string : string
                any sequence of "o" (occupied) and "v" (virtual)

        Keyword arguments:
            offset : int
                keys in returned dictionary start from offset value.
        """
        ranges = {}
        for ind, char in enumerate(string):
            if char == "o":
                ranges[f"begin{(ind + offset)}"] = 0
                ranges[f"end{(ind + offset)}"] = self.nacto
            elif char == "v":
                ranges[f"begin{(ind + offset)}"] = self.nacto
                ranges[f"end{(ind + offset)}"] = self.nacto + self.nactv
            elif char == "V":
                ranges[f"begin{(ind + offset)}"] = 0
                ranges[f"end{(ind + offset)}"] = self.nactv
            else:
                pass
        return ranges

    def get_size(self, string):
        """Returns list of arguments containing sizes of tensors

        **Arguments:**

        string : string or int
            any sequence of "o" (occupied) and "v" (virtual) OR a tuple of
            integers indicating the sizes of an array
        """
        args = []
        for char in string:
            if char == "o":
                args.append(self.nacto)
            elif char == "v":
                args.append(self.nactv)
            elif isinstance(char, int):
                args.append(char)
            else:
                raise ArgumentError(f"Do not know how to handle size {char}.")
        return tuple(args)

    ###########################################################################
    # Matrix operations
    ###########################################################################

    def set_seniority_0(self, matrix, value=0.0):
        """Set all seniority 0 t_2 amplitudes to some value.
        matrix - DenseFourIndex object
        """
        ind1, ind2 = np.indices((self.nacto, self.nactv))
        indices = [ind1, ind2, ind1, ind2]
        matrix.assign(value, indices)
        return matrix

    def set_seniority_2(self, matrix, value=0.0):
        """Set all seniority 2 t_2 amplitudes to some value.
        matrix - DenseFourIndex object
        """
        # Get seniority 0 sector
        seniority_0 = self.lf.create_two_index(self.nacto, self.nactv)
        matrix.contract("abab->ab", clear=True, out=seniority_0)
        # Assign seniority 0 and 2
        ind1, ind2, ind3 = np.indices((self.nacto, self.nactv, self.nactv))
        indices = [ind1, ind2, ind1, ind3]
        matrix.assign(value, ind=indices)
        ind1, ind2, ind3 = np.indices((self.nacto, self.nacto, self.nactv))
        indices = [ind1, ind3, ind2, ind3]
        matrix.assign(value, ind=indices)
        # Reassign old values to seniority 0 sector
        matrix = self.set_seniority_0(matrix)
        matrix.iadd_expand_two_to_four("diag", seniority_0)
        return matrix

    ###########################################################################
    # Cache operations
    ###########################################################################

    def from_cache(self, select):
        """Get a matrix/tensor from the cache.

        **Arguments:**

        select
            (str) some object stored in the Cache.
        """
        return self.cache.load(select)

    def init_cache(self, select, *args, **kwargs):
        """Initialize some cache instance

        **Arguments:**

        select

            (str) label of the auxiliary tensor

        args
            The size of the auxiliary matrix in each dimension. The number of given
            arguments determines the order and sizes of the tensor.
            Either a tuple or a string (oo, vv, ovov, etc.) indicating the sizes.
            Not required if ``alloc`` is specified.

        **Keyword Arguments:**

        tags
            The tag used for storing some matrix/tensor in the Cache (default
            `h`).

        alloc
            Specify alloc function explicitly. If not defined some flavor of
            `self.lf.create_N_index` is taken depending on the length of args.

        nvec
            Number of Cholesky vectors. Only required if Cholesky-decomposed ERI
            are used. In this case, only ``args[0]`` is required as the Cholesky
            class does not support different sizes of the arrays.
        """
        for name, _ in kwargs.items():
            check_options(name, name, "tags", "nvec", "alloc")
        tags = kwargs.get("tags", "h")
        nvec = kwargs.get("nvec", None)
        alloc = kwargs.get("alloc", None)
        # resolve args: either pass dimensions or string indicating dimensions
        args = self.get_size(args)

        if len(args) == 0 and not alloc:
            raise ArgumentError(
                "At least one dimension or a user-defined allocation function "
                "have to be specified"
            )
        if alloc:
            pass
        elif nvec is not None:
            alloc = (self.lf.create_four_index, args[0], nvec)
        elif len(args) == 1:
            alloc = (self.lf.create_one_index, *args)
        elif len(args) == 2:
            alloc = (self.lf.create_two_index, *args)
        elif len(args) == 3:
            alloc = (self.lf.create_three_index, *args)
        else:
            alloc = (self.denself.create_four_index, *args)
        # load into the cache
        matrix, new = self.cache.load(select, alloc=alloc, tags=tags)
        if not new:
            raise NonEmptyData(
                f"The Cache instance {select} already exists. "
                "Call clear prior to updating the Cache instance."
            )

        return matrix

    def clear_cache(self, **kwargs):
        """Clear the Cache instance

        **Keyword arguments:**

        tags
             The tag used for storing some matrix/tensor in the Cache (default
             `h`).
        """
        for name in kwargs:
            check_options(name, name, "tags")
        tags = kwargs.get("tags", "h")

        self.cache.clear(tags=tags, dealloc=True)

    ###########################################################################
    # Vector-function
    ###########################################################################

    @abstractmethod
    def cc_residual_vector(self, amplitudes):
        """Residual vector for CC amplitude equations."""

    @abstractmethod
    def vfunction(self, vector):
        """Vectorized CC residual vector."""

    @abstractmethod
    def l_residual_vector(self, amplitudes):
        """Residual vector for Lambda amplitude equations."""

    @abstractmethod
    def vfunction_l(self, vector):
        """Vectorized Lambda residual vector."""

    @abstractmethod
    def ravel(self, amplitudes):
        """Flattens NIndex objects."""

    @abstractmethod
    def unravel(self, vector):
        """Expands vector."""

    @abstractmethod
    def jacobian(self, amplitudes, *args):
        """Some Jacobian approximation used in the PBQN solver"""
