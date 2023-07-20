# This is the main of the Revetment tool

import numpy as np
import pandas as pd
import openturns as ot
import time
import openturns.viewer as viewer
from matplotlib import pylab as plt
from Revetment_types.Loose_Rock import VdMeerFunc
from Input.Parameters import Parameters
# from Revetment_types.Asphalt import AsphaltFunc
# from Revetment_types.Placed_elements import BasaltonFunc
# from Revetment_types.Placed_elements import VerkalitFunc
from ECI.ECI import ECIFunc
from ECI.ECI_Library import ECILib

Hydraulic_BC = pd.read_excel(
    r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Hydra en Steentoets\Hydra-NL\Hydraulic boundary '
    r'conditions.xlsx')


# from Revetment_types.Grass import Grass


# ot.Log.Show(ot.Log.NONE)

def pflifetime(probability):
    # Poisson's distribution for probability of failure lifetime
    lifetime = 10
    probabilty_lft = 1 - (1 - probability) ** lifetime
    return probabilty_lft


# ----------------------------------------------------------------------------------------------------------------------
# LOOSE ROCK

# Select the range of hydraulic boundary conditions in the following files: Hydra and Parameters. Default for Loose rock is [0:8, :]


# Retrieve results from Loose Rock revetment
Probability_failure_LR = VdMeerFunc.Pf_Loose_Rock
Parameter_combinations = Parameters.parameter_combinations_LR

# Add the Pf as a column to the dataframe
Parameter_combinations['Probability of failure'] = Probability_failure_LR
Parameter_combinations['Pf 50 years'] = pflifetime(Parameter_combinations['Probability of failure'])


# Add the ECI as a column to the dataframe
def maintenance_lr(diameter, ECI_main):
    amount_maintenance_year = 0.20
    # eens per drie jaar onderhoud
    design_lifetime = 50
    maintenance = diameter * ECI_main * amount_maintenance_year * design_lifetime
    return maintenance


Parameter_combinations['ECI'] = Parameter_combinations.apply(
    lambda row: ECIFunc.ECILooseRock(row['Nominal diameter rock'], row['Waterlevel +mNAP'], row['Slope angle'])
    if row['Damage number [S]'] <= 5
    else ECIFunc.ECILooseRock(row['Nominal diameter rock'], row['Waterlevel +mNAP'],
                              row['Slope angle']) + maintenance_lr(
        row['Nominal diameter rock'], ECILib.ECI_LR_maintenance), axis=1)

print(Parameter_combinations)
# Parameter_combinations.to_excel("Test for ECI 2.xlsx")

# ----------------------------------------------------------------------------------------------------------------------
# ASPHALT
# Retrieve results from Asphalt uplift model
# Probability_failure_uplift = AsphaltFunc.Pf_asphalt_uplift
# Probability_failure_impact = AsphaltFunc.Pf_asphalt_impact
# Parameter_combinations_asphalt = Parameters.combinations_asphalt
# slopelength_Asphalt = 14.54
#
# # Inladen van de faalkans voor iedere parameter combinatie
# Parameter_combinations_asphalt['Probability of failure uplift'] = Probability_failure_uplift
# Parameter_combinations_asphalt['Probability of failure impact'] = Probability_failure_impact
#
# # De faalkans voor een levensduur van 50 jaar bepalen
# Parameter_combinations_asphalt['Pf uplift 50 year'] = pflifetime(Parameter_combinations_asphalt['Probability of '
#                                                                                                 'failure uplift'])
# Parameter_combinations_asphalt['Pf impact 50 year'] = pflifetime(Parameter_combinations_asphalt['Probability of '
#                                                                                                 'failure impact'])
#
# # De MKI voor iedere parametercombinatie bepalen
# Parameter_combinations_asphalt['ECI'] = ECIFunc.ECIAsphalt(slopelength_Asphalt * Parameter_combinations_asphalt[
#     'Asphalt layer thickness'])
#
# # print(Parameter_combinations_asphalt)
#
# # ----------------------------------------------------------------------------------------------------------------------
# # ELEMENTS (Basalton)
# # Retrieve results from elements, Basalton
# Probability_failure_Basalton = BasaltonFunc.Pf_Basalton
# Parameter_combinations_Basalton = Parameters.parameter_combinations_Basalton
# slopelength_Basalton = 4.82
#
# # Inladen van de faalkans voor iedere parameter combinatie
# Parameter_combinations_Basalton['Probability of failure Basalton'] = Probability_failure_Basalton
#
# # De faalkans voor een levensduur van 50 jaar bepalen
# Parameter_combinations_Basalton['Pf Basalton 50 year'] = pflifetime(
#     Parameter_combinations_Basalton['Probability of failure Basalton'])
#
# # De MKI voor iedere parametercombinatie bepalen
# Parameter_combinations_Basalton['ECI'] = ECIFunc.ECIBasalton(slopelength_Basalton * Parameter_combinations_Basalton[
#     'Layer thickness Basalton'])
#
# # ----------------------------------------------------------------------------------------------------------------------
# # ELEMENTS (Verkalit)
# # Retrieve results from elements, Verkalit
# Probability_failure_Verkalit = VerkalitFunc.Pf_Verkalit
# Parameter_combinations_Verkalit = Parameters.parameter_combinations_Verkalit
# slopelength_Verkalit = 4.82
#
# # Inladen van de faalkans voor iedere parameter combinatie
# Parameter_combinations_Verkalit['Probability of failure Verkalit'] = Probability_failure_Verkalit
#
# # De faalkans voor een levensduur van 50 jaar bepalen
# Parameter_combinations_Verkalit['Pf Verkalit 50 year'] = pflifetime(
#     Parameter_combinations_Verkalit['Probability of failure Verkalit'])
#
# # De MKI voor iedere parametercombinatie bepalen
# Parameter_combinations_Verkalit['ECI'] = ECIFunc.ECIVerkalit(slopelength_Verkalit * Parameter_combinations_Verkalit[
#     'Layer thickness Verkalit'])
#
# # print(Parameter_combinations_Verkalit)
#
# # ----------------------------------------------------------------------------------------------------------------------
# # GRASS
#
# GEBU_results = Grass.GEBU_results
# GEBU_results['slopelength_Grass 1:60.000'] = np.sqrt(
#     (8.22 - GEBU_results.iloc[:, 0]) ** 2 + ((8.22 - GEBU_results.iloc[:, 0]) * 4) ** 2)
#
#
# volume_ECI = GEBU_results.iloc[:, 6] * GEBU_results.iloc[:, 1] - (GEBU_results.iloc[:, 1]-0.8) / 2
# volume_ECI_50y = GEBU_results.iloc[:, 6] * GEBU_results.iloc[:, 3] - (GEBU_results.iloc[:, 3]-0.8) / 2
#
# GEBU_results['ECI 1:60.000'] = ECIFunc.ECIGrass(volume_ECI)
# GEBU_results['ECI 50 year'] = ECIFunc.ECIGrass(volume_ECI_50y)
#
# # Plot the first column
# plt.plot(GEBU_results.iloc[:, 0], GEBU_results.iloc[:, 1])
#
# # Add labels and title
# plt.xlabel('Transition height')
# plt.ylabel('Clay layer thickness')
# plt.title('Clay layer thickness per transition height')
# plt.show()
#
# # print(GEBU_results)
#
