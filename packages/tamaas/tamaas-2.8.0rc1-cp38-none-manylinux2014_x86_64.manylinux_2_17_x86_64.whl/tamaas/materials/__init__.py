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

"""Defines material classes"""

from .._tamaas import Model
from .._tamaas._materials import Material

import numpy as np


try:
    import mgis.behaviour as mgis_bv

    class MFrontMaterial(Material):
        """MFront bridge class for materials

        MFront is a code-generation tool for material constitutive laws. This
        class uses the Python bindings of the MFront Generic Interface Support
        (MGIS).

        """
        def __init__(self, model: Model,
                     behaviour: mgis_bv.Behaviour,
                     dt: float = 1.,
                     **kwargs):
            super().__init__(model)
            self.model = model
            self.behaviour = behaviour

            # Sanity checks on behaviours
            assert "Strain" in (g.name for g in behaviour.gradients)
            assert "Stress" in (f.name for f in behaviour.thermodynamic_forces)
            assert behaviour.btype == \
                mgis_bv.BehaviourType.StandardStrainBasedBehaviour
            assert behaviour.kinematic == \
                mgis_bv.BehaviourKinematic.SmallStrainKinematic
            assert behaviour.symmetry == mgis_bv.BehaviourSymmetry.Isotropic

            # Setting elastic properties
            if "YoungModulus" in behaviour.params:
                behaviour.setParameter("YoungModulus", model.E)
            if "PoissonRatio" in behaviour.params:
                behaviour.setParameter("PoissonRatio", model.nu)

            for k, v in kwargs.items():
                if k in behaviour.params:
                    behaviour.setParameter(k, v)

            # Number of integration points is the number of voxels
            # MGIS does not like numpy types
            N_integration = int(np.prod(model.shape))

            # Let MFront allocate the data
            # (in case of external storage, create an instance of
            # MaterialDataManagerInitializer and use bindGradients, etc.)
            self.manager = mgis_bv.MaterialDataManager(behaviour, N_integration)

            # For some reason we have to set a temperature
            mgis_bv.setExternalStateVariable(self.manager.s1, 'Temperature', 0)
            self.manager.update()  # propagates the changes to the s0 state

            # Total size of internal variables per integration point
            internal_size = mgis_bv.getArraySize(behaviour.isvs,
                                                 behaviour.hypothesis)

            # Create references to MFront arrays
            # Using MFront-allocated arrays to avoid duplicates
            model['stress'] = \
                self.manager.s1.thermodynamic_forces.reshape(model.shape + [6])
            model['strain'] = \
                self.manager.s1.gradients.reshape(model.shape + [6])
            model['mfront::internals'] = \
                self.manager.s1.internal_state_variables.reshape(
                    model.shape + [internal_size])

            # Timestep
            self.dt = dt

        def computeStress(self, stress, strain, strain_increment):
            """Make the MFront call to integrate to compute full stresses"""
            total_strain = strain + strain_increment

            # Gradient is the total strain
            self.manager.s1.gradients[:] = \
                total_strain.reshape(self.manager.s1.gradients.shape)

            # Integrate constitutive law
            mgis_bv.integrate(
                self.manager,
                mgis_bv.IntegrationType.IntegrationWithoutTangentOperator,
                self.dt, 0, int(np.prod(stress.shape[:-1]))
            )

            # Copy stresses over
            stress[:] = \
                self.manager.s1.thermodynamic_forces.reshape(stress.shape)

        def computeEigenStress(self, stress, strain, strain_increment):
            """Compute eigenstress from the full stress"""
            strain_increment = strain_increment.reshape(stress.shape)
            total_strain = strain + strain_increment

            # Compute stress as if behavior was linear elastic
            # (can probably call mfront for this)
            hooke_stress = np.zeros_like(stress)
            self.model.operators['hooke'](total_strain, hooke_stress)

            # Compute real stress
            self.computeStress(stress, strain, strain_increment)

            # Compute eigenstress of full plastic strain
            stress[:] = hooke_stress - stress

            self.model.operators['hooke'](strain, hooke_stress)
            prev_stress = \
                self.manager.s0.thermodynamic_forces.reshape(stress.shape)
            stress[:] = stress - (hooke_stress - prev_stress)

        def update(self):
            """Copy over state s1 -> s0"""
            self.manager.update()

        def internal_view(self, name):
            """Returns a view to a specific internal"""
            isvs = self.behaviour.isvs
            hyp = self.behaviour.hypothesis
            offset = mgis_bv.getVariableOffset(isvs, name, hyp)
            size = mgis_bv.getVariableSize(isvs, name, hyp)
            return self.model['mfront::internals'][..., offset:offset+size]

        def __repr__(self):
            behaviour = self.behaviour

            def desc(x):
                return ", ".join([f"{i.name}: {i.type}" for i in x])

            return f"""{behaviour.behaviour}
-- Parameters: {{ {', '.join(behaviour.parameters)} }}
-- Internal Variables: {{ {desc(behaviour.isvs)} }}
-- External Variables: {{ {desc(behaviour.esvs)} }}
-- Thermodyn. Forces: {{ {desc(behaviour.thermodynamic_forces)} }}
-- Gradients: {{ {desc(behaviour.gradients)} }}"""

except ImportError:
    pass


del Model

from .._tamaas._materials import *  # noqa
