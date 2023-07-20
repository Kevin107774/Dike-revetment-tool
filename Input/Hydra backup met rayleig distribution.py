# This is where the Hydra input is being imported and converted to a class such that it can be used as an input parameter for the probabilistic calculations.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import openturns as ot


ot.Log.Show(ot.Log.NONE)

# Import hydraulic boundary conditions file from excel
# Read the Hm0 values from the Excel file
data = pd.read_excel(
    r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Hydra en Steentoets\Hydra-NL\Hydra input.xlsx')

# Water level h:
h_loose_rock = data.iloc[0:21, 1]
h_verkalit = data.iloc[21:32, 1]
h_basalton = data.iloc[32:43, 1]
h_asphalt = data.iloc[43:, 1]

# Significant wave height Hm0:
Hm0_loose_rock = data.iloc[0:21, [2, 4]]
Hm0_verkalit = data.iloc[21:32, [2, 4]]
Hm0_basalton = data.iloc[32:43, [2, 4]]
Hm0_asphalt = data.iloc[43:, [2, 4]]

H_Loose_rock = []
for i in Hm0_loose_rock.iloc[:, 1]:
    sigma = i
    H_distr = ot.Rayleigh(sigma)
    H_Loose_rock.append(H_distr)

H_verkalit = []
for i in Hm0_verkalit.iloc[:, 1]:
    sigma = i
    H_distr = ot.Rayleigh(sigma)
    H_verkalit.append(H_distr)

H_basalton = []
for i in Hm0_basalton.iloc[:, 1]:
    sigma = i
    H_distr = ot.Rayleigh(sigma)
    H_basalton.append(H_distr)

H_asphalt = []
for i in Hm0_asphalt.iloc[:, 1]:
    sigma = i
    H_distr = ot.Rayleigh(sigma)
    H_asphalt.append(H_distr)

# Peak wave period Tp:
Tp_loose_rock = data.iloc[0:21, 3]
Tp_verkalit = data.iloc[21:32, 3]
Tp_basalton = data.iloc[32:43, 3]
Tp_asphalt = data.iloc[43:, 3]
