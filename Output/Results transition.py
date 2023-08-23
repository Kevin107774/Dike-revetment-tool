
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

    Basalton_filtered = filterresults(Result_raw_Basalton, 1).reset_index(drop=True)
    Basalton_filtered['ECI Basalton flipped'] = Basalton_filtered['ECI'].sort_values(ascending=False).values
    # print(Basalton_filtered)

    # Merge the two dataframes
    Subset_LR = Loose_rock_filtered[['Waterlevel +mNAP', 'ECI']]
    Subset_Basalton = Basalton_filtered[['ECI Basalton flipped']]

    Transition_LR_BAS = pd.concat([Subset_LR, Subset_Basalton], axis=1)
    Transition_LR_BAS['Sum_ECI'] = Transition_LR_BAS['ECI'] + Transition_LR_BAS['ECI Basalton flipped']
    print(Transition_LR_BAS)

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
    plt.show()

    # ------------------------------------------------------------------------------------------------------------------
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

    # ------------------------------------------------------------------------------------------------------------------
    ## Asphalt
    Result_raw_Asphalt = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\4. Asphalt\Result Asphalt complete.xlsx')


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

    # plt.show()



