# This is the file where the placed element revetment type is calculated.
# Splitup into two classes: Basalton and Verkalit.

import numpy as np
import openturns as ot
import time
import openturns.viewer as viewer
from matplotlib import pylab as plt
from Input.Parameters_Class import ElementInput
from scipy.optimize import fsolve

ot.Log.Show(ot.Log.NONE)


# class BasaltonFunc:
#
#     def probBasalton(distribution, deterministic, probabilistic='FORM'):
#         distribution_Basalton = distribution
#         deterministic_Basalton = deterministic

    #     def basalton(self):
    #         rho_c = self[5]
    #         d_b = self[6]
    #         rho_w = self[7]
    #         a = self[4]
    #         t = self[2]
    #         Hs = self[0]
    #         h = self[3]
    #         Tp = self[1]
    #         B = deterministic_Basalton[0]
    #         c1 = deterministic_Basalton[1]
    #         c2 = deterministic_Basalton[2]
    #         b1 = deterministic_Basalton[3]
    #         k2 = deterministic_Basalton[4]
    #         b2 = deterministic_Basalton[5]
    #         v_kin = deterministic_Basalton[6]
    #         n_f = deterministic_Basalton[7]
    #         D_f15 = deterministic_Basalton[8]
    #         g = deterministic_Basalton[9]
    #         Zb = deterministic_Basalton[10]
    #
    #         def Wavelength(g, Tp, h):
    #             c = [0.00011, 0.00039, 0.00171, 0.00654, 0.02174, 0.06320, 0.16084, 0.35550, 0.66667, 1]
    #             sg = (2 * np.pi) / Tp
    #             c0 = g / sg
    #             k0d = sg * (h + 0.4) / c0
    #             kd = np.sqrt(k0d * k0d + k0d / np.polyval(c, k0d))
    #             ar = k0d / kd
    #             sf = ar + kd * (1 - ar * ar)
    #             cf = c0 * ar
    #             l = cf * Tp
    #             cg = 0.5 * c0 * sf
    #             sf = 1 / np.sqrt(sf)  # shoaling factor
    #             return l, cf, cg, ar, sf
    #
    #         L = Wavelength(g, Tp, h)[0]
    #
    #         # If performing FORM analysis turn the breaker criterium off. Too discontinue
    #         H_sb = (0.095 * np.exp(4 * (1 / 33))) * L * np.tanh((2 * np.pi * (0.4 + h)) / L)
    #
    #         if H_sb < Hs:
    #             return [9999999999]
    #
    #         P_Zb = np.maximum(1.06 * (np.maximum((Zb - h) / Hs, -0.3) + 0.3) ** 0.125,
    #                           5 * (np.minimum((Zb - h) / Hs, -0.2)) ** 4 + 0.9)
    #
    #         P_tana = 0.54 * (np.tan(a)) ** -0.49
    #
    #         a_f = 160 * (v_kin * (1 - n_f) ** 2) / (g * n_f ** 3 * D_f15 ** 2)
    #
    #         b_f = 2.2 / (g * n_f ** 3 * D_f15)
    #
    #         k1 = (-a_f + np.sqrt(a_f ** 2 + 1.2 * b_f)) / (0.6 * b_f)
    #
    #         # omega = 0.13
    #         # s_s = -0.5 * (0.3 + 0.3) + np.sqrt(((omega * 0.3 * 0.3) / (1 - omega)) + 0.25 * (0.3 + 0.3)**2)
    #         # s = s_s + 0.3 * 10**-3
    #         # A_ro = s / (0.3 + s)
    #         #
    #         # a_s = (12 * v_kin) / (g * s**2 * A_ro)
    #
    #         # Lambda = np.maximum(np.sqrt((d_b * (b1 * k1 + b2 * k2)) / k))
    #         Lambda = 0.38
    #
    #         P_Lambda = 0.42 * (Lambda / d_b) ** -2.4 + 0.81
    #
    #         P_Delta = 0.25 * ((rho_c - rho_w) / rho_w - 1.7) ** 2 + 0.98
    #
    #         P_N = np.maximum(3.1 * (t / (Tp / 1.2)) ** -0.141, 0.8)
    #
    #         P_B = 5.5 * 10 ** -22 * (B + 90) ** 9.5 + 1
    #
    #         S_op = Hs / L
    #
    #         P_Sop = np.maximum(0.032 * (S_op + 0.3) ** -3, 1.66 * (S_op + 0.3) ** 0.47)
    #
    #         P_D = 1 / (0.054 * d_b ** -1.3 + 0.79)
    #
    #         fs_front = np.maximum(1 - c1 * np.log(t / (Tp / 1.2) / 1000), c2)
    #
    #         Irr = np.tan(a) / (np.sqrt(S_op))
    #
    #         MAX_stab = ((7 * (np.minimum(Irr, 2)) ** (-1 / 3) + np.maximum(0.5 * (np.minimum(Irr, 5) - 2), 0)) / (
    #             np.maximum(((np.cos(B)) ** (2 / 3)), 0.4))) * fs_front
    #
    #         Z_basalton = [Hs / (((rho_c - rho_w) / rho_w) * d_b) -
    #                       np.minimum(4.93 * P_Zb * P_tana * P_Lambda * P_Delta * P_N * P_B * P_Sop * P_D, MAX_stab)]
    #
    #         return Z_basalton
    #
    #     basalton_failure_model = ot.PythonFunction(8, 1, basalton)
    #     distribution.setDescription(["Hs", "Tp", "t", "h", "a", "rho_c", "d_B", "rho_w"])
    #     vector = ot.RandomVector(distribution_Basalton)
    #     Z_basalton = ot.CompositeRandomVector(basalton_failure_model, vector)
    #     basalton_event = ot.ThresholdEvent(Z_basalton, ot.Less(), 0.0)
    #     basalton_event.setName("Failure of revetment for basalton")
    #
    #     if probabilistic == 'FORM':
    #
    #         # Using FORM, define a solver:
    #
    #         optimAlgo = ot.Cobyla()
    #         optimAlgo.setMaximumEvaluationNumber(100000)
    #         optimAlgo.setMaximumAbsoluteError(1.0e-10)
    #         optimAlgo.setMaximumRelativeError(1.0e-10)
    #         optimAlgo.setMaximumResidualError(1.0e-10)
    #         optimAlgo.setMaximumConstraintError(1.0e-10)
    #
    #         # Run FORM
    #         basalton_startingPoint = distribution_Basalton.getMean()
    #         basalton_algo = ot.FORM(optimAlgo, basalton_event, basalton_startingPoint)
    #         basalton_algo.run()
    #         basalton_result = basalton_algo.getResult()
    #         standardSpaceDesignPoint = basalton_result.getStandardSpaceDesignPoint()
    #
    #         # Retrieve results
    #         probability_basalton = basalton_result.getEventProbability()
    #         beta_basalton = basalton_result.getHasoferReliabilityIndex()
    #         # print(f"Pf basalton ={probability_basalton}, beta basalton = {beta_basalton}")
    #
    #         # Importance factors (alpha)
    #         # alpha = basalton_result.drawImportanceFactors()
    #         # viewer.View(alpha)
    #         # plt.show()
    #
    #     elif probabilistic == 'custom_MC':
    #         def condition(x):
    #             if x < 0:
    #                 return 1
    #             return 0
    #
    #         def custom_montecarlo(sample_size, vector):
    #             matrix = np.apply_along_axis(basalton, 1, np.array(vector.getSample(sample_size)))
    #             matrix = matrix[matrix[:, 0] < 9999999999]
    #
    #             monte_carlo = np.apply_along_axis(condition, 1, matrix)
    #             sum_success = monte_carlo.sum()
    #             samples = len(matrix)
    #             pf = sum_success / samples
    #
    #             return pf, samples
    #
    #         nu = time.time()
    #         # pf = 0
    #         sample_size = 20
    #
    #         probability_basalton, size = custom_montecarlo(sample_size, vector)
    #         # print(probability_basalton, size)
    #
    #     elif probabilistic == 'MC':
    #         # Creating the Monte Carlo simulation
    #         experiment = ot.MonteCarloExperiment()
    #         algo = ot.ProbabilitySimulationAlgorithm(basalton_event, experiment)
    #         algo.setMaximumCoefficientOfVariation(0.01)
    #         algo.setMaximumOuterSampling(int(1e7))
    #         algo.run()
    #
    #         # Retrieve results
    #         result = algo.getResult()
    #         probability_basalton = result.getProbabilityEstimate()
    #         # print("Pf=", probability_basalton)
    #
    #     elif probabilistic == 'Importance':
    #         # Using FORM, define a solver:
    #         optimAlgo = ot.Cobyla()
    #         optimAlgo.setMaximumEvaluationNumber(100000)
    #         optimAlgo.setMaximumAbsoluteError(1.0e-10)
    #         optimAlgo.setMaximumRelativeError(1.0e-10)
    #         optimAlgo.setMaximumResidualError(1.0e-10)
    #         optimAlgo.setMaximumConstraintError(1.0e-10)
    #
    #         # Run FORM
    #         startingPoint = distribution_Basalton.getMean()
    #         algo = ot.FORM(optimAlgo, basalton_event, startingPoint)
    #         algo.run()
    #         result = algo.getResult()
    #
    #         # Design point
    #         standardSpaceDesignPoint = result.getStandardSpaceDesignPoint()
    #         dimension = distribution.getDimension()
    #
    #         # Importance sampling algorithm
    #         myImportance = ot.Normal(dimension)
    #         myImportance.setMean(standardSpaceDesignPoint)
    #         experiment = ot.ImportanceSamplingExperiment(myImportance)
    #         standardEvent = ot.StandardEvent(basalton_event)
    #
    #         # Run the simulation
    #         algo = ot.ProbabilitySimulationAlgorithm(standardEvent, experiment)
    #         algo.setMaximumCoefficientOfVariation(0.1)
    #         algo.setMaximumOuterSampling(40000)
    #         algo.run()
    #
    #         # Retrieve the results
    #         result = algo.getResult()
    #         probability = result.getProbabilityEstimate()
    #         # print("Probability = ", probability)
    #
    #     return probability_basalton, size
    #
    # # Retrieve alpha values: Use 1 row as input for the function, otherwise too many graphs to publish.
    #
    # # x = ElementInput.distributionbasalton[20]
    # # y = ElementInput.deterministicbasalton
    # # Pf_for_alpha = (probBasalton(x, y, 'FORM'))
    # # print(x, y)
    # # print(Pf_for_alpha)
    #
    # Pf_Basalton = []
    # nr_samples = []
    # start_time = time.time()
    #
    # for i in ElementInput.distributionbasalton:
    #     start_time = time.time()
    #     Pf_Basalton.append(probBasalton(i, ElementInput.deterministicbasalton, 'custom_MC')[0])
    #     nr_samples.append(probBasalton(i, ElementInput.deterministicbasalton, 'custom_MC')[1])
    #
    #     print(Pf_Basalton[-1], nr_samples[-1])
    #
    #     end_time = time.time()
    #     execution_time = end_time - start_time
    #
    #     print("Execution time:", execution_time, "seconds")
    #
    # print("BASALTON Execution time:", execution_time, "seconds, ", "seconds per calculation:",
    #       execution_time / len(Pf_Basalton))
    # print(len(Pf_Basalton), Pf_Basalton)


class VerkalitFunc:

    def probVerkalit(distribution, deterministic, probabilistic='custom_MC'):
        distribution_Verkalit = distribution
        deterministic_Verkalit = deterministic

        def verkalit(self):
            rho_c = self[5]
            d_b = self[6]
            rho_w = self[7]
            a = self[4]
            t = self[2]
            Hs = self[0]
            h = self[3]
            Tp = self[1]
            B = deterministic_Verkalit[0]
            c1 = deterministic_Verkalit[1]
            c2 = deterministic_Verkalit[2]
            b1 = deterministic_Verkalit[3]
            k2 = deterministic_Verkalit[4]
            b2 = deterministic_Verkalit[5]
            v_kin = deterministic_Verkalit[6]
            n_f = deterministic_Verkalit[7]
            D_f15 = deterministic_Verkalit[8]
            g = deterministic_Verkalit[9]
            Zb = deterministic_Verkalit[10]
            f_V = deterministic_Verkalit[11]

            def Wavelength(g, Tp, h):
                c = [0.00011, 0.00039, 0.00171, 0.00654, 0.02174, 0.06320, 0.16084, 0.35550, 0.66667, 1]
                sg = (2 * np.pi) / Tp
                c0 = g / sg
                k0d = sg * (h + 0.4) / c0
                kd = np.sqrt(k0d * k0d + k0d / np.polyval(c, k0d))
                ar = k0d / kd
                sf = ar + kd * (1 - ar * ar)
                cf = c0 * ar
                l = cf * Tp
                cg = 0.5 * c0 * sf
                sf = 1 / np.sqrt(sf)  # shoaling factor
                return l, cf, cg, ar, sf

            L = Wavelength(g, Tp, h)[0]

            # If performing FORM analysis turn the breaker criterium off. Too discontinue
            H_sb = (0.095 * np.exp(4 * (1 / 33))) * L * np.tanh((2 * np.pi * (0.4 + h)) / L)

            if H_sb < Hs:
                return [9999999999]

            P_Zb = np.maximum(1.06 * (np.maximum((Zb - h) / Hs, -0.3) + 0.3) ** 0.125,
                              5 * (np.minimum((Zb - h) / Hs, -0.2)) ** 4 + 0.9)

            P_tana = 0.54 * (np.tan(a)) ** -0.49

            a_f = 160 * (v_kin * (1 - n_f) ** 2) / (g * n_f ** 3 * D_f15 ** 2)

            b_f = 2.2 / (g * n_f ** 3 * D_f15)

            k1 = (-a_f + np.sqrt(a_f ** 2 + 1.2 * b_f)) / (0.6 * b_f)

            # omega = 0.13
            # s_s = -0.5 * (0.3 + 0.3) + np.sqrt(((omega * 0.3 * 0.3) / (1 - omega)) + 0.25 * (0.3 + 0.3)**2)
            # s = s_s + 0.3 * 10**-3
            # A_ro = s / (0.3 + s)
            #
            # a_s = (12 * v_kin) / (g * s**2 * A_ro)

            # Lambda = np.maximum(np.sqrt((d_b * (b1 * k1 + b2 * k2)) / k))
            Lambda = 0.38

            P_Lambda = 0.42 * (Lambda / d_b) ** -2.4 + 0.81

            P_Delta = 0.25 * ((rho_c - rho_w) / rho_w - 1.7) ** 2 + 0.98

            P_N = np.maximum(3.1 * (t / (Tp / 1.2)) ** -0.141, 0.8)

            P_B = 5.5 * 10 ** -22 * (B + 90) ** 9.5 + 1

            S_op = Hs / L

            P_Sop = np.maximum(0.032 * (S_op + 0.3) ** -3, 1.66 * (S_op + 0.3) ** 0.47)

            P_D = 1 / (0.054 * d_b ** -1.3 + 0.79)

            fs_front = np.maximum(1 - c1 * np.log(t / (Tp / 1.2) / 1000), c2)

            Irr = np.tan(a) / (np.sqrt(S_op))

            MAX_stab = ((7 * (np.minimum(Irr, 2)) ** (-1 / 3) + np.maximum(0.5 * (np.minimum(Irr, 5) - 2), 0)) / (
                np.maximum(((np.cos(B)) ** (2 / 3)), 0.4))) * fs_front

            Z_Verkalit = [Hs / (((rho_c - rho_w) / rho_w) * d_b) -
                          np.minimum(4.93 * P_Zb * P_tana * P_Lambda * P_Delta * P_N * P_B * P_Sop * P_D * f_V,
                                     MAX_stab)]

            return Z_Verkalit

        Verkalit_failure_model = ot.PythonFunction(8, 1, verkalit)
        distribution.setDescription(["Hs", "Tp", "t", "h", "a", "rho_c", "d_B", "rho_w"])
        vector = ot.RandomVector(distribution_Verkalit)
        Z_Verkalit = ot.CompositeRandomVector(Verkalit_failure_model, vector)
        Verkalit_event = ot.ThresholdEvent(Z_Verkalit, ot.Less(), 0.0)
        Verkalit_event.setName("Failure of revetment for Verkalit")

        if probabilistic == 'FORM':

            optimAlgo = ot.Cobyla()
            optimAlgo.setMaximumEvaluationNumber(100000)
            optimAlgo.setMaximumAbsoluteError(1.0e-10)
            optimAlgo.setMaximumRelativeError(1.0e-10)
            optimAlgo.setMaximumResidualError(1.0e-10)
            optimAlgo.setMaximumConstraintError(1.0e-10)

            # Run FORM
            Verkalit_startingPoint = distribution_Verkalit.getMean()
            Verkalit_algo = ot.FORM(optimAlgo, Verkalit_event, Verkalit_startingPoint)
            Verkalit_algo.run()
            Verkalit_result = Verkalit_algo.getResult()
            standardSpaceDesignPoint = Verkalit_result.getStandardSpaceDesignPoint()

            # Retrieve results
            probability_Verkalit = Verkalit_result.getEventProbability()
            beta_Verkalit = Verkalit_result.getHasoferReliabilityIndex()
            # print(f"Pf Verkalit ={probability_Verkalit}, beta Verkalit = {beta_Verkalit}")

            # Importance factors (alpha)
            # alpha = Verkalit_result.drawImportanceFactors()
            # viewer.View(alpha)
            # plt.show()

        elif probabilistic == 'custom_MC':
            def condition(x):
                if x < 0:
                    return 1
                return 0

            def custom_montecarlo(sample_size, vector):
                matrix = np.apply_along_axis(verkalit, 1, np.array(vector.getSample(sample_size)))
                matrix = matrix[matrix[:, 0] < 9999999999]

                monte_carlo = np.apply_along_axis(condition, 1, matrix)
                sum_success = monte_carlo.sum()
                samples = len(matrix)
                pf = sum_success / samples

                return pf, samples

            nu = time.time()
            # pf = 0
            sample_size = 1000

            probability_Verkalit, size = custom_montecarlo(sample_size, vector)

        elif probabilistic == 'MC':
            # Creating the Monte Carlo simulation
            experiment = ot.MonteCarloExperiment()
            algo = ot.ProbabilitySimulationAlgorithm(Verkalit_event, experiment)
            algo.setMaximumCoefficientOfVariation(0.01)
            algo.setMaximumOuterSampling(int(1e7))
            algo.setBlockSize(50)
            algo.run()

            # Retrieve results
            result = algo.getResult()
            probability_Verkalit = result.getProbabilityEstimate()
            # print("Pf=", probability)

        elif probabilistic == 'Importance':
            # Using FORM, define a solver:
            optimAlgo = ot.Cobyla()
            optimAlgo.setMaximumEvaluationNumber(100000)
            optimAlgo.setMaximumAbsoluteError(1.0e-10)
            optimAlgo.setMaximumRelativeError(1.0e-10)
            optimAlgo.setMaximumResidualError(1.0e-10)
            optimAlgo.setMaximumConstraintError(1.0e-10)

            # Run FORM
            startingPoint = distribution_Verkalit.getMean()
            algo = ot.FORM(optimAlgo, Verkalit_event, startingPoint)
            algo.run()
            result = algo.getResult()

            # Design point
            standardSpaceDesignPoint = result.getStandardSpaceDesignPoint()
            dimension = distribution.getDimension()

            # Importance sampling algorithm
            myImportance = ot.Normal(dimension)
            myImportance.setMean(standardSpaceDesignPoint)
            experiment = ot.ImportanceSamplingExperiment(myImportance)
            standardEvent = ot.StandardEvent(Verkalit_event)

            # Run the simulation
            algo = ot.ProbabilitySimulationAlgorithm(standardEvent, experiment)
            algo.setMaximumCoefficientOfVariation(0.1)
            algo.setMaximumOuterSampling(40000)
            algo.run()

            # Retrieve the results
            result = algo.getResult()
            probability_Verkalit = result.getProbabilityEstimate()
            # print("Probability = ", probability)

        return probability_Verkalit, size

    # Retrieve alpha values: Use 1 row as input for the function, otherwise too many graphs to publish.

    # x = ElementInput.distributionverkalit[20]
    # y = ElementInput.deterministicverkalit
    # Pf_for_alpha = (probVerkalit(x, y, 'FORM'))
    # print(x, y)
    # print(Pf_for_alpha)

    Pf_Verkalit = []
    nr_samples = []
    start_time = time.time()

    for i in ElementInput.distributionverkalit:
        Pf_Verkalit.append(probVerkalit(i, ElementInput.deterministicverkalit, 'custom_MC')[0])
        nr_samples.append(probVerkalit(i, ElementInput.deterministicverkalit, 'custom_MC')[1])

    end_time = time.time()
    execution_time = end_time - start_time

    print("VERKALIT: Execution time:", execution_time, "seconds, ", "seconds per calculation:",
          execution_time / len(Pf_Verkalit))

    print("VERKALIT:,", len(Pf_Verkalit), Pf_Verkalit)
    print("VERKALIT:" ,nr_samples)
