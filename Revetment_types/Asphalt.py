# This is the file where Asphalt revetment is calculated.

import numpy as np
import openturns as ot
import time
import openturns.viewer as viewer
from matplotlib import pylab as plt
from Input.Parameters_Class import AsphaltUpliftInput
from Input.Parameters_Class import AsphaltImpactInput
from scipy.optimize import fsolve
from concurrent.futures import ProcessPoolExecutor

ot.Log.Show(ot.Log.NONE)


class AsphaltFunc:

    # def probasphaltuplift(distribution, probabilistic='FORM'):
    #
    #     distributionasphalt = distribution
    #
    #     def asphalt_uplift(self):
    #         d = self[4]
    #         rho_w = self[5]
    #         rho_a = self[6]
    #         a = self[3]
    #         a_vert = self[0]
    #         v_vert = self[1]
    #         R = self[2]
    #
    #         Qn = 0.96 / np.cos(a)
    #
    #         Z = [d - (0.21 * Qn * (a_vert + v_vert) * (rho_w / (rho_a - rho_w)) * R)]
    #         return Z
    #
    #     uplift_failure_model = ot.PythonFunction(7, 1, asphalt_uplift)
    #     distribution.setDescription(["d", "rho_w", "rho_a", "a", "a_vert", "v_vert", "R"])
    #     vect = ot.RandomVector(distributionasphalt)
    #     Z = ot.CompositeRandomVector(uplift_failure_model, vect)
    #     event = ot.ThresholdEvent(Z, ot.Less(), 0.0)
    #     event.setName("Failure of asphalt for uplift")
    #
    #     if probabilistic == 'FORM':
    #
    #         # Using FORM, define a solver:
    #         optimAlgo = ot.Cobyla()
    #         optimAlgo.setMaximumEvaluationNumber(1000000)
    #         optimAlgo.setMaximumAbsoluteError(1.0e-10)
    #         optimAlgo.setMaximumRelativeError(1.0e-10)
    #         optimAlgo.setMaximumResidualError(1.0e-10)
    #         optimAlgo.setMaximumConstraintError(1.0e-10)
    #
    #         # Run FORM
    #         startingPoint = distributionasphalt.getMean()
    #         algo = ot.FORM(optimAlgo, event, startingPoint)
    #         algo.run()
    #         result = algo.getResult()
    #         # standardSpaceDesignPoint = result.getStandardSpaceDesignPoint()
    #
    #         # Retrieve results
    #         probability_uplift = result.getEventProbability()
    #         beta_uplift = result.getHasoferReliabilityIndex()
    #         # print(f"Pf uplift ={probability_uplift}, beta uplift = {beta_uplift}")
    #
    #         # Importance factors (alpha)
    #         # alpha = result.drawImportanceFactors()
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
    #
    #             matrix = np.apply_along_axis(asphalt_uplift, 1, np.array(vector.getSample(sample_size)))
    #
    #             monte_carlo = np.apply_along_axis(condition, 1, matrix)
    #             sum_success = monte_carlo.sum()
    #             samples = len(matrix)
    #             pf = sum_success / samples
    #
    #             return pf, samples
    #
    #         nu = time.time()
    #         sample_size = 1000
    #
    #         probability_uplift, size = custom_montecarlo(sample_size, vect)
    #
    #         # print('Probability of failure =', probability_uplift, 'with sample size', size)
    #         # print('duration =', time.time() - nu)
    #
    #     elif probabilistic == 'MC':
    #         # Creating the Monte Carlo simulation
    #         experiment = ot.MonteCarloExperiment()
    #         algo = ot.ProbabilitySimulationAlgorithm(event, experiment)
    #         algo.setMaximumCoefficientOfVariation(0.05)
    #         algo.setMaximumOuterSampling(int(1e5))
    #         algo.setBlockSize(50)
    #         algo.run()
    #
    #         # Retrieve results
    #         result = algo.getResult()
    #         probability_uplift = result.getProbabilityEstimate()
    #         # print("Pf=", probability)
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
    #         startingPoint = distributionasphalt.getMean()
    #         algo = ot.FORM(optimAlgo, event, startingPoint)
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
    #         standardEvent = ot.StandardEvent(event)
    #
    #         # Run the simulation
    #         algo = ot.ProbabilitySimulationAlgorithm(standardEvent, experiment)
    #         algo.setMaximumCoefficientOfVariation(0.1)
    #         algo.setMaximumOuterSampling(40000)
    #         algo.run()
    #
    #         # Retrieve the results
    #         result = algo.getResult()
    #         probability_uplift = result.getProbabilityEstimate()
    #         # print("Probability = ", probability)
    #
    #     return probability_uplift
    #
    # # Retrieve alpha values: Use 1 row as input for the function, otherwise too many graphs to publish.
    #
    # # x = AsphaltUpliftInput.distribution_uplift_asphalt[20]
    # #
    # # Pf_for_alpha = (probasphaltuplift(x, 'FORM'))
    # # print(x)
    # # print(Pf_for_alpha)
    #
    # Pf_asphalt_uplift = []
    # start_time = time.time()
    #
    # for i in AsphaltUpliftInput.distribution_uplift_asphalt:
    #     Pf_asphalt_uplift.append(probasphaltuplift(i, 'FORM'))
    #
    # end_time = time.time()
    # execution_time = end_time - start_time
    #
    # print("Execution time:", execution_time, "seconds, ", "seconds per calculation:",
    #       execution_time / len(Pf_asphalt_uplift))
    # print(Pf_asphalt_uplift)

    def probasphaltimpact(self, distribution, deterministic, probabilistic='custom_MC'):

        distributionasphalt = distribution
        deterministicasphalt = deterministic

        def asphalt_impact(self):
            Hs = self[0]
            Tp = self[1]
            a = self[3]
            q_r = self[4]
            rho_w = self[5]
            c = self[6]
            E = self[7]
            d = self[8]
            sigma_b = self[9]
            t = self[2]
            h = self[10]

            g = deterministicasphalt[0]
            v = deterministicasphalt[1]
            alpha = deterministicasphalt[2]
            B = deterministicasphalt[3]

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

            # When performing FORM analysis turn the breaker criterium off, too discontinue
            H_sb = (0.095 * np.exp(4 * (1 / 33))) * L * np.tanh((2 * np.pi * (0.4 + h)) / L)

            if H_sb < Hs:
                return [9999999999]

            q = (np.tan(a) / 0.25) * q_r

            P_max = rho_w * g * q * Hs

            Beta = ((3 * c * (1 - v ** 2)) / (E * d ** 3)) ** (1 / 4)

            z = np.minimum(0.75 * Hs, 1.3355 / Beta)

            sigma = (P_max / (4 * (Beta ** 3) * z)) * (
                    1 - np.exp(-Beta * z) * ((np.cos(Beta * z)) + np.sin(Beta * z))) * (6 / d ** 2)

            Nf = 10 ** (B * (np.log10(sigma_b) - np.log10(sigma)) ** alpha)
            # print(z, Beta, q, q_r, P_max, B, sigma_b, sigma, alpha, Nf)
            N = t / (Tp / 1.2)

            Z_impact = [Nf - N]

            return Z_impact

        impact_failure_model = ot.PythonFunction(11, 1, asphalt_impact)
        distribution.setDescription(["Hs", "Tp", "t", "a", "q_r", "rho_w", "c", "E", "d", "sigma_b", "h"])
        vector = ot.RandomVector(distributionasphalt)
        Z_impact = ot.CompositeRandomVector(impact_failure_model, vector)
        impact_event = ot.ThresholdEvent(Z_impact, ot.Less(), 0.0)
        impact_event.setName("Failure of asphalt for impact")

        if probabilistic == 'FORM':

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
            # standardSpaceDesignPoint = impact_result.getStandardSpaceDesignPoint()

            # Retrieve results
            probability_impact = impact_result.getEventProbability()
            beta_impact = impact_result.getHasoferReliabilityIndex()
            # print(f"Pf impact ={probability_impact}, beta impact = {beta_impact}")

            # Importance factors (alpha)
            # alpha = impact_result.drawImportanceFactors()
            # viewer.View(alpha)
            # plt.show()

        elif probabilistic == 'custom_MC':
            def condition(x):
                if x < 0:
                    return 1
                return 0

            def custom_montecarlo(sample_size, vector):

                matrix = np.apply_along_axis(asphalt_impact, 1, np.array(vector.getSample(sample_size)))
                matrix = matrix[matrix[:, 0] < 9999999999]

                monte_carlo = np.apply_along_axis(condition, 1, matrix)
                sum_success = monte_carlo.sum()
                samples = len(matrix)
                pf = sum_success / samples
                # print(samples)
                return pf, samples

            sample_size = 1450
            probability_impact, size = custom_montecarlo(sample_size, vector)
            # print(probability_impact, size)

        elif probabilistic == 'MC':
            # Creating the Monte Carlo simulation
            experiment = ot.MonteCarloExperiment()
            algo = ot.ProbabilitySimulationAlgorithm(impact_event, experiment)
            algo.setMaximumCoefficientOfVariation(0.05)
            algo.setMaximumOuterSampling(int(1e5))
            algo.setBlockSize(50)
            algo.run()

            # Retrieve results
            result = algo.getResult()
            probability_impact = result.getProbabilityEstimate()
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
            startingPoint = distributionasphalt.getMean()
            algo = ot.FORM(optimAlgo, impact_event, startingPoint)
            algo.run()
            result = algo.getResult()

            # Design point
            standardSpaceDesignPoint = result.getStandardSpaceDesignPoint()
            dimension = distribution.getDimension()

            # Importance sampling algorithm
            myImportance = ot.Normal(dimension)
            myImportance.setMean(standardSpaceDesignPoint)
            experiment = ot.ImportanceSamplingExperiment(myImportance)
            standardEvent = ot.StandardEvent(impact_event)

            # Run the simulation
            algo = ot.ProbabilitySimulationAlgorithm(standardEvent, experiment)
            algo.setMaximumCoefficientOfVariation(0.1)
            algo.setMaximumOuterSampling(40000)
            algo.run()

            # Retrieve the results
            result = algo.getResult()
            probability_impact = result.getProbabilityEstimate()
            # print("Probability = ", probability)

        return probability_impact, size

    # Retrieve alpha values: Use 1 row as input for the function, otherwise too many graphs to publish.

    # x = AsphaltImpactInput.distribution_impact_asphalt[200]
    # y = AsphaltImpactInput.deterministic_impact_asphalt

    # Pf_for_alpha = (probasphaltimpact(x, y, 'FORM'))
    # print(x, y)
    # print(Pf_for_alpha)

def probability_asphalt_impact(args):
    i, j = args
    asphalt_instance = AsphaltFunc()
    result, samples, = asphalt_instance.probasphaltimpact(i, j, 'custom_MC')
    return result, samples

if __name__ == "__main__":
    Pf_asphalt_impact = []
    nr_samples = []

    start_time = time.time()

    # Create the ProcessPoolExecutor with the desired number of processes
    num_processes = 6  # Adjust based on the system's capacity
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        args_list = [(i, AsphaltImpactInput.deterministic_impact_asphalt) for i in AsphaltImpactInput.distribution_impact_asphalt]
        results = executor.map(probability_asphalt_impact, args_list)

    # Collect the results
    for result, samples in results:
        Pf_asphalt_impact.append(result)
        nr_samples.append(samples)
        print(len(Pf_asphalt_impact), Pf_asphalt_impact)
        print(nr_samples)

    end_time = time.time()
    execution_time = end_time - start_time

    print("Asphalt impact, Execution time:", execution_time, "seconds, seconds per calculation:",
          execution_time / len(Pf_asphalt_impact))

    print("Asphalt impact", Pf_asphalt_impact, len(Pf_asphalt_impact))
    print("Asphalt imapct", nr_samples)
