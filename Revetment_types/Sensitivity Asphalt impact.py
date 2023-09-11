import numpy as np
import openturns as ot
import time
import openturns.viewer as viewer
from matplotlib import pylab as plt
from Input.Parameters import Parameters
import math

ot.Log.Show(ot.Log.NONE)


# class sensitivity_LR:
#     FunctionvdMeer = ['C_pl * P ^ 0.18 * (S / (t / (Tp / 1.2))) ^ 0.2 * (tan(a1) / ((Hs / L)^0.5)) ^ -0.5 - '
#                       'Hs / (((rho_s - rho_w) / rho_w) * Dn50)']
#
#     model = ot.SymbolicFunction(['C_pl', 'P', 'S', 't', 'Tp', 'a1', 'Hs', 'L', 'rho_s', 'rho_w', 'Dn50'],
#                                 FunctionvdMeer)
#
#     Hs = ot.Normal(0.93, 0.18)
#     Tp = ot.Normal(3.33, 0.37)
#     t = ot.Normal(21060, 1053)
#     h = ot.Normal(1.8, 0.0001)
#
#     rho_s = Parameters.Density_rock
#     rho_w = Parameters.Density_water
#     P = Parameters.Porosity
#     C_pl = Parameters.Uncertainty_a
#     a1 = Parameters.Slope_angle1
#     S = ot.Uniform(4.9999, 5.0001)
#
#     Dn50 = ot.Normal(0.17, 0.17 * 0.03)
#
#     L = (Tp / 1.2) * np.sqrt(9.81 * (h + 0.4))
#
#     distribution = ot.ComposedDistribution([C_pl, P, S, t, Tp, a1, Hs, L, rho_s, rho_w, Dn50])
#     distribution.setDescription(['C_pl', 'P', 'S', 't', 'Tp', 'a1', 'Hs', 'L', 'rho_s', 'rho_w', 'Dn50'])
#
#     # Define size to compute
#     size = 200000
#     inputDesign = ot.SobolIndicesExperiment(distribution, size).generate()
#     outputDesign = model(inputDesign)
#     # print(inputDesign.getSize())
#
#     output = model(inputDesign)
#     sensitivityAnalysis = ot.SaltelliSensitivityAlgorithm(inputDesign, outputDesign, size)
#     first_order = sensitivityAnalysis.getFirstOrderIndices()
#     total_order = sensitivityAnalysis.getTotalOrderIndices()
#     # print(first_order)
#     # print(total_order)
#
#     graph = sensitivityAnalysis.draw()
#     view = viewer.View(graph)
#     # plt.show()

class Sensitivity_Asphalt_impact:


    AsphaltImpact = '(10 ^ (B * (log10(sigma_b) - log10(((rho_w * g * ((tan(a) / 0.25) * q_r) * Hs) / (4 * ((((3 * c * (1 - v ^ 2)) / (E * d ^ 3)) ^ (1 / '
    AsphaltImpact += '4)) ^ 3) * (1.3355 / (((3 * c * (1 - v ^ 2)) / (E * d ^ 3)) ^ (1 / 4))))) * (1 - exp(-(((3 * '
    AsphaltImpact += 'c * (1 - v ^ 2)) / (E * d ^ 3)) ^ (1 / 4)) * (1.3355 / (((3 * c * (1 - v ^ 2)) / (E * d ^ 3)) ^ '
    AsphaltImpact += '(1 / 4)))) * ((cos((((3 * c * (1 - v ^ 2)) / (E * d ^ 3)) ^ (1 / 4)) * (1.3355 / (((3 * c * '
    AsphaltImpact += '(1 - v ^ 2)) / (E * d ^ 3)) ^ (1 / 4))))) + sin((((3 * c * (1 - v ^ 2)) / (E * d ^ 3)) ^ (1 / 4)) '
    AsphaltImpact += '* (1.3355 / (((3 * c * (1 - v ^ 2)) / (E * d ^ 3)) ^ (1 / 4)))))) * (6 / d ^ 2))) ^ alpha)) - t / '
    AsphaltImpact += '(Tp / 1.2)'

    input_variables = ['Hs', 'Tp', 't', 'a', 'q_r', 'rho_w', 'c', 'E', 'd', 'sigma_b', 'h', 'g', 'v', 'alpha', 'B']
    model = ot.SymbolicFunction(input_variables, [AsphaltImpact])

    Hs_dist = ot.Normal(2.36, 0.45)
    Tp_dist = ot.Normal(5.97, 0.66)
    t_dist = ot.Normal(16236, 812)
    a_dist = ot.Normal(3.75, 0.013)
    q_r_dist = ot.LogNormal(1.1268, 0.223)
    rho_w_dist = ot.Normal(1025, 30.75)
    c_dist = ot.LogNormal(18.39, 0.0606)
    E_dist = ot.Normal(7000*10**6, 1400*10**6)
    d_dist = ot.Normal(0.15, 0.015)
    sigma_b_dist = ot.Normal(6.3*10**7, 1.575*10**6)
    h_dist = ot.Normal(6.2, 0.0001)
    g_dist = ot.Uniform(9.809, 9.811)
    v_dist = ot.Uniform(0.349, 0.351)
    alpha_dist = ot.Uniform(0.499, 0.501)
    B_dist = ot.Uniform(5.39, 5.41)

    distribution = ot.ComposedDistribution([
        Hs_dist, Tp_dist, t_dist, a_dist, q_r_dist, rho_w_dist,
        c_dist, E_dist, d_dist, sigma_b_dist, h_dist, g_dist, v_dist,
        alpha_dist, B_dist])
    distribution.setDescription(['Hs', 'Tp', 't', 'a', 'q_r', 'rho_w', 'c', 'E', 'd', 'sigma_b', 'h', 'g', 'v', 'alpha', 'B'])

    # Define size to compute
    size = 2000000
    inputDesign = ot.SobolIndicesExperiment(distribution, size).generate()
    outputDesign = model(inputDesign)
    print(inputDesign.getSize())

    output = model(inputDesign)
    sensitivityAnalysis = ot.SaltelliSensitivityAlgorithm(inputDesign, outputDesign, size)
    first_order = sensitivityAnalysis.getFirstOrderIndices()
    total_order = sensitivityAnalysis.getTotalOrderIndices()
    print(first_order)
    print(total_order)

    graph = sensitivityAnalysis.draw()
    view = viewer.View(graph)
    plt.show()



