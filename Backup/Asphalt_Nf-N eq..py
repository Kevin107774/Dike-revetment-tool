# This is the file where Asphalt revetment is calculated.

import numpy as np
import openturns as ot
import time
import openturns.viewer as viewer
from matplotlib import pylab as plt
from Input.Parameters_Class import AsphaltUpliftInput
from Input.Parameters_Class import AsphaltImpactInput

ot.Log.Show(ot.Log.NONE)


class AsphaltFunc:

    def probasphalt(distribution, deterministic):

        distributionasphalt = distribution
        deterministicasphalt = deterministic

        if len(deterministicasphalt) == 4:
            def asphalt_uplift(self):
                d = self[0]
                rho_w = self[1]
                rho_a = self[2]
                Qn = deterministicasphalt[0]
                a = deterministicasphalt[1]
                v = deterministicasphalt[2]
                Rw = deterministicasphalt[3]

                Z = [0.21 * Qn * (a + v) * rho_w / (rho_a - rho_w) * Rw - d]

                return Z

            uplift_failure_model = ot.PythonFunction(3, 1, asphalt_uplift)

            vect = ot.RandomVector(distributionasphalt)
            Z = ot.CompositeRandomVector(uplift_failure_model, vect)
            event = ot.ThresholdEvent(Z, ot.Less(), 0.0)
            event.setName("Failure of asphalt for uplift")
            # print(event)

            # Using FORM, define a solver:
            optimAlgo = ot.Cobyla()
            optimAlgo.setMaximumEvaluationNumber(100000)
            optimAlgo.setMaximumAbsoluteError(1.0e-10)
            optimAlgo.setMaximumRelativeError(1.0e-10)
            optimAlgo.setMaximumResidualError(1.0e-10)
            optimAlgo.setMaximumConstraintError(1.0e-10)

            # Run FORM
            startingPoint = distributionasphalt.getMean()
            algo = ot.FORM(optimAlgo, event, startingPoint)
            algo.run()
            result = algo.getResult()
            standardSpaceDesignPoint = result.getStandardSpaceDesignPoint()

            # Retrieve results
            probability_uplift = result.getEventProbability()
            beta_uplift = result.getHasoferReliabilityIndex()
            # print(f"Pf uplift ={probability_uplift}, beta uplift = {beta_uplift}")
            return probability_uplift

        else:
            def asphalt_impact(self):
                a3 = self[0]
                q_r = self[1]
                rho_w = self[2]
                c = self[3]
                E = self[4]
                d = self[5]
                sigma_b = self[6]
                t = self[7]

                Hs = deterministicasphalt[0]
                g = deterministicasphalt[1]
                v = deterministicasphalt[2]
                alpha = deterministicasphalt[3]
                B = deterministicasphalt[4]
                Tp = deterministicasphalt[5]

                q = np.tan(a3) / q_r

                P_max = rho_w * g * q * Hs

                Beta = ((3 * c * (1 - v ** 2)) / (E * d ** 3)) ** (1 / 4)

                z = 1.3355 / Beta

                sigma = (P_max / (4 * (Beta ** 3) * z)) * (
                            1 - np.exp(-Beta * z) * ((np.cos(Beta * z)) + np.sin(Beta * z))) * (6 / d ** 2)

                Nf = 10 ** (B * (np.log(sigma_b) - np.log(sigma)) ** alpha)
                print(Nf)
                N = t / Tp

                Z_impact = [Nf - N]

                return Z_impact

            impact_failure_model = ot.PythonFunction(8, 1, asphalt_impact)

            vector = ot.RandomVector(distributionasphalt)
            Z_impact = ot.CompositeRandomVector(impact_failure_model, vector)
            impact_event = ot.ThresholdEvent(Z_impact, ot.Less(), 0.0)
            impact_event.setName("Failure of asphalt for impact")

            # Using FORM, define a solver:
            optimAlgo = ot.Cobyla()
            optimAlgo.setMaximumEvaluationNumber(100000)
            optimAlgo.setMaximumAbsoluteError(1.0e-10)
            optimAlgo.setMaximumRelativeError(1.0e-10)
            optimAlgo.setMaximumResidualError(1.0e-10)
            optimAlgo.setMaximumConstraintError(1.0e-10)

            # Run FORM
            impact_startingPoint = distributionasphalt.getMean()
            impact_algo = ot.FORM(optimAlgo, impact_event, impact_startingPoint)
            impact_algo.run()
            impact_result = impact_algo.getResult()
            standardSpaceDesignPoint = impact_result.getStandardSpaceDesignPoint()

            # Retrieve results
            probability_impact = impact_result.getEventProbability()
            beta_impact = impact_result.getHasoferReliabilityIndex()
            # print(f"Pf impact ={probability_impact}, beta impact = {beta_impact}")

            return probability_impact

    Pf_asphalt_uplift = []
    for i in AsphaltUpliftInput.distribution_uplift_asphalt:
        Pf_asphalt_uplift.append(probasphalt(i, AsphaltUpliftInput.deterministic_uplift_asphalt))

    Pf_asphalt_impact = []
    for j in AsphaltImpactInput.distribution_impact_asphalt:
        Pf_asphalt_impact.append(probasphalt(j, AsphaltImpactInput.deterministic_impact_asphalt))

    print(Pf_asphalt_uplift, Pf_asphalt_impact)
