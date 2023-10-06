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
    Result_Raw_LR_S6 = Result_Raw_LR[Result_Raw_LR['Damage number [S]'] == 6]
    Result_Raw_LR_S11 = Result_Raw_LR[Result_Raw_LR['Damage number [S]'] == 11]
    Result_Raw_LR_S17 = Result_Raw_LR[Result_Raw_LR['Damage number [S]'] == 17]
    # Result_Raw_LR_S2.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\RAW\Loose rock raw.xlsx')


    figure = plt.figure(figsize=(20, 10))
    font = {'size': 12}
    matplotlib.rc('font', **font)

    plt.subplot(2, 2, 1)
    Plot_S2 = plt.scatter([Result_Raw_LR_S2['Stability number']], [Result_Raw_LR_S2['Significant wave height']],
                          c=[np.maximum(Result_Raw_LR_S2['Probability of failure'], 1e-7)], cmap='viridis', marker='o', label='S = 2',
                          norm=mcolors.LogNorm())
    cbar = plt.colorbar(Plot_S2)
    cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔDn50')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 5)
    plt.title(
        textwrap.fill('Probability of failure corresponding to the stability number and wave height for S = 2', 50),
        loc='center')

    plt.subplot(2, 2, 2)
    Plot_S6 = plt.scatter([Result_Raw_LR_S6['Stability number']], [Result_Raw_LR_S6['Significant wave height']],
                          c=[np.maximum(Result_Raw_LR_S6['Probability of failure'], 1e-7)], cmap='viridis', marker='s', label='S = 6',
                          norm=mcolors.LogNorm())
    cbar = plt.colorbar(Plot_S6)
    cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔDn50')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 5)
    plt.title(
        textwrap.fill('Probability of failure corresponding to the stability number and wave height for S = 6', 50),
        loc='center')

    plt.subplot(2, 2, 3)
    Plot_S11 = plt.scatter([Result_Raw_LR_S11['Stability number']], [Result_Raw_LR_S11['Significant wave height']],
                           c=[np.maximum(Result_Raw_LR_S11['Probability of failure'], 1e-7)], cmap='viridis', marker='^', label='S = 11',
                           norm=mcolors.LogNorm())
    cbar = plt.colorbar(Plot_S11)
    cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔDn50')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 5)
    plt.title(
        textwrap.fill('Probability of failure corresponding to the stability number and wave height for S = 11', 50),
        loc='center')

    plt.subplot(2, 2, 4)
    Plot_S17 = plt.scatter([Result_Raw_LR_S17['Stability number']], [Result_Raw_LR_S17['Significant wave height']],
                           c=[np.maximum(Result_Raw_LR_S17['Probability of failure'], 1e-7)], cmap='viridis', marker='*', label='S = 17',
                           norm=mcolors.LogNorm())
    cbar = plt.colorbar(Plot_S17)
    cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔDn50')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 5)
    plt.title(
        textwrap.fill('Probability of failure corresponding to the stability number and wave height for S = 17', 50),
        loc='center')

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
    Basalton_RAW_BAS_rho2750 = Result_raw_Basalton[Result_raw_Basalton['Density concrete'] == 2750]
    Basalton_RAW_BAS_rho2850 = Result_raw_Basalton[Result_raw_Basalton['Density concrete'] == 2850]
    Basalton_RAW_BAS_rho3000 = Result_raw_Basalton[Result_raw_Basalton['Density concrete'] == 3000]

    figure = plt.figure(figsize=(20, 10))
    font = {'size': 12}
    matplotlib.rc('font', **font)

    plt.subplot(2, 2, 1)
    Plot_S2 = plt.scatter([Basalton_RAW_BAS_rho2650['Stability number']], [Basalton_RAW_BAS_rho2650['Significant wave height']],
                          c=[np.maximum(Basalton_RAW_BAS_rho2650['Probability of failure'], 1e-7)], cmap='viridis', marker='o', label='S = 2',
                          norm=mcolors.LogNorm())
    cbar = plt.colorbar(Plot_S2)
    cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔD')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 8)
    plt.title(
        textwrap.fill('Probability of failure Basalton corresponding to the stability number and wave height for density of concrete 2650 kg/m3', 50),
        loc='center')

    plt.subplot(2, 2, 2)
    Plot_S6 = plt.scatter([Basalton_RAW_BAS_rho2750['Stability number']], [Basalton_RAW_BAS_rho2750['Significant wave height']],
                          c=[np.maximum(Basalton_RAW_BAS_rho2750['Probability of failure'], 1e-7)], cmap='viridis', marker='s', label='S = 6',
                          norm=mcolors.LogNorm())
    cbar = plt.colorbar(Plot_S6)
    cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔD')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 8)
    plt.title(
        textwrap.fill('Probability of failure Basalton corresponding to the stability number and wave height for density of concrete 2750 kg/m3', 50),
        loc='center')

    plt.subplot(2, 2, 3)
    Plot_S11 = plt.scatter([Basalton_RAW_BAS_rho2850['Stability number']], [Basalton_RAW_BAS_rho2850['Significant wave height']],
                           c=[np.maximum(Basalton_RAW_BAS_rho2850['Probability of failure'], 1e-7)], cmap='viridis', marker='^', label='S = 11',
                           norm=mcolors.LogNorm())
    cbar = plt.colorbar(Plot_S11)
    cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔD')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 8)
    plt.title(
        textwrap.fill('Probability of failure Basalton corresponding to the stability number and wave height for density of concrete 2850 kg/m3', 50),
        loc='center')

    plt.subplot(2, 2, 4)
    Plot_S17 = plt.scatter([Basalton_RAW_BAS_rho3000['Stability number']], [Basalton_RAW_BAS_rho3000['Significant wave height']],
                           c=[np.maximum(Basalton_RAW_BAS_rho3000['Probability of failure'], 1e-7)], cmap='viridis', marker='*', label='S = 17',
                           norm=mcolors.LogNorm())
    cbar = plt.colorbar(Plot_S17)
    cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔD')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 8)
    plt.title(
        textwrap.fill('Probability of failure Basalton corresponding to the stability number and wave height for density of concrete 3000 kg/m3', 50),
        loc='center')

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
    Verkalit_RAW_Ver_rho2750 = Result_raw_Verkalit[Result_raw_Verkalit['Density concrete'] == 2750]
    Verkalit_RAW_Ver_rho2850 = Result_raw_Verkalit[Result_raw_Verkalit['Density concrete'] == 2850]
    Verkalit_RAW_Ver_rho3000 = Result_raw_Verkalit[Result_raw_Verkalit['Density concrete'] == 3000]

    figure = plt.figure(figsize=(20, 10))
    font = {'size': 12}
    matplotlib.rc('font', **font)

    plt.subplot(2, 2, 1)
    Plot_S2 = plt.scatter([Verkalit_RAW_Ver_rho2650['Stability number']],
                          [Verkalit_RAW_Ver_rho2650['Significant wave height']],
                          c=[np.maximum(Verkalit_RAW_Ver_rho2650['Probability of failure'], 1e-7)], cmap='viridis',
                          marker='o', label='S = 2',
                          norm=mcolors.LogNorm())
    cbar = plt.colorbar(Plot_S2)
    cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔD')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 8)
    plt.title(
        textwrap.fill(
            'Probability of failure Verkalit corresponding to the stability number and wave height for density of concrete 2650 kg/m3',
            50),
        loc='center')

    plt.subplot(2, 2, 2)
    Plot_S6 = plt.scatter([Verkalit_RAW_Ver_rho2750['Stability number']],
                          [Verkalit_RAW_Ver_rho2750['Significant wave height']],
                          c=[np.maximum(Verkalit_RAW_Ver_rho2750['Probability of failure'], 1e-7)], cmap='viridis',
                          marker='s', label='S = 6',
                          norm=mcolors.LogNorm())
    cbar = plt.colorbar(Plot_S6)
    cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔD')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 8)
    plt.title(
        textwrap.fill(
            'Probability of failure Verkalit corresponding to the stability number and wave height for density of concrete 2750 kg/m3',
            50),
        loc='center')

    plt.subplot(2, 2, 3)
    Plot_S11 = plt.scatter([Verkalit_RAW_Ver_rho2850['Stability number']],
                           [Verkalit_RAW_Ver_rho2850['Significant wave height']],
                           c=[np.maximum(Verkalit_RAW_Ver_rho2850['Probability of failure'], 1e-7)], cmap='viridis',
                           marker='^', label='S = 11',
                           norm=mcolors.LogNorm())
    cbar = plt.colorbar(Plot_S11)
    cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔD')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 8)
    plt.title(
        textwrap.fill(
            'Probability of failure Verkalit corresponding to the stability number and wave height for density of concrete 2850 kg/m3',
            50),
        loc='center')

    plt.subplot(2, 2, 4)
    Plot_S17 = plt.scatter([Verkalit_RAW_Ver_rho3000['Stability number']],
                           [Verkalit_RAW_Ver_rho3000['Significant wave height']],
                           c=[np.maximum(Verkalit_RAW_Ver_rho3000['Probability of failure'], 1e-7)], cmap='viridis',
                           marker='*', label='S = 17',
                           norm=mcolors.LogNorm())
    cbar = plt.colorbar(Plot_S17)
    cbar.set_label('Probability of Failure')
    plt.xlabel('Stability number Hs/ΔD')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 3)
    plt.xlim(0, 8)
    plt.title(
        textwrap.fill(
            'Probability of failure Verkalit corresponding to the stability number and wave height for density of concrete 3000 kg/m3',
            50),
        loc='center')

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

    figure = plt.figure(figsize=(20, 10))
    font = {'size': 12}
    matplotlib.rc('font', **font)

    Plot_S2 = plt.scatter([Result_raw_Asphalt['Asphalt layer thickness']],
                          [Result_raw_Asphalt['Significant wave height']],
                          c=[np.maximum(Result_raw_Asphalt['Probability of failure'], 1e-7)], cmap='viridis',
                          marker='o', label='S = 2',
                          norm=mcolors.LogNorm())
    cbar = plt.colorbar(Plot_S2)
    cbar.set_label('Probability of Failure')
    plt.xlabel('Layer thickness, d [m]')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 2.5)
    plt.xlim(0, 0.5)
    plt.title(
        textwrap.fill(
            'Probability of failure Asphalt corresponding to the layer thickness and wave height', 50),
        loc='center')

    # Uplift
    figure = plt.figure(figsize=(20, 10))
    font = {'size': 12}
    matplotlib.rc('font', **font)

    Plot_S2 = plt.scatter([Result_raw_Asphalt['Asphalt layer thickness']],
                          [Result_raw_Asphalt['Waterlevel +mNAP']],
                          c=[np.maximum(Result_raw_Asphalt['Pf uplift'], 1e-7)], cmap='viridis',
                          marker='o',
                          norm=mcolors.LogNorm())
    cbar = plt.colorbar(Plot_S2)
    cbar.set_label('Probability of Failure')
    plt.xlabel('Layer thickness, d [m]')
    plt.ylabel('Waterlevel, [mNAP]')
    plt.ylim(1.2, 7)
    plt.xlim(0, 0.5)
    plt.title(
        textwrap.fill(
            'Probability of failure Asphalt due to uplift corresponding to the layer thickness and water level', 50),
        loc='center')

    # Uplift and impact
    # Uplift
    figure = plt.figure(figsize=(20, 10))
    font = {'size': 12}
    matplotlib.rc('font', **font)

    Plot_S2 = plt.scatter([Result_raw_Asphalt['Asphalt layer thickness']],
                          [Result_raw_Asphalt['Significant wave height']],
                          c=[np.maximum(Result_raw_Asphalt['Probability of failure2'], 1e-7)], cmap='viridis',
                          marker='o',
                          norm=mcolors.LogNorm())
    cbar = plt.colorbar(Plot_S2)
    cbar.set_label('Probability of Failure')
    plt.xlabel('Layer thickness, d [m]')
    plt.ylabel('Significant wave height, Hs [m]')
    plt.ylim(0.8, 2.5)
    plt.xlim(0, 0.5)
    plt.title(
        textwrap.fill(
            'Probability of failure Asphalt for both wave impact and uplift corresponding to the layer thickness and wave height', 50),
        loc='center')

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
