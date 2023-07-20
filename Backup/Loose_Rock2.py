# This is the file where loose rock is being calculated according to the vd Meer Equations.
import numpy as np
import openturns as ot
import time
import openturns.viewer as viewer
from matplotlib import pylab as plt
from Input.Parameters_Class import VdMeerInput
from Input.Parameters import Parameters

ot.Log.Show(ot.Log.NONE)


class VdMeerFunc:

    distribution_matrix = np.zeros([len(VdMeerInput.distributionvdmeer2), len(VdMeerInput.deterministicvdmeer2)])

    for i, distvdmeer_i in enumerate(VdMeerInput.distributionvdmeer2):
        for j, deterministic_j in enumerate(VdMeerInput.deterministicvdmeer2):
            distribution_matrix[i, j] = [distvdmeer_i, deterministic_j]
            vdmeermodel(   )


    # for i in range(len(VdMeerInput.distributionvdmeer2)):
    #     distributionvdmeer = VdMeerInput.distributionvdmeer2[i]

    def vdmeermodel(vector):
        Dn50 = vector[0]
        rho_w = vector[1]
        rho_s = vector[2]
        P = vector[3]
        Cpl_a = vector[4]
        Cpl_b = vector[5]
        t = vector[6]
        a1 = vector[7]

        for j in range(len(VdMeerInput.deterministicvdmeer2)):
            deterministicvdmeer = VdMeerInput.deterministicvdmeer2[j]
            S = deterministicvdmeer[1]
            Hs = deterministicvdmeer[0]
            Tp = deterministicvdmeer[2]
            L = deterministicvdmeer[3]

            zeta = np.tan(a1) / (np.sqrt(Hs / L))

            if zeta <= 3:
                # Limit state function plunging waves:
                Z = [Cpl_a * P ** 0.18 * (S / np.sqrt(abs(t) / Tp)) ** 0.2 * (
                        np.tan(a1) / (np.sqrt(Hs / L))) ** -0.5 - Hs / (((rho_s - rho_w) / rho_w) * Dn50)]

            else:
                # Limit state function surging waves:
                Z = [Cpl_b * P ** -0.13 * (S / np.sqrt(abs(t) / Tp)) ** 0.2 * np.sqrt(1 / np.tan(a1)) * (
                        np.tan(a1) / (np.sqrt(Hs / L))) ** P - Hs / (((rho_s - rho_w) / rho_w) * Dn50)]
            return Z

        ot_failure_model = ot.PythonFunction(8, 1, vdmeermodel)

        vect = ot.RandomVector(distributionvdmeer)
        Z = ot.CompositeRandomVector(ot_failure_model, vect)
        event = ot.ThresholdEvent(Z, ot.Less(), 0.0)
        event.setName("Failure of rock diameter")

        # Using FORM, define a solver:
        optimAlgo = ot.Cobyla()
        optimAlgo.setMaximumEvaluationNumber(100000)
        optimAlgo.setMaximumAbsoluteError(1.0e-10)
        optimAlgo.setMaximumRelativeError(1.0e-10)
        optimAlgo.setMaximumResidualError(1.0e-10)
        optimAlgo.setMaximumConstraintError(1.0e-10)

        # Run FORM
        startingPoint = distributionvdmeer.getMean()
        algo = ot.FORM(optimAlgo, event, startingPoint)
        algo.run()
        result = algo.getResult()
        standardSpaceDesignPoint = result.getStandardSpaceDesignPoint()

        # Retrieve results
        probability = result.getEventProbability()
        beta = result.getHasoferReliabilityIndex()
        print(f"{distributionvdmeer}, Pf={probability}, beta = {beta}")
