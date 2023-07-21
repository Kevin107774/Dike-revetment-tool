# This is the file where loose rock is being calculated according to the vd Meer Equations.
import numpy as np
import openturns as ot
import time

import pandas as pd
from openturns.viewer import View
import openturns.viewer as viewer
from matplotlib import pylab as plt
from Input.Parameters_Class import VdMeerInput
from scipy.optimize import fsolve

ot.Log.Show(ot.Log.NONE)


class VdMeerFunc:

    def problooserock(distribution, deterministic, probabilistic='custom_MC'):

        distributionvdmeer = distribution
        deterministicvdmeer = deterministic

        def vdmeermodel(vector):
            S = deterministicvdmeer
            g = 9.81
            Dn50 = vector[0]
            rho_w = vector[1]
            rho_s = vector[2]
            P = vector[3]
            C_pl = vector[4]
            C_s = vector[5]
            t = vector[6]
            a = vector[7]
            Hs = vector[8]
            Tp = vector[9]
            h = vector[10]

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

            zeta = np.tan(a) / (np.sqrt(Hs / L))

            # If performing FORM analysis turn the breaker criterium off. Too discontinue
            H_sb = (0.095 * np.exp(4 * (1 / 33))) * L * np.tanh((2 * np.pi * (0.4 + h)) / L)
            # print(h, Hs, H_sb)

            if H_sb < Hs:
                return [9999999999]

            zeta_cr = (C_pl / C_s * P ** 0.31 * np.sqrt(np.tan(a))) ** 1 / (P + 0.5)

            if zeta <= zeta_cr:
                # Limit state function plunging waves:
                Z = [C_pl * P ** 0.18 * (S / (t / (Tp / 1.2))) ** 0.2 * (
                        np.tan(a) / (np.sqrt(Hs / L))) ** -0.5 - Hs / (((rho_s - rho_w) / rho_w) * Dn50)]

            else:
                # Limit state function surging waves:
                Z = [C_s * P ** -0.13 * (S / (t / Tp)) ** 0.2 * np.sqrt(1 / np.tan(a)) * (
                        np.tan(a) / (np.sqrt(Hs / L))) ** P - Hs / (((rho_s - rho_w) / rho_w) * Dn50)]
                # print(zeta)

            # print(Z)
            return Z

        ot_failure_model = ot.PythonFunction(11, 1, vdmeermodel)
        distribution.setDescription(["Dn50", "rho_w", "rho_s", " P", "C_pl", "C_s", "t", "a", "Hs", "Tp", "h"])
        vect = ot.RandomVector(distributionvdmeer)
        Z = ot.CompositeRandomVector(ot_failure_model, vect)
        event = ot.ThresholdEvent(Z, ot.Less(), 0.0)
        event.setName("Failure of rock diameter")

        if probabilistic == 'FORM':

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
            # standardSpaceDesignPoint = result.getStandardSpaceDesignPoint()

            # Retrieve results
            probability = result.getEventProbability()
            beta = result.getHasoferReliabilityIndex()
            # print(f"Pf={probability}, beta = {beta}" )

            # Importance factors (alpha)
            # alpha = result.drawImportanceFactors()
            # viewer.View(alpha)
            # plt.show()

        elif probabilistic == 'custom_MC':
            def condition(x):
                if x < 0:
                    return 1
                return 0

            def custom_montecarlo(sample_size, vector):

                matrix = np.apply_along_axis(vdmeermodel, 1, np.array(vector.getSample(sample_size)))
                matrix = matrix[matrix[:, 0] < 9999999999]

                monte_carlo = np.apply_along_axis(condition, 1, matrix)
                sum_success = monte_carlo.sum()
                samples = len(matrix)
                pf = sum_success / samples

                return pf, samples

            nu = time.time()
            # pf = 0
            sample_size = 1000

            probability, size = custom_montecarlo(sample_size, vect)
            # print(probability, size)

            # print('Probability of failure =', probability, 'with sample size', size)
            # print('duration =', time.time() - nu)

            # def min_sample_size(pf_value):
            #     return (1 - pf_value) * 1000
            #
            # while min_sample_size(pf) > sample_size-0.1:
            #     sample_size = sample_size * 10
            #     pf, size = custom_montecarlo(int(sample_size), vect)

        elif probabilistic == 'MC':
            # Creating the Monte Carlo simulation
            nu = time.time()
            experiment = ot.MonteCarloExperiment()
            algo = ot.ProbabilitySimulationAlgorithm(event, experiment)
            algo.setMaximumCoefficientOfVariation(0.01)
            algo.setMaximumOuterSampling(int(1e5))
            algo.setBlockSize(50)
            algo.run()

            # Retrieve results
            result = algo.getResult()
            # print('Number of samples OT =', result.getOuterSampling())
            probability = result.getProbabilityEstimate()
            # print("time_OT=", time.time() - nu)
            # print("Pf_OT=", probability)

        elif probabilistic == 'Importance':
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

            # Design point
            standardSpaceDesignPoint = result.getStandardSpaceDesignPoint()
            dimension = distribution.getDimension()

            # Importance sampling algorithm
            myImportance = ot.Normal(dimension)
            myImportance.setMean(standardSpaceDesignPoint)
            experiment = ot.ImportanceSamplingExperiment(myImportance)
            standardEvent = ot.StandardEvent(event)

            # Run the simulation
            algo = ot.ProbabilitySimulationAlgorithm(standardEvent, experiment)
            algo.setMaximumCoefficientOfVariation(0.1)
            algo.setMaximumOuterSampling(40000)
            algo.run()

            # Retrieve the results
            result = algo.getResult()
            probability = result.getProbabilityEstimate()
            # print("Probability = ", probability)

        return probability, size

    # Retrieve alpha values: Use 1 row as input for the function, otherwise too many graphs to publish.

    # x = VdMeerInput.distributionvdmeer2[20]
    # y = VdMeerInput.deterministicvdmeer2[5]
    # Pf_for_alpha = (problooserock(x, y, 'FORM'))
    # print(x, y)
    # print(Pf_for_alpha)

    Pf_Loose_Rock = []
    nr_samples = []

    start_time = time.time()

    for i in VdMeerInput.distributionvdmeer2:
        for j in VdMeerInput.deterministicvdmeer2:
            Pf_Loose_Rock.append(problooserock(i, j, 'custom_MC')[0])
            nr_samples.append(problooserock(i, j, 'custom_MC')[1])

    end_time = time.time()
    execution_time = end_time - start_time

    print("Loose rock, Execution time:", execution_time, "seconds, seconds per calculation:",
          execution_time / len(Pf_Loose_Rock))

    print("Loose rock", len(Pf_Loose_Rock), Pf_Loose_Rock)
    print("Loose rock", nr_samples)