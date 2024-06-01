# -*- mode:python; coding: utf-8 -*-
#
# Copyright (©) 2016-2024 EPFL (École Polytechnique Fédérale de Lausanne),
# Laboratory (LSMS - Laboratoire de Simulation en Mécanique des Solides)
# Copyright (©) 2020-2024 Lucas Frérot
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Nonlinear solvers for plasticity problems.

Solvers in this module use :py:mod:`scipy.optimize` to solve the implicit
non-linear equation for plastic deformations with fixed contact pressures.
"""
import numpy as np

from functools import wraps

from scipy.optimize import newton_krylov, root
from scipy.sparse.linalg import bicgstab, LinearOperator

from .._tamaas import (
    EPSolver,
    Logger,
    LogLevel,
    mpi,
    _tolerance_manager,
    _DFSANESolver as DFSANECXXSolver,
    TamaasInfo
)


__all__ = ['NLNoConvergence',
           'DFSANESolver',
           'DFSANECXXSolver',
           'NewtonKrylovSolver',
           'ToleranceManager']

if TamaasInfo.has_petsc:
    from .._tamaas import _PETScSolver as PETScSolver  # noqa
    __all__.append('PETScSolver')


class NLNoConvergence(RuntimeError):
    """Convergence not reached exception."""


class NewtonRaphsonSolver(EPSolver):
    """Basic Newton-Raphson scheme"""

    def __init__(self, residual):
        super(NewtonRaphsonSolver, self).__init__(residual)
        self._x = self.getStrainIncrement()
        self._residual = self.getResidual()
        self.max_iter = 1000

    def solve(self):
        EPSolver.beforeSolve(self)

        # assemble RHS
        self._residual.computeResidual(self._x)
        rhs = -self._residual.vector.ravel()

        norm_0 = np.linalg.norm(rhs) / rhs.size

        if norm_0 < self.tolerance:
            Logger().get(LogLevel.info) << (
                "NewtonRaphson: successful convergence (0 iterations,"
                f" {self.tolerance}, {norm_0})\n")
            self._residual.computeResidualDisplacement(self._x)
            return

        # define linear operator
        def residual_tangent(x):
            v = np.zeros_like(x)
            self._residual.applyTangent(v, x, self._x)
            return v.ravel()

        T = LinearOperator(matvec=residual_tangent, shape=[self._x.size] * 2)

        error = norm_0
        nit = 0

        while error > self.tolerance and nit < self.max_iter:
            self._residual.computeResidual(self._x)
            rhs = -self._residual.vector.ravel()
            x, error_code = bicgstab(T, rhs, atol=1e-10)
            self._x += x.reshape(self._x.shape)
            error = np.linalg.norm(rhs) / rhs.size
            nit += 1

        if error > self.tolerance:
            msg = "did not converge"
        else:
            msg = "successful convergence"

        Logger().get(LogLevel.info) << (
            f"NewtonRaphson: {msg} ({nit} iterations,"
            f" {self.tolerance}, {error:.3e})\n")

        self._residual.computeResidualDisplacement(self._x)


class ScipySolver(EPSolver):
    """Base class for solvers wrapping SciPy routines."""

    def __init__(self, residual, model=None, callback=None):
        """Construct nonlinear solver with residual.

        :param residual: plasticity residual object
        :param model: Deprecated
        :param callback: passed on to the Scipy solver
        """
        super(ScipySolver, self).__init__(residual)

        if mpi.size() > 1:
            raise RuntimeError("Scipy solvers cannot be used with MPI; "
                               "DFSANECXXSolver can be used instead")

        self.callback = callback
        self._x = self.getStrainIncrement()
        self._residual = self.getResidual()
        self.options = {'ftol': 0, 'fatol': 1e-9}

    def solve(self):
        """Solve R(δε) = 0 using a Scipy function."""
        # For initial guess, compute the strain due to boundary tractions
        # self._residual.computeResidual(self._x)
        # self._x[...] = self._residual.getVector()
        EPSolver.beforeSolve(self)

        # Scipy root callback
        def compute_residual(vec):
            self._residual.computeResidual(vec)
            return self._residual.vector.copy()

        # Solve
        Logger().get(LogLevel.debug) << \
            "Entering non-linear solve\n"
        self._x[...] = self._scipy_solve(compute_residual)
        Logger().get(LogLevel.debug) << \
            "Non-linear solve returned"

        # Computing displacements
        self._residual.computeResidualDisplacement(self._x)

    def reset(self):
        """Set solution vector to zero."""
        self._x[...] = 0

    def _scipy_solve(self, compute_residual):
        """Actually call the scipy solver.

        :param compute_residual: function returning residual for given variable
        """
        raise NotImplementedError()


class NewtonKrylovSolver(ScipySolver):
    """Solve using a finite-difference Newton-Krylov method."""

    def _scipy_solve(self, compute_residual):
        try:
            return newton_krylov(compute_residual, self._x,
                                 f_tol=self.tolerance,
                                 verbose=False, callback=self.callback)
        except Exception:
            raise NLNoConvergence("Newton-Krylov did not converge")


class DFSANESolver(ScipySolver):
    """Solve using a spectral residual jacobianless method.

    See :doi:`10.1090/S0025-5718-06-01840-0` for details on method and
    the relevant Scipy `documentation
    <https://scipy.github.io/devdocs/reference/optimize.root-dfsane.html>`_ for
    details on parameters.

    """

    def _scipy_solve(self, compute_residual):
        solution = root(compute_residual,
                        self._x,
                        method='df-sane',
                        options={'ftol': 0, 'fatol': self.tolerance},
                        callback=self.callback)
        Logger().get(LogLevel.info) << \
            "DF-SANE/Scipy: {} ({} iterations, {})".format(
                solution.message,
                solution.nit,
                self.tolerance)

        if not solution.success:
            raise NLNoConvergence("DF-SANE/Scipy did not converge")
        return solution.x.copy()


def ToleranceManager(start, end, rate):
    """Decorate solver to manage tolerance of non-linear solve step."""

    def actual_decorator(cls):
        orig_init = cls.__init__
        orig_solve = cls.solve
        orig_update_state = cls.updateState

        @wraps(cls.__init__)
        def __init__(obj, *args, **kwargs):
            orig_init(obj, *args, **kwargs)
            obj.setToleranceManager(_tolerance_manager(start, end, rate))

        @wraps(cls.solve)
        def new_solve(obj, *args, **kwargs):
            ftol = obj.tolerance
            ftol *= rate

            obj.tolerance = max(ftol, end)
            return orig_solve(obj, *args, **kwargs)

        @wraps(cls.updateState)
        def updateState(obj, *args, **kwargs):
            obj.tolerance = start
            return orig_update_state(obj, *args, **kwargs)

        cls.__init__ = __init__
        # cls.solve = new_solve
        # cls.updateState = updateState
        return cls

    return actual_decorator
