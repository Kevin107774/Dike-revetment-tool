# This is where all results of the calculations from the ECI and revetment types are merged and one table is formed to be able to rank the designs.

import numpy as np
import openturns as ot
import pandas as pd
import matplotlib.pyplot as plt
from Input.Parameters import Parameters
from ECI.ECI_class import ECIFunc
from ECI.ECI_Library import ECILib
import textwrap

ot.Log.Show(ot.Log.NONE)


def maintenance_lr(diameter, ECI_main):
    amount_maintenance_year = 0.20
    # eens per drie jaar onderhoud
    design_lifetime = 50
    maintenance = diameter * ECI_main * amount_maintenance_year * design_lifetime
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
        if row['Damage number [S]'] <= 5
        else ECIFunc.ECILooseRock(row['Nominal diameter rock'], 1.79,
                                  row['Slope angle']) + maintenance_lr(
            row['Nominal diameter rock'], ECILib.ECI_LR_maintenance), axis=1)

    # Result_Raw_LR.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\1. Loose Rock\Result raw with extra column.xlsx')

    # Analysis for the original design

    Loose_rock_selection = Result_Raw_LR[Result_Raw_LR['Probability of failure'] < 1 / 60000]
    Loose_rock_selection = Loose_rock_selection[Loose_rock_selection['Waterlevel +mNAP'] < 1.8]
    Loose_rock_selection = Loose_rock_selection.sort_values(
        ['Nominal diameter rock', 'Damage number [S]', 'ECI_slopelength'],
        ascending=[True, True, True])

    # Without maintenance (S<5)
    Loose_rock_selection_low = Loose_rock_selection[Loose_rock_selection['Damage number [S]'] < 5]
    Loose_rock_selection_low = Loose_rock_selection_low.groupby('Nominal diameter rock').head(1)
    # Create a new row filled with zeros for the graph
    new_row = pd.DataFrame([[0] * len(Loose_rock_selection_low.columns)], columns=Loose_rock_selection_low.columns)
    Loose_rock_selection_low = pd.concat([new_row, Loose_rock_selection_low], ignore_index=True)

    # With maintenance (S>5)
    Loose_rock_selection_high = Loose_rock_selection[Loose_rock_selection['Damage number [S]'] > 5]
    Loose_rock_selection_high = Loose_rock_selection_high.groupby('Nominal diameter rock').head(1)
    # print(Loose_rock_selection_low)
    # Loose_rock_selection.to_excel(
    #     r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\1. Loose Rock\Selection original design.xlsx')

    figure = plt.figure()
    x = np.arange(len(Loose_rock_selection_high['Nominal diameter rock']))
    plt.bar(x - 0.1, Loose_rock_selection_low['ECI_slopelength'], color='b', width=0.2, label='Without maintenance')
    plt.bar(x + 0.1, Loose_rock_selection_high['ECI_slopelength'], color='r', width=0.2, label='With maintenance')
    labels_x = ['HMa 300-1000', 'HMa 1000-3000', 'HMa 3000-6000', 'HMa 6000-10000']
    plt.xticks(x, labels_x)
    plt.xlabel('Rock class (kg)')
    plt.ylabel('ECI (€)')
    plt.ylim(0, 170)
    plt.title(textwrap.fill('ECI for each nominal diameter rock with (S>5) and without maintenance (S≤5)', 50),
              loc='center')
    plt.legend(loc='upper left')

    # Add y-values to the bars
    for i, v in enumerate(Loose_rock_selection_low['ECI_slopelength']):
        if v != 0:
            plt.text(i - 0.1, v + 0.1, f'ECI: {v:.1f}\nS: {Loose_rock_selection_low["Damage number [S]"].iloc[i]}',
                     color='b', ha='center')
    for i, v in enumerate(Loose_rock_selection_high['ECI_slopelength']):
        if v != 0:
            plt.text(i + 0.1, v + 1, f'ECI: {v:.1f}\nS: {Loose_rock_selection_high["Damage number [S]"].iloc[i]}',
                     color='r', ha='center')
    plt.show()

    # Analysis for the transition heights
    Loose_rock_filtered = filterresults(Result_Raw_LR, 2)
    # print(Loose_rock_selection)
    # Loose_rock_selection.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\1. Loose Rock\Filtered result table Loose rock.xlsx')

    # ------------------------------------------------------------------------------------------------------------------
    ## Basalton
    Result_raw_Basalton = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\3. Basalton\Result Basalton complete.xlsx')
    Result_raw_Basalton['ECI_slopelength'] = ECIFunc.ECIBasalton(Result_raw_Basalton['Layer thickness Basalton'], 2.41,
                                                                 Result_raw_Basalton['Slope angle'])
    # print(Result_raw_Basalton)
    # Result_raw_Basalton.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\3. Basalton\Raw for original design Basalton.xlsx')

    Basalton_selection = Result_raw_Basalton[Result_raw_Basalton['Probability of failure'] < 1 / 60000]
    Basalton_selection = Basalton_selection[Basalton_selection['Waterlevel +mNAP'] == 2.4]
    # Basalton_selection = Basalton_selection[Basalton_selection['Waterlevel +mNAP'] < 2.6]
    Basalton_selection = Basalton_selection.sort_values(
        ['Layer thickness Basalton', 'ECI_slopelength'], ascending=[True, True])

    Basalton_selection = Basalton_selection.groupby('Layer thickness Basalton').head(1)
    # print(Basalton_selection)
    # Basalton_selection.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\3. Basalton\Selection original design Basalton.xlsx')

    Basalton_filtered = filterresults(Result_raw_Basalton, 5)
    # print(Basalton_filtered)
    # Basalton_filtered.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\3. Basalton\Filtered result table Basalton.xlsx')

    # ------------------------------------------------------------------------------------------------------------------
    ## Verkalit
    Result_raw_Verkalit = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\2. Verkalit\Result Verkalit complete.xlsx')
    Result_raw_Verkalit['ECI_slopelength'] = ECIFunc.ECIVerkalit(Result_raw_Verkalit['Layer thickness Verkalit'], 2.41,
                                                                 Result_raw_Verkalit['Slope angle'])
    # print(Result_raw_Verkalit)
    # Result_raw_Verkalit.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\2. Verkalit\Raw for original design Verkalit.xlsx')

    Verkalit_selection = Result_raw_Verkalit[Result_raw_Verkalit['Probability of failure'] < 1 / 60000]
    Verkalit_selection = Verkalit_selection[Verkalit_selection['Waterlevel +mNAP'] == 2.4]
    # Verkalit_selection = Verkalit_selection[Verkalit_selection['Waterlevel +mNAP'] < 2.6]
    Verkalit_selection = Verkalit_selection.sort_values(
        ['Layer thickness Verkalit', 'ECI_slopelength'], ascending=[True, True])

    Verkalit_selection = Verkalit_selection.groupby('Layer thickness Verkalit').head(1)
    new_row = pd.DataFrame([[0] * len(Verkalit_selection.columns)], columns=Verkalit_selection.columns)
    Verkalit_selection = pd.concat([new_row, Verkalit_selection], ignore_index=True)
    # print(Verkalit_selection)
    # Verkalit_selection.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\2. Verkalit\Selection original design Verkalit.xlsx')

    figure = plt.figure()
    x = np.arange(len(Basalton_selection['Layer thickness Basalton']))
    plt.bar(x - 0.1, Basalton_selection['ECI_slopelength'], color='b', width=0.2, label='Basalton')
    plt.bar(x + 0.1, Verkalit_selection['ECI_slopelength'], color='r', width=0.2, label='Verkalit')
    plt.xticks(x, Basalton_selection['Layer thickness Basalton'])
    plt.xlabel('Element thickness placed revetment (m)')
    plt.ylabel('ECI (€)')
    plt.ylim(0, 100)
    plt.title(textwrap.fill('ECI per element thickness Basalton and Verkalit', 50),
              loc='center')
    plt.legend(loc='upper left')

    # Add y-values to the bars
    for i, v in enumerate(Basalton_selection['ECI_slopelength']):
        if v != 0:
            plt.text(i - 0.1, v + 1, f'ECI: {v:.1f}\nρ: {Basalton_selection["Density concrete"].iloc[i]}',
                     color='b', ha='center')

    for i, v in enumerate(Verkalit_selection['ECI_slopelength']):
        if v != 0:
            plt.text(i + 0.1, v + 1, f'ECI: {v:.1f}\nρ: {Verkalit_selection["Density concrete"].iloc[i]}',
                     color='r', ha='center')
    # plt.show()

    Verkalit_filtered = filterresults(Result_raw_Verkalit, 5)
    # print(Verkalit_filtered)
    # Verkalit_filtered.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\2. Verkalit\Filtered result table Verkalit.xlsx')

    # Select the water levels in the original design
    Verkalit_original_design = Verkalit_filtered.loc[Verkalit_filtered['Layer thickness Verkalit'].idxmax()]
    Verkalit_original_design = pd.DataFrame([Verkalit_original_design])
    # print(Verkalit_original_design)
    # Verkalit_original_design.to_excel('the highest value.xlsx')

    # ------------------------------------------------------------------------------------------------------------------
    ## Asphalt
    Result_raw_Asphalt = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\4. Asphalt\Result Asphalt complete.xlsx')

    Result_raw_Asphalt['ECI_slopelength'] = ECIFunc.ECIAsphalt(Result_raw_Asphalt['Asphalt layer thickness'], 6.2,
                                                                 Result_raw_Asphalt['slope asphalt'])
    # print(Result_raw_Asphalt)
    # Result_raw_Asphalt.to_excel(
    #     r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\4. Asphalt\Raw for original design Asphalt.xlsx')

    Asphalt_selection = Result_raw_Asphalt[Result_raw_Asphalt['Probability of failure'] < 1 / 60000]
    Asphalt_selection = Asphalt_selection[Asphalt_selection['Waterlevel +mNAP'] == 2.4]
    # Asphalt_selection = Asphalt_selection[Asphalt_selection['Waterlevel +mNAP'] < 2.6]
    Asphalt_selection = Asphalt_selection.sort_values(
        ['Asphalt layer thickness', 'ECI_slopelength'], ascending=[True, True])

    Asphalt_selection = Asphalt_selection.groupby('Asphalt layer thickness').head(1)
    # print(Asphalt_selection)
    # Asphalt_selection.to_excel(
    #     r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\4. Asphalt\Selection original design Asphalt.xlsx')

    figure = plt.figure()
    x = np.arange(len(Asphalt_selection['Asphalt layer thickness']))
    plt.bar(x, Asphalt_selection['ECI_slopelength'], color='b', width=0.2, label='Asphalt')
    plt.xticks(x, Asphalt_selection['Asphalt layer thickness'])
    plt.xlabel('Asphalt layer thickness (m)')
    plt.ylabel('ECI (€)')
    plt.ylim(0, 550)
    plt.title(textwrap.fill('ECI for each asphalt layer thickness', 50), loc='center')
    plt.legend(loc='upper left')

    # Add y-values to the bars
    for i, v in enumerate(Asphalt_selection['ECI_slopelength']):
        if v != 0:
            plt.text(i, v, f'ECI: {v:.1f}\n', color='b', ha='center')
    # plt.show()


    Asphalt_filtered = filterresults(Result_raw_Asphalt, 5)
    # print(Asphalt_filtered)
    Asphalt_original_design = Asphalt_filtered.loc[Asphalt_filtered['Asphalt layer thickness'].idxmax()]
    Asphalt_original_design = pd.DataFrame([Asphalt_original_design])
    # print(Asphalt_original_design)

    # Asphalt_filtered.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\4. Asphalt\Filtered result table Asphalt.xlsx')

    ## Grass
    Result_Grass = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\5. Grass\GEBU results.xlsx',
        usecols='A:C', nrows=23)

    Result_Grass['ECI'] = ECIFunc.ECIGrass(Result_Grass['clay layer thickness'],
                                           Result_Grass['Transition height asphalt-grass (+mNAP)'])
    # print(Result_Grass)

    figure = plt.figure()
    x = np.arange(len(Result_Grass['clay layer thickness']))
    plt.bar(x, Result_Grass['ECI'], color='b', width=0.2, label='ECI clay')
    plt.xticks(x, Result_Grass['clay layer thickness'])
    plt.xlabel('clay layer thickness (m)')
    plt.ylabel('ECI (€)')
    plt.ylim(0, 200)
    plt.title(textwrap.fill('ECI for each clay layer thickness including the transition height', 50), loc='center')
    plt.legend(loc='upper left')
    # Add line graph with water level
    ax2 = plt.twinx()
    ax2.plot(x, Result_Grass['Transition height asphalt-grass (+mNAP)'], color='r', linestyle='-', marker='o',
             label='Transition height')
    ax2.set_ylabel('Transition height asphalt-grass (+mNAP)')

    # Add y-values to the bars
    for i, v in enumerate(Result_Grass['ECI']):
        if v != 0:
            plt.text(i, v, f'ECI: {v:.1f}\n', color='b', ha='center')

    # Add legend for both plots using proxy artists
    plt.legend(loc='upper right')

    plt.show()

    # Result_Grass.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\5. Grass\Result table Grass.xlsx')
