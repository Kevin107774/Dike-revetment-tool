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
    Loose_rock_selection = Loose_rock_selection.sort_values(['Nominal diameter rock', 'Damage number [S]', 'ECI_slopelength'],
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
    plt.xticks(x, Loose_rock_selection_high['Nominal diameter rock'])
    plt.xlabel('Nominal diameter rock (m)')
    plt.ylabel('ECI (€)')
    plt.ylim(0, 170)
    plt.title(textwrap.fill('ECI for each nominal diameter rock with (S>5) and without maintenance (S<5)', 50), loc='center')
    plt.legend()

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

    ## Basalton
    Result_raw_Basalton = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\3. Basalton\Result Basalton complete.xlsx')

    Basalton_filtered = filterresults(Result_raw_Basalton, 5)
    # print(Basalton_filtered)
    # Basalton_filtered.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\3. Basalton\Filtered result table Basalton.xlsx')

    ## Verkalit
    Result_raw_Verkalit = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\2. Verkalit\Result Verkalit complete.xlsx')

    Verkalit_filtered = filterresults(Result_raw_Verkalit, 5)
    # print(Verkalit_filtered)
    # Verkalit_filtered.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\2. Verkalit\Filtered result table Verkalit.xlsx')

    # Select the water levels in the original design
    Verkalit_original_design = Verkalit_filtered.loc[Verkalit_filtered['Layer thickness Verkalit'].idxmax()]
    Verkalit_original_design = pd.DataFrame([Verkalit_original_design])
    # print(Verkalit_original_design)
    # Verkalit_original_design.to_excel('the highest value.xlsx')

    ## Asphalt
    Result_raw_Asphalt = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\4. Asphalt\Result Asphalt complete.xlsx')
    # print(Result_raw_Asphalt)

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
    #
    # Result_Grass.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\5. Grass\Result table Grass.xlsx')
