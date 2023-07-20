# This is the file where the placed element revetment type is calculated.
# Splitup into two classes: Basalton and Verkalit.

import numpy as np
import openturns as ot
import time
import openturns.viewer as viewer
from matplotlib import pylab as plt
from Input.Parameters_Class import ElementInput

ot.Log.Show(ot.Log.NONE)


class BasaltonFunc:
    distribution_elements = ElementInput.distributionelements

    def basalton(self):
        deterministic_elements = ElementInput.deterministicelements
        rho_c = self[0]
        rho_w = self[1]
        d_b = self[2]
        d_v = self[3]
        a2 = self[4]
        t = self[5]
        Hs = deterministic_elements[0]
        h = deterministic_elements[1]
        B = deterministic_elements[2]
        c1 = deterministic_elements[3]
        c2 = deterministic_elements[4]
        gamma_s = deterministic_elements[5]
        b1 = deterministic_elements[6]
        k2 = deterministic_elements[7]
        b2 = deterministic_elements[8]
        v_kin = deterministic_elements[9]
        n_f = deterministic_elements[10]
        D_f15 = deterministic_elements[11]
        g = deterministic_elements[12]
        Tp = deterministic_elements[13]
        Zb = deterministic_elements[14]
        L = deterministic_elements[15]

        P_Zb = np.maximum(1.06 * (np.maximum((Zb - h) / Hs, -0.3) + 0.3) ** 0.125,
                          5 * (np.minimum((Zb - h) / Hs, -0.2)) ** 4 + 0.9)
        P_tana = 0.54 * (np.tan(a2)) ** -0.49
        a_f = 160 * (v_kin * (1 - n_f) ** 2) / (g * n_f ** 3 * D_f15 ** 2)
        b_f = 2.2 / (g * n_f ** 3 * D_f15)
        k1 = (-a_f + np.sqrt(a_f ** 2 + 1.2 * b_f)) / (0.6 * b_f)
        k = 0.05  ## Moet nog worden toegevoegd
        Lambda = np.maximum(np.sqrt((d_b * (b1 * k1 + b2 * k2)) / k), 0.5 * d_b)
        P_Lambda = 0.42 * (Lambda / d_b) ** -2.4 + 0.81
        P_Delta = 0.25 * ((rho_c - rho_w) / rho_w - 1.7) ** 2 + 0.98

        P_N = np.maximum(3.1 * (t / Tp) ** -0.141, 0.8)

        P_B = 5.5 * 10 ** -22 * (B + 90) ** 9.5 + 1

        S_op = Hs / L

        P_Sop = np.maximum(0.032 * (S_op + 0.3) ** -3, 1.66 * (S_op + 0.3) ** 0.47)

        P_D = 1 / (0.054 * d_b ** -1.3 + 0.79)

        fs_front = np.maximum(1 - c1 * np.log(t / (Tp / 1.1)), c2)

        Irr = np.tan(a2) / (np.sqrt(Hs / L))

        MAX_stab = (7 * (np.minimum(Irr, 2)) ** -(1 / 3) + np.maximum(0.5 * (np.minimum(Irr, 5) - 2), 0)) / (
            np.maximum(((np.cos(B)) ** (2 / 3)), 0.4)) * fs_front

        Z_basalton = [np.minimum(4.93 * P_Zb * P_tana * P_Lambda * P_Delta * P_N * P_B * P_Sop * P_D, MAX_stab) - Hs / (
                    ((rho_c - rho_w) / rho_w) * d_b)]

        return Z_basalton

    basalton_failure_model = ot.PythonFunction(6, 1, basalton)

    vector = ot.RandomVector(distribution_elements)
    Z_basalton = ot.CompositeRandomVector(basalton_failure_model, vector)
    basalton_event = ot.ThresholdEvent(Z_basalton, ot.Less(), 0.0)
    basalton_event.setName("Failure of asphalt for basalton")

    optimAlgo = ot.Cobyla()
    optimAlgo.setMaximumEvaluationNumber(100000)
    optimAlgo.setMaximumAbsoluteError(1.0e-10)
    optimAlgo.setMaximumRelativeError(1.0e-10)
    optimAlgo.setMaximumResidualError(1.0e-10)
    optimAlgo.setMaximumConstraintError(1.0e-10)

    # Run FORM
    basalton_startingPoint = distribution_elements.getMean()
    basalton_algo = ot.FORM(optimAlgo, basalton_event, basalton_startingPoint)
    basalton_algo.run()
    basalton_result = basalton_algo.getResult()
    standardSpaceDesignPoint = basalton_result.getStandardSpaceDesignPoint()

    # Retrieve results
    probability_basalton = basalton_result.getEventProbability()
    beta_basalton = basalton_result.getHasoferReliabilityIndex()
    # print(f"Pf basalton ={probability_basalton}, beta basalton = {beta_basalton}")
