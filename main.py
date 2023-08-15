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
from ECI.ECI_class import ECIFunc
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
Number_samples = VdMeerFunc.nr_samples
Parameter_combinations = Parameters.parameter_combinations_LR

# Add the Pf as a column to the dataframe
Parameter_combinations['Probability of failure'] = Probability_failure_LR
Parameter_combinations['Pf 50 years'] = pflifetime(Parameter_combinations['Probability of failure'])
Parameter_combinations['Number of samples'] = Number_samples


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
Parameter_combinations.to_excel("LooseRock_S1600_tbv ECI(1.6-6.2mNAP).xlsx")

# ----------------------------------------------------------------------------------------------------------------------
# ASPHALT
# Retrieve results from Asphalt uplift model

# Parameter_combinations_asphalt = Parameters.parameter_combinations_asphalt
# Number_samples = AsphaltFunc.nr_samples
# # Probability_failure_uplift = AsphaltFunc.Pf_asphalt_uplift
# Probability_failure_impact = AsphaltFunc.Pf_asphalt_impact
# #
# #
# # Add the Pf as a column to the dataframe
# # Parameter_combinations_asphalt['Probability of failure uplift'] = Probability_failure_uplift
# Parameter_combinations_asphalt['Probability of failure impact'] = Probability_failure_impact
#
# #
# # Add the Pf for the design lifetime to the dataframe
# # Parameter_combinations_asphalt['Pf uplift 50 year'] = pflifetime(Parameter_combinations_asphalt['Probability of '
# #                                                                                                 'failure uplift'])
# Parameter_combinations_asphalt['Pf impact 50 year'] = pflifetime(Parameter_combinations_asphalt['Probability of '
#                                                                                                 'failure impact'])
# # Add the number of samples to the dataframe
# Parameter_combinations_asphalt['Number of samples (impact)'] = Number_samples
#
# # Add ECI as column to the dataframe
# Parameter_combinations_asphalt['ECI'] = Parameter_combinations_asphalt.apply(lambda row: ECIFunc.ECIAsphalt(row[
#     'Asphalt layer thickness'], row['Water level +mNAP'], row['slope asphalt']), axis=1)
#
# print(Parameter_combinations_asphalt)
# Parameter_combinations_asphalt.to_excel("AsphaltImpact_S14500000_21-7_Table(2.4-6.2mNAP).xlsx")


# ----------------------------------------------------------------------------------------------------------------------
# # ELEMENTS (Basalton)
# # Retrieve results from elements, Basalton
#
# Parameter_combinations_Basalton = Parameters.parameter_combinations_Basalton
# Number_samples = BasaltonFunc.nr_samples
# Probability_failure_Basalton = BasaltonFunc.Pf_Basalton
#
# # Add the Pf as a column to the dataframe
# Parameter_combinations_Basalton['Probability of failure Basalton'] = Probability_failure_Basalton
#
#
# # Add the Pf for the design lifetime to the dataframe
# Parameter_combinations_Basalton['Pf Basalton 50 year'] = pflifetime(
#     Parameter_combinations_Basalton['Probability of failure Basalton'])
#
# # Add the number of samples to the dataframe
# Parameter_combinations_Basalton['Number of samples'] = Number_samples
#
# # Add ECI as column to the dataframe
# Parameter_combinations_Basalton['ECI'] = Parameter_combinations_Basalton.apply(lambda row: ECIFunc.ECIBasalton(
#     row['Layer thickness Basalton'], row['Waterlevel +mNAP'], row['Slope angle']), axis=1)
#
# print(Parameter_combinations_Basalton)
# Parameter_combinations_Basalton.to_excel("Test Basalton 1.xlsx")

# ----------------------------------------------------------------------------------------------------------------------
# ELEMENTS (Verkalit)
# Retrieve results from elements, Verkalit

# Parameter_combinations_Verkalit = Parameters.parameter_combinations_Verkalit
# Number_samples = VerkalitFunc.nr_samples
# Probability_failure_Verkalit = VerkalitFunc.Pf_Verkalit
#
# # Add the Pf as a column to the dataframe
# Parameter_combinations_Verkalit['Probability of failure Verkalit'] = Probability_failure_Verkalit
#
# # Add the Pf for the design lifetime to the dataframe
# Parameter_combinations_Verkalit['Pf Verkalit 50 year'] = pflifetime(
#     Parameter_combinations_Verkalit['Probability of failure Verkalit'])
#
# # Add the number of samples to the dataframe
# Parameter_combinations_Verkalit['Number of samples'] = Number_samples
#
# # Add ECI as column to the dataframe
# Parameter_combinations_Verkalit['ECI'] = Parameter_combinations_Verkalit.apply(lambda row: ECIFunc.ECIVerkalit(
#     row['Layer thickness Verkalit'], row['Waterlevel +mNAP'], row['Slope angle']), axis=1)
#
# print(Parameter_combinations_Verkalit)
# Parameter_combinations_Verkalit.to_excel("Verkalit_S14500000_21-7_Table(1.8-2.4mNAP).xlsx")

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
