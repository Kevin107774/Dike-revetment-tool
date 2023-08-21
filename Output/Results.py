# This is where all results of the calculations from the ECI and revetment types are merged and one table is formed to be able to rank the designs.

import numpy as np
import openturns as ot
import pandas as pd
import matplotlib.pyplot as plt
from Input.Parameters import Parameters
from ECI.ECI_class import ECIFunc
from ECI.ECI_Library import ECILib

ot.Log.Show(ot.Log.NONE)


class ResultTableLooseRock:

    # Analysis of Loose Rock

    # print(Result_Raw)
    def filterresults(Result_Raw, selected_amount, Req_pf = 1/60000):

        Result_filtered = Result_Raw[Result_Raw['Probability of failure'] < Req_pf]
        Result_sorted = Result_filtered.sort_values(['Waterlevel +mNAP', 'ECI'], ascending=[True, True])
        Result_grouped = Result_sorted.groupby('Waterlevel +mNAP').head(selected_amount)
        return Result_grouped


## Loose Rock
    Result_Raw_LR = pd.read_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\1. Loose Rock\Result Loose Rock complete.xlsx')

    Loose_rock_filtered = filterresults(Result_Raw_LR, 8)
    # print(Loose_rock_filtered)
    # Loose_rock_filtered.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\1. Loose Rock\Filtered result table Loose rock.xlsx')


    plt.scatter(Loose_rock_filtered['ECI'], Loose_rock_filtered['Probability of failure'])
    plt.xlabel('Nominal diameter rock')
    plt.ylabel('Probability of failure')
    plt.title('TEST')
    ymin = 0
    ymax = 1/60000
    plt.ylim(ymin, ymax)
    # plt.show()

## Basalton
    Result_raw_Basalton = pd.read_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\3. Basalton\Result Basalton complete.xlsx')

    Basalton_filtered = filterresults(Result_raw_Basalton, 5)
    # print(Basalton_filtered)
    # Basalton_filtered.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\3. Basalton\Filtered result table Basalton.xlsx')

## Verkalit
    Result_raw_Verkalit = pd.read_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\2. Verkalit\Result Verkalit complete.xlsx')

    Verkalit_filtered = filterresults(Result_raw_Verkalit, 5)
    # print(Verkalit_filtered)
    # Verkalit_filtered.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\2. Verkalit\Filtered result table Verkalit.xlsx')

    #Select the water levels in the original design
    Verkalit_original_design = Verkalit_filtered.loc[Verkalit_filtered['Layer thickness Verkalit'].idxmax()]
    Verkalit_original_design = pd.DataFrame([Verkalit_original_design])
    # print(Verkalit_original_design)
    # Verkalit_original_design.to_excel('the highest value.xlsx')

## Asphalt
    Result_raw_Asphalt = pd.read_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\4. Asphalt\Result Asphalt complete.xlsx')
    # print(Result_raw_Asphalt)

    Asphalt_filtered = filterresults(Result_raw_Asphalt, 5)
    # print(Asphalt_filtered)
    Asphalt_original_design = Asphalt_filtered.loc[Asphalt_filtered['Asphalt layer thickness'].idxmax()]
    Asphalt_original_design = pd.DataFrame([Asphalt_original_design])
    # print(Asphalt_original_design)

    # Asphalt_filtered.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\4. Asphalt\Filtered result table Asphalt.xlsx')

## Grass
    Result_Grass = pd.read_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\5. Grass\GEBU results.xlsx',usecols='A:C', nrows=23)


    Result_Grass['ECI'] = ECIFunc.ECIGrass(Result_Grass['clay layer thickness'], Result_Grass['Transition height asphalt-grass (+mNAP)'])
    print(Result_Grass)

    Result_Grass.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\5. Grass\Result table Grass.xlsx')



