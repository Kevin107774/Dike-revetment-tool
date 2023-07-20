import numpy as np
import openturns as ot
import time
import openturns.viewer as viewer
from matplotlib import pylab as plt
from Input.Parameters import Parameters

ot.Log.Show(ot.Log.NONE)


class sensitivity_LR:
    FunctionvdMeer = ['C_pl * P ^ 0.18 * (S / (t / (Tp / 1.2))) ^ 0.2 * (tan(a1) / ((Hs / L)^0.5)) ^ -0.5 - '
                      'Hs / (((rho_s - rho_w) / rho_w) * Dn50)']

    model = ot.SymbolicFunction(['C_pl', 'P', 'S', 't', 'Tp', 'a1', 'Hs', 'L', 'rho_s', 'rho_w', 'Dn50'],
                                FunctionvdMeer)

    Hs = ot.Normal(0.93, 0.18)
    Tp = ot.Normal(3.33, 0.37)
    t = ot.Normal(21060, 1053)
    h = ot.Normal(1.8, 0.0001)

    rho_s = Parameters.Density_rock
    rho_w = Parameters.Density_water
    P = Parameters.Porosity
    C_pl = Parameters.Uncertainty_a
    a1 = Parameters.Slope_angle1
    S = ot.Uniform(4.9999, 5.0001)

    Dn50 = ot.Normal(0.17, 0.17 * 0.03)

    L = (Tp / 1.2) * np.sqrt(9.81 * (h + 0.4))

    distribution = ot.ComposedDistribution([C_pl, P, S, t, Tp, a1, Hs, L, rho_s, rho_w, Dn50])
    distribution.setDescription(['C_pl', 'P', 'S', 't', 'Tp', 'a1', 'Hs', 'L', 'rho_s', 'rho_w', 'Dn50'])

    # Define size to compute
    size = 200000
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
