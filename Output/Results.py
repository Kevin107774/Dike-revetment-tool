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

    # Analysis for the original design

    Loose_rock_selection = Result_Raw_LR[Result_Raw_LR['Probability of failure'] < 1 / 60000]
    Loose_rock_selection = Loose_rock_selection[Loose_rock_selection['Waterlevel +mNAP'] < 1.8]
    Loose_rock_selection = Loose_rock_selection.sort_values(
        ['Nominal diameter rock', 'Damage number [S]', 'ECI_slopelength'],
        ascending=[True, True, True])
    # print(Loose_rock_selection)


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

    Loose_rock_selection_S2 = Loose_rock_selection[Loose_rock_selection['Damage number [S]'] == 2]
    Loose_rock_selection_S2 = Loose_rock_selection_S2.groupby('Nominal diameter rock').head(1)
    zeros_df = pd.DataFrame(0, index=range(2), columns=Loose_rock_selection_S2.columns)
    Loose_rock_selection_S2 = pd.concat([zeros_df, Loose_rock_selection_S2]).reset_index(drop=True)

    Loose_rock_selection_S3 = Loose_rock_selection[Loose_rock_selection['Damage number [S]'] == 3]
    Loose_rock_selection_S3 = Loose_rock_selection_S3.groupby('Nominal diameter rock').head(1)
    zeros_df = pd.DataFrame(0, index=range(2), columns=Loose_rock_selection_S3.columns)
    Loose_rock_selection_S3 = pd.concat([zeros_df, Loose_rock_selection_S3]).reset_index(drop=True)

    Loose_rock_selection_S4 = Loose_rock_selection[Loose_rock_selection['Damage number [S]'] == 4]
    Loose_rock_selection_S4 = Loose_rock_selection_S4.groupby('Nominal diameter rock').head(1)
    zeros_df = pd.DataFrame(0, index=range(1), columns=Loose_rock_selection_S4.columns)
    Loose_rock_selection_S4 = pd.concat([zeros_df, Loose_rock_selection_S4]).reset_index(drop=True)

    Loose_rock_selection_S5 = Loose_rock_selection[Loose_rock_selection['Damage number [S]'] == 5]
    Loose_rock_selection_S5 = Loose_rock_selection_S5.groupby('Nominal diameter rock').head(1)
    zeros_df = pd.DataFrame(0, index=range(1), columns=Loose_rock_selection_S5.columns)
    Loose_rock_selection_S5 = pd.concat([zeros_df, Loose_rock_selection_S5]).reset_index(drop=True)

    Loose_rock_selection_S6 = Loose_rock_selection[Loose_rock_selection['Damage number [S]'] == 6]
    Loose_rock_selection_S6 = Loose_rock_selection_S6.groupby('Nominal diameter rock').head(1)
    zeros_df = pd.DataFrame(0, index=range(1), columns=Loose_rock_selection_S6.columns)
    Loose_rock_selection_S6 = pd.concat([zeros_df, Loose_rock_selection_S6]).reset_index(drop=True)

    Loose_rock_selection_S7 = Loose_rock_selection[Loose_rock_selection['Damage number [S]'] == 7]
    Loose_rock_selection_S7 = Loose_rock_selection_S7.groupby('Nominal diameter rock').head(1)
    zeros_df = pd.DataFrame(0, index=range(1), columns=Loose_rock_selection_S7.columns)
    Loose_rock_selection_S7 = pd.concat([zeros_df, Loose_rock_selection_S7]).reset_index(drop=True)

    Loose_rock_selection_S8 = Loose_rock_selection[Loose_rock_selection['Damage number [S]'] == 8]
    Loose_rock_selection_S8 = Loose_rock_selection_S8.groupby('Nominal diameter rock').head(1)


    Loose_rock_selection_S9 = Loose_rock_selection[Loose_rock_selection['Damage number [S]'] == 9]
    Loose_rock_selection_S9 = Loose_rock_selection_S9.groupby('Nominal diameter rock').head(1)
    # zeros_df = pd.DataFrame(0, index=range(1), columns=Loose_rock_selection_S9.columns)
    # Loose_rock_selection_S9 = pd.concat([zeros_df, Loose_rock_selection_S9]).reset_index(drop=True)

    Loose_rock_selection_S10 = Loose_rock_selection[Loose_rock_selection['Damage number [S]'] == 10]
    Loose_rock_selection_S10 = Loose_rock_selection_S10.groupby('Nominal diameter rock').head(1)
    # zeros_df = pd.DataFrame(0, index=range(1), columns=Loose_rock_selection_S10.columns)
    # Loose_rock_selection_S10 = pd.concat([zeros_df, Loose_rock_selection_S10]).reset_index(drop=True)

    Loose_rock_selection_S11 = Loose_rock_selection[Loose_rock_selection['Damage number [S]'] == 11]
    Loose_rock_selection_S11 = Loose_rock_selection_S11.groupby('Nominal diameter rock').head(1)
    # zeros_df = pd.DataFrame(0, index=range(1), columns=Loose_rock_selection_S11.columns)
    # Loose_rock_selection_S11 = pd.concat([zeros_df, Loose_rock_selection_S11]).reset_index(drop=True)

    Loose_rock_selection_S12 = Loose_rock_selection[Loose_rock_selection['Damage number [S]'] == 12]
    Loose_rock_selection_S12 = Loose_rock_selection_S12.groupby('Nominal diameter rock').head(1)
    # zeros_df = pd.DataFrame(0, index=range(1), columns=Loose_rock_selection_S12.columns)
    # Loose_rock_selection_S12 = pd.concat([zeros_df, Loose_rock_selection_S12]).reset_index(drop=True)

    Loose_rock_selection_S13 = Loose_rock_selection[Loose_rock_selection['Damage number [S]'] == 13]
    Loose_rock_selection_S13 = Loose_rock_selection_S13.groupby('Nominal diameter rock').head(1)
    # zeros_df = pd.DataFrame(0, index=range(1), columns=Loose_rock_selection_S13.columns)
    # Loose_rock_selection_S13 = pd.concat([zeros_df, Loose_rock_selection_S13]).reset_index(drop=True)

    Loose_rock_selection_S14 = Loose_rock_selection[Loose_rock_selection['Damage number [S]'] == 14]
    Loose_rock_selection_S14 = Loose_rock_selection_S14.groupby('Nominal diameter rock').head(1)
    zeros_df = pd.DataFrame(0, index=range(1), columns=Loose_rock_selection_S14.columns)
    Loose_rock_selection_S14 = pd.concat([zeros_df, Loose_rock_selection_S14]).reset_index(drop=True)

    Loose_rock_selection_S15 = Loose_rock_selection[Loose_rock_selection['Damage number [S]'] == 15]
    Loose_rock_selection_S15 = Loose_rock_selection_S15.groupby('Nominal diameter rock').head(1)
    zeros_df = pd.DataFrame(0, index=range(1), columns=Loose_rock_selection_S15.columns)
    Loose_rock_selection_S15 = pd.concat([zeros_df, Loose_rock_selection_S15]).reset_index(drop=True)


    Loose_rock_selection_S16 = Loose_rock_selection[Loose_rock_selection['Damage number [S]'] == 16]
    Loose_rock_selection_S16 = Loose_rock_selection_S16.groupby('Nominal diameter rock').head(1)
    zeros_df = pd.DataFrame(0, index=range(1), columns=Loose_rock_selection_S16.columns)
    Loose_rock_selection_S16 = pd.concat([zeros_df, Loose_rock_selection_S16]).reset_index(drop=True)

    Loose_rock_selection_S17 = Loose_rock_selection[Loose_rock_selection['Damage number [S]'] == 17]
    Loose_rock_selection_S17 = Loose_rock_selection_S17.groupby('Nominal diameter rock').head(1)
    zeros_df = pd.DataFrame(0, index=range(1), columns=Loose_rock_selection_S17.columns)
    Loose_rock_selection_S17 = pd.concat([zeros_df, Loose_rock_selection_S17]).reset_index(drop=True)
    # print(Loose_rock_selection_S9, Loose_rock_selection_S10, Loose_rock_selection_S11, Loose_rock_selection_S12)

    figure = plt.figure(figsize=(12, 6))
    font = {'size': 12}
    matplotlib.rc('font', **font)

    x = np.arange(len(Loose_rock_selection_S2['Nominal diameter rock']))
    plt.bar(x - 8/20, Loose_rock_selection_S2['ECI_slopelength'], width=1/20, color='cornflowerblue', label='S = 2')
    plt.bar(x - 7/20, Loose_rock_selection_S3['ECI_slopelength'], width=1/20, color='cornflowerblue', label='S = 3')
    plt.bar(x - 6/20, Loose_rock_selection_S4['ECI_slopelength'], width=1/20, color='cornflowerblue', label='S = 4')
    plt.bar(x - 5/20, Loose_rock_selection_S5['ECI_slopelength'], width=1/20, color='cornflowerblue', label='S = 5')
    plt.bar(x - 4/20, Loose_rock_selection_S6['ECI_slopelength'], width=1/20, color='cornflowerblue', label='S = 6')
    plt.bar(x - 3/20, Loose_rock_selection_S7['ECI_slopelength'], width=1/20, color='cornflowerblue', label='S = 7')
    plt.bar(x - 2/20, Loose_rock_selection_S8['ECI_slopelength'], width=1/20, color='cornflowerblue', label='S = 8')
    plt.bar(x - 1/20, Loose_rock_selection_S9['ECI_slopelength'], width=1/20, color='cornflowerblue', label='S = 9')
    plt.bar(x, Loose_rock_selection_S10['ECI_slopelength'], width=1/20, color='cornflowerblue', label='S = 10')
    plt.bar(x + 1/20, Loose_rock_selection_S11['ECI_slopelength'], width=1/20, color='cornflowerblue', label='S = 11')
    plt.bar(x + 2/20, Loose_rock_selection_S12['ECI_slopelength'], width=1 / 20, color='cornflowerblue', label='S = 12')
    plt.bar(x + 3/20, Loose_rock_selection_S13['ECI_slopelength'], width=1 / 20, color='cornflowerblue', label='S = 13')
    plt.bar(x + 4/20, Loose_rock_selection_S14['ECI_slopelength'], width=1 / 20, color='cornflowerblue', label='S = 14')
    plt.bar(x + 5/20, Loose_rock_selection_S15['ECI_slopelength'], width=1 / 20, color='cornflowerblue', label='S = 15')
    plt.bar(x + 6/20, Loose_rock_selection_S16['ECI_slopelength'], width=1 / 20, color='cornflowerblue', label='S = 16')
    plt.bar(x + 7/20, Loose_rock_selection_S17['ECI_slopelength'], width=1 / 20, color='cornflowerblue', label='S = 17')

    labels_x = ['HMa 300-1000', 'HMa 1000-3000', 'HMa 3000-6000', 'HMa 6000-10000']
    plt.xticks(x, labels_x)
    plt.xlabel('Rock class (kg)')
    plt.ylabel('ECI (€)')
    plt.ylim(0, 300)
    plt.title(textwrap.fill('ECI for each nominal diameter rock with (S>5) and without maintenance (S≤5)', 50),
              loc='center')
    plt.legend(loc='upper left')

    # Add y-values to the bars
    for i, v in enumerate(Loose_rock_selection_S2['ECI_slopelength']):
        if v != 0:
            plt.text(i-8/20, v + 1, f'S: {Loose_rock_selection_S2["Damage number [S]"].iloc[i]}',
                     color='r', ha='center')
    for i, v in enumerate(Loose_rock_selection_S3['ECI_slopelength']):
        if v != 0:
            plt.text(i-7/20, v + 1, f'S: {Loose_rock_selection_S3["Damage number [S]"].iloc[i]}',
                     color='r', ha='center')
    for i, v in enumerate(Loose_rock_selection_S4['ECI_slopelength']):
        if v != 0:
            plt.text(i-6/20, v + 1, f'S: {Loose_rock_selection_S4["Damage number [S]"].iloc[i]}',
                     color='r', ha='center')
    for i, v in enumerate(Loose_rock_selection_S5['ECI_slopelength']):
        if v != 0:
            plt.text(i-5/20, v + 1, f'S: {Loose_rock_selection_S5["Damage number [S]"].iloc[i]}',
                     color='r', ha='center')
    for i, v in enumerate(Loose_rock_selection_S6['ECI_slopelength']):
        if v != 0:
            plt.text(i-4/20, v + 1, f'S: {Loose_rock_selection_S6["Damage number [S]"].iloc[i]}',
                     color='r', ha='center')
    for i, v in enumerate(Loose_rock_selection_S7['ECI_slopelength']):
        if v != 0:
            plt.text(i-3/20, v + 1, f'S: {Loose_rock_selection_S7["Damage number [S]"].iloc[i]}',
                     color='r', ha='center')
    for i, v in enumerate(Loose_rock_selection_S8['ECI_slopelength']):
        if v != 0:
            plt.text(i-2/20, v + 1, f'S: {Loose_rock_selection_S8["Damage number [S]"].iloc[i]}',
                     color='r', ha='center')
    for i, v in enumerate(Loose_rock_selection_S9['ECI_slopelength']):
        if v != 0:
            plt.text(i-1/20, v + 1, f'S: {Loose_rock_selection_S9["Damage number [S]"].iloc[i]}',
                     color='r', ha='center')
    for i, v in enumerate(Loose_rock_selection_S10['ECI_slopelength']):
        if v != 0:
            plt.text(i, v + 1, f'S: {Loose_rock_selection_S10["Damage number [S]"].iloc[i]}',
                     color='r', ha='center')
    for i, v in enumerate(Loose_rock_selection_S11['ECI_slopelength']):
        if v != 0:
            plt.text(i+1/20, v + 1, f'S: {Loose_rock_selection_S11["Damage number [S]"].iloc[i]}',
                     color='r', ha='center')
    for i, v in enumerate(Loose_rock_selection_S12['ECI_slopelength']):
        if v != 0:
            plt.text(i+2/20, v + 1, f'S: {Loose_rock_selection_S12["Damage number [S]"].iloc[i]}',
                     color='r', ha='center')
    for i, v in enumerate(Loose_rock_selection_S13['ECI_slopelength']):
        if v != 0:
            plt.text(i+3/20, v + 1, f'S: {Loose_rock_selection_S13["Damage number [S]"].iloc[i]}',
                     color='r', ha='center')
    for i, v in enumerate(Loose_rock_selection_S14['ECI_slopelength']):
        if v != 0:
            plt.text(i+4/20, v + 1, f'S: {Loose_rock_selection_S14["Damage number [S]"].iloc[i]}',
                     color='r', ha='center')
    for i, v in enumerate(Loose_rock_selection_S15['ECI_slopelength']):
        if v != 0:
            plt.text(i+5/20, v + 1, f'S: {Loose_rock_selection_S15["Damage number [S]"].iloc[i]}',
                     color='r', ha='center')
    for i, v in enumerate(Loose_rock_selection_S16['ECI_slopelength']):
        if v != 0:
            plt.text(i+6/20, v + 1, f'S: {Loose_rock_selection_S16["Damage number [S]"].iloc[i]}',
                     color='r', ha='center')
    for i, v in enumerate(Loose_rock_selection_S17['ECI_slopelength']):
        if v != 0:
            plt.text(i+7/20, v + 1, f'S: {Loose_rock_selection_S17["Damage number [S]"].iloc[i]}',
                     color='r', ha='center')

    # plt.show()

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
    # Verkalit_selection.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\2. Verkalit\Selection original design Verkalit2.xlsx')

    figure = plt.figure()
    x = np.arange(len(Basalton_selection['Layer thickness Basalton']))
    plt.bar(x-0.1, Basalton_selection['ECI_slopelength'], color='lightsalmon', width=0.2, label='Basalton')
    plt.bar(x+0.1, Verkalit_selection['ECI_slopelength'], color='peachpuff', width=0.2, label='Verkalit')
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
            plt.text(i - 0.2, v + 1, f'ECI: {v:.1f}\nρ: {Basalton_selection["Density concrete"].iloc[i]}',
                     color='b', ha='center')

    for i, v in enumerate(Verkalit_selection['ECI_slopelength']):
        if v != 0:
            plt.text(i + 0.2, v + 1, f'ECI: {v:.1f}\nρ: {Verkalit_selection["Density concrete"].iloc[i]}',
                     color='r', ha='center')
    plt.show()

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
    # Asphalt_selection = Asphalt_selection[Asphalt_selection['Waterlevel +mNAP'] == 2.4]
    Asphalt_selection = Asphalt_selection[Asphalt_selection['Waterlevel +mNAP'] == 6.2]
    Asphalt_selection = Asphalt_selection.sort_values(
        ['Asphalt layer thickness', 'ECI_slopelength'], ascending=[True, True])

    Asphalt_selection = Asphalt_selection.groupby('Asphalt layer thickness').head(1)
    print(Asphalt_selection)
    # Asphalt_selection.to_excel(
    #     r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\4. Asphalt\Selection original design Asphalt.xlsx')

    figure = plt.figure()
    x = np.arange(len(Asphalt_selection['Asphalt layer thickness']))
    plt.bar(x, Asphalt_selection['ECI_slopelength'], color='dimgrey', width=0.2, label='Hydraulic asphalt concrete')
    plt.xticks(x, Asphalt_selection['Asphalt layer thickness'])
    plt.xlabel('Hydraulic asphalt concrete layer thickness (m)')
    plt.ylabel('ECI (€)')
    plt.ylim(0, 550)
    plt.title(textwrap.fill('ECI for each hydraulic asphalt concrete layer thickness', 50), loc='center')
    plt.legend(loc='upper left')

    # Add y-values to the bars
    for i, v in enumerate(Asphalt_selection['ECI_slopelength']):
        if v != 0:
            plt.text(i, v, f'ECI: {v:.1f}\n', color='r', ha='center')
    plt.show()

    Asphalt_filtered = filterresults(Result_raw_Asphalt, 1)
    # print(Asphalt_filtered)
    Asphalt_original_design = Asphalt_filtered.loc[Asphalt_filtered['Asphalt layer thickness'].idxmax()]
    Asphalt_original_design = pd.DataFrame([Asphalt_original_design])
    # print(Asphalt_original_design)

    # Asphalt_filtered.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\4. Asphalt\Filtered result table Asphalt only best option per WL.xlsx')

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
