# This is where all results of the calculations from the ECI and revetment types are merged and one table is formed to be able to rank the designs.

import numpy as np
import openturns as ot
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as matplotlib
from Input.Parameters import Parameters
from ECI.ECI_class import ECIFunc
from ECI.ECI_Library import ECILib
import textwrap
import matplotlib.colors as mcolors

ot.Log.Show(ot.Log.NONE)


def maintenance_lr(diameter, ECI_main):
    amount_maintenance_year = 0.20
    # eens per drie jaar onderhoud
    design_lifetime = 50
    maintenance = diameter * ECI_main * amount_maintenance_year * design_lifetime
    return maintenance

def maintenance_LR_2(diameter, ECI_maintenance, S):
    Treshold_S = 6
    design_lifetime = 50
    frequency = 0.2
    maintenance = diameter * ECI_maintenance * (S / Treshold_S) * design_lifetime * frequency
    return maintenance


class ResultTableLooseRock:

    # Analysis of Loose Rock

    # print(Result_Raw)
    def filterresults(Result_Raw, selected_amount, Req_pf=1 / 60000):
        Result_filtered = Result_Raw[Result_Raw['Probability of failure'] < Req_pf]
        Result_sorted = Result_filtered.sort_values(['Waterlevel +mNAP', 'ECI'], ascending=[True, True])
        Result_grouped = Result_sorted.groupby('Waterlevel +mNAP').head(selected_amount)
        return Result_grouped

    ## Loose Rock
    Result_Raw_LR = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\1. Loose Rock\Result Loose Rock complete.xlsx')

    Result_Raw_LR['ECI_slopelength'] = Result_Raw_LR.apply(
        lambda row: ECIFunc.ECILooseRock(row['Nominal diameter rock'], 1.79, row['Slope angle'])
        if row['Damage number [S]'] <= 1
        else ECIFunc.ECILooseRock(row['Nominal diameter rock'], 1.79,
                                  row['Slope angle']) + maintenance_LR_2(
            row['Nominal diameter rock'], ECILib.ECI_LR_maintenance, row['Damage number [S]']), axis=1)


    # Result_Raw_LR.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\1. Loose Rock\Result raw with extra column.xlsx')

    # Add the stability number to the dataframe
    Result_Raw_LR['Stability number'] = Result_Raw_LR['Significant wave height'] / (((Result_Raw_LR['Density rock'] -
                                        Result_Raw_LR['Density water']) / Result_Raw_LR['Density water']) *
                                        Result_Raw_LR['Nominal diameter rock'])

    # Analysis for the original design

    Result_Raw_LR_S2 = Result_Raw_LR[Result_Raw_LR['Damage number [S]'] == 2]
    probability_of_failureS2 = Result_Raw_LR_S2['Probability of failure']
    stability_numberS2 = Result_Raw_LR_S2['Stability number']
    significant_wave_heightS2 = Result_Raw_LR_S2['Significant wave height']

    Result_Raw_LR_S6 = Result_Raw_LR[Result_Raw_LR['Damage number [S]'] == 6]
    probability_of_failureS6 = Result_Raw_LR_S6['Probability of failure']
    stability_numberS6 = Result_Raw_LR_S6['Stability number']
    significant_wave_heightS6 = Result_Raw_LR_S6['Significant wave height']

    Result_Raw_LR_S11 = Result_Raw_LR[Result_Raw_LR['Damage number [S]'] == 11]
    probability_of_failureS11 = Result_Raw_LR_S11['Probability of failure']
    stability_numberS11 = Result_Raw_LR_S11['Stability number']
    significant_wave_heightS11 = Result_Raw_LR_S11['Significant wave height']

    Result_Raw_LR_S17 = Result_Raw_LR[Result_Raw_LR['Damage number [S]'] == 17]
    probability_of_failureS17 = Result_Raw_LR_S17['Probability of failure']
    stability_numberS17 = Result_Raw_LR_S17['Stability number']
    significant_wave_heightS17 = Result_Raw_LR_S17['Significant wave height']

    # Result_Raw_LR_S2.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\RAW\Loose rock raw.xlsx')

    above_thresholdS2 = probability_of_failureS2 > 1/60000
    above_thresholdS6 = probability_of_failureS6 > 1/60000
    above_thresholdS11 = probability_of_failureS11 > 1/60000
    above_thresholdS17 = probability_of_failureS17 > 1/60000

    figure = plt.figure(figsize=(20, 10))
    font = {'size': 12}
    matplotlib.rc('font', **font)

    plt.subplot(2, 2, 1)
    # Plot_S2 = plt.scatter([Result_Raw_LR_S2['Stability number']], [Result_Raw_LR_S2['Significant wave height']],
    #                       c=[np.maximum(Result_Raw_LR_S2['Probability of failure'], 1e-7)], cmap='viridis', marker='o', label='S = 2',
    #                       norm=mcolors.LogNorm())
    Plot_S2 = plt.scatter(stability_numberS2, significant_wave_heightS2, c=probability_of_failureS2, cmap='viridis', marker='o',
                label='Pf < 1/60.000')
    Plot_S2 = plt.scatter(stability_numberS2[above_thresholdS2], significant_wave_heightS2[above_thresholdS2], c='red', marker='o',
                label='Pf > 1/60.000')

    # cbar = plt.colorbar(Plot_S2)
    # cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔDn50')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 5)
    plt.title(
        textwrap.fill('Probability of failure corresponding to the stability number and wave height for S = 2', 50),
        loc='center')
    plt.legend()

    plt.subplot(2, 2, 2)
    # Plot_S6 = plt.scatter([Result_Raw_LR_S6['Stability number']], [Result_Raw_LR_S6['Significant wave height']],
    #                       c=[np.maximum(Result_Raw_LR_S6['Probability of failure'], 1e-7)], cmap='viridis', marker='o', label='S = 6',
    #                       norm=mcolors.LogNorm())
    Plot_S6 = plt.scatter(stability_numberS6, significant_wave_heightS6, c=probability_of_failureS6, cmap='viridis', marker='o',
                label='Pf < 1/60.000')
    Plot_S6 = plt.scatter(stability_numberS6[above_thresholdS6], significant_wave_heightS6[above_thresholdS6], c='red', marker='o',
                label='Pf > 1/60.000')
    # cbar = plt.colorbar(Plot_S6)
    # cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔDn50')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 5)
    plt.title(
        textwrap.fill('Probability of failure corresponding to the stability number and wave height for S = 6', 50),
        loc='center')
    plt.legend()

    plt.subplot(2, 2, 3)
    # Plot_S11 = plt.scatter([Result_Raw_LR_S11['Stability number']], [Result_Raw_LR_S11['Significant wave height']],
    #                        c=[np.maximum(Result_Raw_LR_S11['Probability of failure'], 1e-7)], cmap='viridis', marker='o', label='S = 11',
    #                        norm=mcolors.LogNorm())
    Plot_S11 = plt.scatter(stability_numberS11, significant_wave_heightS11, c=probability_of_failureS11, cmap='viridis', marker='o',
                label='Pf < 1/60.000')
    Plot_S11 = plt.scatter(stability_numberS11[above_thresholdS11], significant_wave_heightS11[above_thresholdS11], c='red', marker='o',
                label='Pf > 1/60.000')

    # cbar = plt.colorbar(Plot_S11)
    # cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔDn50')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 5)
    plt.title(
        textwrap.fill('Probability of failure corresponding to the stability number and wave height for S = 11', 50),
        loc='center')
    plt.legend()

    plt.subplot(2, 2, 4)
    # Plot_S17 = plt.scatter([Result_Raw_LR_S17['Stability number']], [Result_Raw_LR_S17['Significant wave height']],
    #                        c=[np.maximum(Result_Raw_LR_S17['Probability of failure'], 1e-7)], cmap='viridis', marker='o', label='S = 17',
    #                        norm=mcolors.LogNorm())
    Plot_S17 = plt.scatter(stability_numberS17, significant_wave_heightS17, c=probability_of_failureS17, cmap='viridis', marker='o',
                label='Pf < 1/60.000')
    Plot_S17 = plt.scatter(stability_numberS17[above_thresholdS17], significant_wave_heightS17[above_thresholdS17], c='red', marker='o',
                label='Pf > 1/60.000')

    # cbar = plt.colorbar(Plot_S17)
    # cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔDn50')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 5)
    plt.title(
        textwrap.fill('Probability of failure corresponding to the stability number and wave height for S = 17', 50),
        loc='center')
    plt.legend()

    # plt.show()

    # ------------------------------------------------------------------------------------------------------------------
    ## Basalton
    Result_raw_Basalton = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\3. Basalton\Result Basalton complete.xlsx')
    Result_raw_Basalton['ECI_slopelength'] = ECIFunc.ECIBasalton(Result_raw_Basalton['Layer thickness Basalton'], 2.41,
                                                                 Result_raw_Basalton['Slope angle'])

    Result_raw_Basalton['Stability number'] = Result_raw_Basalton['Significant wave height'] / (((Result_raw_Basalton['Density concrete'] -
                                              1025) / 1025) *
                                              Result_raw_Basalton['Layer thickness Basalton'])

    Basalton_RAW_BAS_rho2650 = Result_raw_Basalton[Result_raw_Basalton['Density concrete'] == 2650]
    probability_of_failure2650 = Basalton_RAW_BAS_rho2650['Probability of failure']
    stability_number2650 = Basalton_RAW_BAS_rho2650['Stability number']
    significant_wave_height2650 = Basalton_RAW_BAS_rho2650['Significant wave height']

    Basalton_RAW_BAS_rho2750 = Result_raw_Basalton[Result_raw_Basalton['Density concrete'] == 2750]
    probability_of_failure2750 = Basalton_RAW_BAS_rho2650['Probability of failure']
    stability_number2750 = Basalton_RAW_BAS_rho2650['Stability number']
    significant_wave_height2750 = Basalton_RAW_BAS_rho2650['Significant wave height']

    Basalton_RAW_BAS_rho2850 = Result_raw_Basalton[Result_raw_Basalton['Density concrete'] == 2850]
    probability_of_failure2850 = Basalton_RAW_BAS_rho2650['Probability of failure']
    stability_number2850 = Basalton_RAW_BAS_rho2650['Stability number']
    significant_wave_height2850 = Basalton_RAW_BAS_rho2650['Significant wave height']

    Basalton_RAW_BAS_rho3000 = Result_raw_Basalton[Result_raw_Basalton['Density concrete'] == 3000]
    probability_of_failure3000 = Basalton_RAW_BAS_rho2650['Probability of failure']
    stability_number3000 = Basalton_RAW_BAS_rho2650['Stability number']
    significant_wave_height3000 = Basalton_RAW_BAS_rho2650['Significant wave height']

    above_threshold2650 = probability_of_failure2650 > 1/60000
    above_threshold2750 = probability_of_failure2750 > 1/60000
    above_threshold2850 = probability_of_failure2850 > 1/60000
    above_threshold3000 = probability_of_failure3000 > 1/60000

    figure = plt.figure(figsize=(20, 10))
    font = {'size': 12}
    matplotlib.rc('font', **font)

    plt.subplot(2, 2, 1)
    Plot_S2 = plt.scatter(stability_number2650, significant_wave_height2650, c=probability_of_failure2650, cmap='viridis', marker='o',
                label='Pf < 1/60.000')
    Plot_S2 = plt.scatter(stability_number2650[above_threshold2650], significant_wave_height2650[above_threshold2650], c='red', marker='o',
                label='Pf > 1/60.000')

    # cbar = plt.colorbar(Plot_S2)
    # cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔD')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 8)
    plt.title(
        textwrap.fill('Probability of failure Basalton corresponding to the stability number and wave height for density of concrete 2650 kg/m3', 50),
        loc='center')
    plt.legend()

    plt.subplot(2, 2, 2)
    Plot_S6 = plt.scatter(stability_number2750, significant_wave_height2750, c=probability_of_failure2750, cmap='viridis', marker='o',
                label='S = 2')
    Plot_S6 = plt.scatter(stability_number2750[above_threshold2750], significant_wave_height2750[above_threshold2750], c='red', marker='o',
                label='S = 2 (Above Threshold)')

    # cbar = plt.colorbar(Plot_S6)
    # cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔD')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 8)
    plt.title(
        textwrap.fill('Probability of failure Basalton corresponding to the stability number and wave height for density of concrete 2750 kg/m3', 50),
        loc='center')

    plt.subplot(2, 2, 3)
    Plot_S11 = plt.scatter(stability_number2850, significant_wave_height2850, c=probability_of_failure2850, cmap='viridis', marker='o',
                label='S = 2')
    Plot_S11 = plt.scatter(stability_number2850[above_threshold2850], significant_wave_height2850[above_threshold2850], c='red', marker='o',
                label='S = 2 (Above Threshold)')

    # cbar = plt.colorbar(Plot_S11)
    # cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔD')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 8)
    plt.title(
        textwrap.fill('Probability of failure Basalton corresponding to the stability number and wave height for density of concrete 2850 kg/m3', 50),
        loc='center')
    plt.legend()

    plt.subplot(2, 2, 4)
    Plot_S17 = plt.scatter(stability_number3000, significant_wave_height3000, c=probability_of_failure3000, cmap='viridis', marker='o',
                label='S = 2')
    Plot_S17 = plt.scatter(stability_number3000[above_threshold3000], significant_wave_height3000[above_threshold3000], c='red', marker='o',
                label='S = 2 (Above Threshold)')

    # cbar = plt.colorbar(Plot_S17)
    # cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔD')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 8)
    plt.title(
        textwrap.fill('Probability of failure Basalton corresponding to the stability number and wave height for density of concrete 3000 kg/m3', 50),
        loc='center')
    plt.legend()

    # plt.show()
    #
    # print(Basalton_RAW_BAS_rho2650)
    # Basalton_filtered.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\3. Basalton\Filtered result table Basalton.xlsx')

    # ------------------------------------------------------------------------------------------------------------------
    ## Verkalit
    Result_raw_Verkalit = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\2. Verkalit\Result Verkalit complete.xlsx')
    Result_raw_Verkalit['ECI_slopelength'] = ECIFunc.ECIVerkalit(Result_raw_Verkalit['Layer thickness Verkalit'], 2.41,
                                                                 Result_raw_Verkalit['Slope angle'])

    Result_raw_Verkalit['Stability number'] = Result_raw_Verkalit['Significant wave height'] / (
                ((Result_raw_Verkalit['Density concrete'] -
                  1025) / 1025) *
                Result_raw_Verkalit['Layer thickness Verkalit'])

    Verkalit_RAW_Ver_rho2650 = Result_raw_Verkalit[Result_raw_Verkalit['Density concrete'] == 2650]
    probability_of_failure2650 = Verkalit_RAW_Ver_rho2650['Probability of failure']
    stability_number2650 = Verkalit_RAW_Ver_rho2650['Stability number']
    significant_wave_height2650 = Verkalit_RAW_Ver_rho2650['Significant wave height']

    Verkalit_RAW_Ver_rho2750 = Result_raw_Verkalit[Result_raw_Verkalit['Density concrete'] == 2750]
    probability_of_failure2750 = Verkalit_RAW_Ver_rho2650['Probability of failure']
    stability_number2750 = Verkalit_RAW_Ver_rho2650['Stability number']
    significant_wave_height2750 = Verkalit_RAW_Ver_rho2650['Significant wave height']

    Verkalit_RAW_Ver_rho2850 = Result_raw_Verkalit[Result_raw_Verkalit['Density concrete'] == 2850]
    probability_of_failure2850 = Verkalit_RAW_Ver_rho2650['Probability of failure']
    stability_number2850 = Verkalit_RAW_Ver_rho2650['Stability number']
    significant_wave_height2850 = Verkalit_RAW_Ver_rho2650['Significant wave height']

    Verkalit_RAW_Ver_rho3000 = Result_raw_Verkalit[Result_raw_Verkalit['Density concrete'] == 3000]
    probability_of_failure3000 = Verkalit_RAW_Ver_rho2650['Probability of failure']
    stability_number3000 = Verkalit_RAW_Ver_rho2650['Stability number']
    significant_wave_height3000 = Verkalit_RAW_Ver_rho2650['Significant wave height']

    above_threshold2650 = probability_of_failure2650 > 1 / 60000
    above_threshold2750 = probability_of_failure2750 > 1 / 60000
    above_threshold2850 = probability_of_failure2850 > 1 / 60000
    above_threshold3000 = probability_of_failure3000 > 1 / 60000

    figure = plt.figure(figsize=(20, 10))
    font = {'size': 12}
    matplotlib.rc('font', **font)

    plt.subplot(2, 2, 1)
    Plot_S2 = plt.scatter(stability_number2650, significant_wave_height2650, c=probability_of_failure2650,
                          cmap='viridis', marker='o',
                          label='Pf < 1/60.000')
    Plot_S2 = plt.scatter(stability_number2650[above_threshold2650], significant_wave_height2650[above_threshold2650],
                          c='red', marker='o',
                          label='Pf > 1/60.000')

    # cbar = plt.colorbar(Plot_S2)
    # cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔD')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 8)
    plt.title(
        textwrap.fill(
            'Probability of failure Verkalit corresponding to the stability number and wave height for density of concrete 2650 kg/m3',
            50),
        loc='center')
    plt.legend()

    plt.subplot(2, 2, 2)
    Plot_S6 = plt.scatter(stability_number2750, significant_wave_height2750, c=probability_of_failure2750,
                          cmap='viridis', marker='o',
                          label='S = 2')
    Plot_S6 = plt.scatter(stability_number2750[above_threshold2750], significant_wave_height2750[above_threshold2750],
                          c='red', marker='o',
                          label='S = 2 (Above Threshold)')

    # cbar = plt.colorbar(Plot_S6)
    # cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔD')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 8)
    plt.title(
        textwrap.fill(
            'Probability of failure Verkalit corresponding to the stability number and wave height for density of concrete 2750 kg/m3',
            50),
        loc='center')
    plt.legend()

    plt.subplot(2, 2, 3)
    Plot_S11 = plt.scatter(stability_number2850, significant_wave_height2850, c=probability_of_failure2850,
                           cmap='viridis', marker='o',
                           label='S = 2')
    Plot_S11 = plt.scatter(stability_number2850[above_threshold2850], significant_wave_height2850[above_threshold2850],
                           c='red', marker='o',
                           label='S = 2 (Above Threshold)')

    # cbar = plt.colorbar(Plot_S11)
    # cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔD')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 8)
    plt.title(
        textwrap.fill(
            'Probability of failure Verkalit corresponding to the stability number and wave height for density of concrete 2850 kg/m3',
            50),
        loc='center')
    plt.legend()

    plt.subplot(2, 2, 4)
    Plot_S17 = plt.scatter(stability_number3000, significant_wave_height3000, c=probability_of_failure3000,
                           cmap='viridis', marker='o',
                           label='S = 2')
    Plot_S17 = plt.scatter(stability_number3000[above_threshold3000], significant_wave_height3000[above_threshold3000],
                           c='red', marker='o',
                           label='S = 2 (Above Threshold)')

    # cbar = plt.colorbar(Plot_S17)
    # cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔD')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 8)
    plt.title(
        textwrap.fill(
            'Probability of failure Verkalit corresponding to the stability number and wave height for density of concrete 3000 kg/m3',
            50),
        loc='center')
    plt.legend()

    # plt.show()
    #
    # print(Verkalit_RAW_Ver_rho2650)

    # ------------------------------------------------------------------------------------------------------------------
    ## Asphalt
    Result_raw_Asphalt = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\4. Asphalt\Result Asphalt complete.xlsx')

    # Result_raw_Asphalt_d10 = Result_raw_Asphalt[Result_raw_Asphalt['Density concrete'] == 0.1]
    # Result_raw_Asphalt_d15 = Result_raw_Asphalt[Result_raw_Asphalt['Density concrete'] == 0.15]
    # Result_raw_Asphalt_d20 = Result_raw_Asphalt[Result_raw_Asphalt['Density concrete'] == 0.2]
    # Result_raw_Asphalt_d25 = Result_raw_Asphalt[Result_raw_Asphalt['Density concrete'] == 0.25]

    probability_of_failure = Result_raw_Asphalt['Probability of failure']
    Asphalt_layer_thickness = Result_raw_Asphalt['Asphalt layer thickness']
    significant_wave_height = Result_raw_Asphalt['Significant wave height']
    waterlevel_uplift = Result_raw_Asphalt['Waterlevel +mNAP']

    above_threshold = probability_of_failure > 1 / 60000

    figure = plt.figure(figsize=(20, 10))
    font = {'size': 12}
    matplotlib.rc('font', **font)

    # Plot_S2 = plt.scatter([Result_raw_Asphalt['Asphalt layer thickness']],
    #                       [Result_raw_Asphalt['Significant wave height']],
    #                       c=[np.maximum(Result_raw_Asphalt['Probability of failure'], 1e-7)], cmap='viridis',
    #                       marker='o', label='S = 2',
    #                       norm=mcolors.LogNorm())

    Plot_S2 = plt.scatter(Asphalt_layer_thickness, waterlevel_uplift, c=probability_of_failure,
                          cmap='viridis', marker='o',
                          label='Pf < 1/60.000')
    Plot_S2 = plt.scatter(Asphalt_layer_thickness[above_threshold], waterlevel_uplift[above_threshold],
                          c='red', marker='o',
                          label='Pf > 1/60.000')

    # cbar = plt.colorbar(Plot_S2)
    # cbar.set_label('Probability of Failure')
    plt.xlabel('Layer thickness, d [m]')
    plt.ylabel('Waterlevel, [mNAP]')
    plt.ylim(1.2, 7)
    plt.xlim(0, 0.5)
    plt.title(
        textwrap.fill(
            'Probability of failure Asphalt corresponding to the layer thickness and water level', 50),
        loc='center')
    plt.legend()

    # Uplift
    probability_of_failure_uplift = Result_raw_Asphalt['Pf uplift']
    waterlevel_uplift = Result_raw_Asphalt['Waterlevel +mNAP']

    above_threshold_uplift = probability_of_failure_uplift > 1 / 60000

    figure = plt.figure(figsize=(20, 10))
    font = {'size': 12}
    matplotlib.rc('font', **font)

    # Plot_S2 = plt.scatter([Result_raw_Asphalt['Asphalt layer thickness']],
    #                       [Result_raw_Asphalt['Waterlevel +mNAP']],
    #                       c=[np.maximum(Result_raw_Asphalt['Pf uplift'], 1e-7)], cmap='viridis',
    #                       marker='o',
    #                       norm=mcolors.LogNorm())

    Plot_S2 = plt.scatter(Asphalt_layer_thickness, waterlevel_uplift, c=probability_of_failure_uplift,
                          cmap='viridis', marker='o',
                          label='Pf < 1/60.000')
    Plot_S2 = plt.scatter(Asphalt_layer_thickness[above_threshold_uplift], waterlevel_uplift[above_threshold_uplift],
                          c='red', marker='o',
                          label='Pf > 1/60.000')

    # cbar = plt.colorbar(Plot_S2)
    # cbar.set_label('Probability of Failure')
    plt.xlabel('Layer thickness, d [m]')
    plt.ylabel('Waterlevel, [mNAP]')
    plt.ylim(1.2, 7)
    plt.xlim(0, 0.5)
    plt.title(
        textwrap.fill(
            'Probability of failure Asphalt due to uplift corresponding to the layer thickness and water level', 50),
        loc='center')
    plt.legend()

    # Uplift and impact

    probability_of_failure_combined = Result_raw_Asphalt['Probability of failure2']
    above_threshold_combined = probability_of_failure_combined > 1 / 60000


    figure = plt.figure(figsize=(20, 10))
    font = {'size': 12}
    matplotlib.rc('font', **font)

    # Plot_S2 = plt.scatter([Result_raw_Asphalt['Asphalt layer thickness']],
    #                       [Result_raw_Asphalt['Significant wave height']],
    #                       c=[np.maximum(Result_raw_Asphalt['Probability of failure2'], 1e-7)], cmap='viridis',
    #                       marker='o',
    #                       norm=mcolors.LogNorm())

    Plot_S2 = plt.scatter(Asphalt_layer_thickness, waterlevel_uplift, c=probability_of_failure_combined,
                          cmap='viridis', marker='o',
                          label='Pf < 1/60.000')
    Plot_S2 = plt.scatter(Asphalt_layer_thickness[above_threshold_combined], waterlevel_uplift[above_threshold_combined],
                          c='red', marker='o',
                          label='Pf > 1/60.000')

    # cbar = plt.colorbar(Plot_S2)
    # cbar.set_label('Probability of Failure')
    plt.xlabel('Layer thickness, d [m]')
    plt.ylabel('Waterlevel, [mNAP]')
    plt.ylim(1.2, 7)
    plt.xlim(0, 0.5)
    plt.title(
        textwrap.fill(
            'Probability of failure Asphalt for both wave impact and uplift corresponding to the layer thickness and water level', 50),
        loc='center')
    plt.legend()

    plt.show()
    # print(Result_raw_Asphalt)

    # ------------------------------------------------------------------------------------------------------------------
    ## Grass
    Result_Grass = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\5. Grass\GEBU results.xlsx',
        usecols='A:C', nrows=23)

    Result_Grass['ECI'] = ECIFunc.ECIGrass(Result_Grass['clay layer thickness'],
                                           Result_Grass['Transition height asphalt-grass (+mNAP)'])
    # print(Result_Grass)

    figure = plt.figure()
    x = np.arange(len(Result_Grass['clay layer thickness']))
    plt.bar(x, Result_Grass['ECI'], color='mediumseagreen', width=0.2, label='ECI clay')
    plt.xticks(x, Result_Grass['clay layer thickness'])
    plt.xlabel('clay layer thickness (m)')
    plt.ylabel('ECI (€)')
    plt.ylim(0, 220)
    plt.title(textwrap.fill('ECI for each clay layer thickness including the transition height', 50), loc='center')
    # Add y-values to the bars
    for i, v in enumerate(Result_Grass['ECI']):
        if v != 0:
            plt.text(i, v, f'ECI: {v:.1f}\n', color='b', ha='center')
    plt.legend(loc='upper left')
    # Add line graph with water level
    ax2 = plt.twinx()
    ax2.plot(x, Result_Grass['Transition height asphalt-grass (+mNAP)'], color='r', linestyle='-', marker='o',
             label='Transition height')
    ax2.set_ylabel('Transition height asphalt-grass (+mNAP)')



    plt.legend(loc='upper right')

    # plt.show()

    # Result_Grass.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\5. Grass\Result table Grass.xlsx')
