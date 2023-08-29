
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

    # Transition Loose rock to Basalton

    def filterresults(Result_Raw, selected_amount, Req_pf=1 / 60000):
        Result_filtered = Result_Raw[Result_Raw['Probability of failure'] < Req_pf]
        Result_sorted = Result_filtered.sort_values(['Waterlevel +mNAP', 'ECI'], ascending=[True, True])
        Result_grouped = Result_sorted.groupby('Waterlevel +mNAP').head(selected_amount)
        return Result_grouped

    ## Loose Rock
    Result_Raw_LR = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\1. Loose Rock\Result Loose Rock complete.xlsx')

    Loose_rock_filtered = filterresults(Result_Raw_LR, 1)
    Loose_rock_filtered = Loose_rock_filtered[Loose_rock_filtered['Waterlevel +mNAP'] > 1.7].reset_index(drop=True)
    # print(Loose_rock_filtered)

    # Basalton
    Result_raw_Basalton = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\3. Basalton\Result Basalton complete.xlsx')

    Basalton_filtered = filterresults(Result_raw_Basalton, 1)
    Basalton_filtered = Basalton_filtered[Basalton_filtered['Waterlevel +mNAP'] < 4.1].reset_index(drop=True)
    Basalton_filtered['ECI Basalton flipped'] = Basalton_filtered['ECI'].sort_values(ascending=False).values
    # print(Basalton_filtered)

    # Merge the two dataframes
    Subset_LR = Loose_rock_filtered[['Waterlevel +mNAP', 'ECI']]
    Subset_Basalton = Basalton_filtered[['ECI Basalton flipped']]

    Transition_LR_BAS = pd.concat([Subset_LR, Subset_Basalton], axis=1)
    Transition_LR_BAS['Sum_ECI'] = Transition_LR_BAS['ECI'] + Transition_LR_BAS['ECI Basalton flipped']
    # print(Transition_LR_BAS)

    plt.figure()
    x = np.arange(len(Transition_LR_BAS['Waterlevel +mNAP']))
    plt.plot(x, Transition_LR_BAS['ECI'], color='b', label='ECI Loose rock')
    plt.plot(x, Transition_LR_BAS['ECI Basalton flipped'], color='r', label='ECI Basalton')
    plt.plot(x, Transition_LR_BAS['Sum_ECI'], color='black', linestyle='--', label='Total ECI')
    plt.xticks(x, Transition_LR_BAS['Waterlevel +mNAP'])
    plt.xlabel('Waterlevel +mNAP')
    plt.ylabel('ECI (€)')
    plt.ylim(0, 300)
    plt.title(textwrap.fill('Transition height from Loose rock to Basalton', 50), loc='center')
    plt.legend(loc='upper left')
    # plt.show()

    # ------------------------------------------------------------------------------------------------------------------
    ## Transition from Basalton to Grass

    # Basalton
    Result_raw_Basalton = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\3. Basalton\Result Basalton complete.xlsx')

    Basalton_filtered2 = filterresults(Result_raw_Basalton, 1)
    Basalton_filtered2 = Basalton_filtered2[Basalton_filtered2['Waterlevel +mNAP'] > 4.9].reset_index(drop=True)
    # print(Basalton_filtered)

    # Grass

    Result_Grass = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\5. Grass\GEBU results.xlsx',
        usecols='A:C', nrows=23)

    Result_Grass['ECI_grass'] = ECIFunc.ECIGrass(Result_Grass['clay layer thickness'],
                                           Result_Grass['Transition height asphalt-grass (+mNAP)'])
    # print(Result_Grass)
    values_to_select = [5.0, 5.2, 5.4, 5.6, 5.8, 6.0]
    Result_Grass = Result_Grass[Result_Grass['Transition height asphalt-grass (+mNAP)'].isin(values_to_select)]
    Result_Grass = Result_Grass[Result_Grass['Transition height asphalt-grass (+mNAP)'] < 6.01].reset_index(drop=True)
    # print(Result_Grass)

    # Merging the two dataframes
    Subset_Basalton = Basalton_filtered2[['Waterlevel +mNAP', 'ECI']]
    Subset_Grass = Result_Grass[['ECI_grass']]
    Transition_BAS_Grass = pd.concat([Subset_Basalton, Subset_Grass], axis=1)
    Transition_BAS_Grass['Sum_ECI'] = Transition_BAS_Grass['ECI'] + Transition_BAS_Grass['ECI_grass']
    # print(Transition_BAS_Grass)

    plt.figure()
    x = np.arange(len(Transition_BAS_Grass['Waterlevel +mNAP']))
    plt.plot(x, Transition_BAS_Grass['ECI_grass'], color='g', label='ECI Grass')
    plt.plot(x, Transition_BAS_Grass['ECI'], color='r', label='ECI Basalton')
    plt.plot(x, Transition_BAS_Grass['Sum_ECI'], color='black', linestyle='--', label='Total ECI')
    plt.xticks(x, Transition_BAS_Grass['Waterlevel +mNAP'])
    plt.xlabel('Waterlevel +mNAP')
    plt.ylabel('ECI (€)')
    plt.ylim(0, 400)
    plt.title(textwrap.fill('Transition height from basalton to grass', 50), loc='center')
    plt.legend(loc='upper left')
    # plt.show()

    # ------------------------------------------------------------------------------------------------------------------
    # Transition asphalt to grass

    ## Asphalt
    Result_raw_Asphalt = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\4. Asphalt\Result Asphalt complete.xlsx')

    Asphalt_filtered = filterresults(Result_raw_Asphalt, 1)
    Asphalt_filtered = Asphalt_filtered[Asphalt_filtered['Waterlevel +mNAP'] > 4.99].reset_index(drop=True)
    # print(Asphalt_filtered)

    # Grass

    Result_Grass = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\5. Grass\GEBU results.xlsx',
        usecols='A:C', nrows=23)

    Result_Grass['ECI_grass'] = ECIFunc.ECIGrass(Result_Grass['clay layer thickness'],
                                                 Result_Grass['Transition height asphalt-grass (+mNAP)'])
    # print(Result_Grass)
    values_to_select = [5.0, 5.2, 5.4, 5.6, 5.8, 6.0]
    Result_Grass = Result_Grass[Result_Grass['Transition height asphalt-grass (+mNAP)'].isin(values_to_select)]
    Result_Grass = Result_Grass[Result_Grass['Transition height asphalt-grass (+mNAP)'] < 6.01].reset_index(drop=True)
    # print(Result_Grass)

    # Merging the two dataframes
    Subset_Asphalt = Asphalt_filtered[['Waterlevel +mNAP', 'ECI']]
    Subset_Grass = Result_Grass[['ECI_grass']]
    Transition_ASP_Grass = pd.concat([Subset_Asphalt, Subset_Grass], axis=1)
    Transition_ASP_Grass['Sum_ECI'] = Transition_ASP_Grass['ECI'] + Transition_ASP_Grass['ECI_grass']
    print(Transition_ASP_Grass)

    plt.figure()
    x = np.arange(len(Transition_ASP_Grass['Waterlevel +mNAP']))
    plt.plot(x, Transition_ASP_Grass['ECI_grass'], color='g', label='ECI Grass')
    plt.plot(x, Transition_ASP_Grass['ECI'], color='y', label='ECI Asphalt')
    plt.plot(x, Transition_ASP_Grass['Sum_ECI'], color='black', linestyle='--', label='Total ECI')
    plt.xticks(x, Transition_ASP_Grass['Waterlevel +mNAP'])
    plt.xlabel('Waterlevel +mNAP')
    plt.ylabel('ECI (€)')
    plt.ylim(0, 400)
    plt.title(textwrap.fill('Transition height from Asphalt to grass', 50), loc='center')
    plt.legend(loc='upper left')
    plt.show()
