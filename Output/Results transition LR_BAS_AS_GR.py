import numpy as np
import openturns as ot
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from Input.Parameters import Parameters
from ECI.ECI_class import ECIFunc
from ECI.ECI_Library import ECILib
import textwrap
import itertools
from Financial_costs.Financial_costs_rev import CostFunc

ot.Log.Show(ot.Log.NONE)


def maintenance_LR_2(diameter, ECI_maintenance, S):
    Treshold_S = 10
    design_lifetime = 50
    frequency = 0.2
    maintenance = diameter * ECI_maintenance * (S / Treshold_S) * design_lifetime * frequency
    return maintenance


class ResultTableLooseRock:

    # Transition Loose rock to Basalton to Grass

    def filterresults(Result_Raw, selected_amount, Req_pf=1 / 60000):
        Result_filtered = Result_Raw[Result_Raw['Probability of failure'] < Req_pf]
        Result_sorted = Result_filtered.sort_values(['Waterlevel +mNAP', 'ECI'], ascending=[True, True])
        Result_grouped = Result_sorted.groupby('Waterlevel +mNAP').head(selected_amount)
        return Result_grouped

    ## Loose Rock
    Result_Raw_LR = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\1. Loose Rock\Result Loose Rock '
        r'complete.xlsx')

    Result_Raw_LR['ECI_slopelength'] = Result_Raw_LR.apply(
        lambda row: ECIFunc.ECILooseRock(row['Nominal diameter rock'], row['Waterlevel +mNAP'], row['Slope angle'])
        if row['Damage number [S]'] <= 1
        else ECIFunc.ECILooseRock(row['Nominal diameter rock'], row['Waterlevel +mNAP'],
                                  row['Slope angle']) + maintenance_LR_2(
            row['Nominal diameter rock'], ECILib.ECI_LR_maintenance, row['Damage number [S]']), axis=1)

    Loose_rock_filtered = filterresults(Result_Raw_LR, 1)
    Loose_rock_filtered = Loose_rock_filtered[Loose_rock_filtered['Waterlevel +mNAP'] > 1.7].reset_index(drop=True)
    Loose_rock_filtered['height'] = Loose_rock_filtered['Waterlevel +mNAP'] + 0.37
    Loose_rock_filtered = Loose_rock_filtered[
        ['Waterlevel +mNAP', 'height', 'Nominal diameter rock', 'Damage number [S]', 'Slope angle',
         'Probability of failure', 'ECI_slopelength']]
    Loose_rock_filtered = Loose_rock_filtered.rename(
        columns={'Waterlevel +mNAP': 'Waterlevel +mNAP_LR', 'height': 'height_LR',
                 'Nominal diameter rock': 'Nomnal diameter rock_LR', 'Damage number [S]': 'Damage number S_LR',
                 'Slope angle': 'Slope angle_LR',
                 'Probability of failure': 'Probability of failure_LR', 'ECI_slopelength': 'ECI_LR'})

    # Costs
    Loose_rock_filtered['costs_LR'] = Loose_rock_filtered.apply(
        lambda row: CostFunc.costLooseRock(row['Nomnal diameter rock_LR'], row['Waterlevel +mNAP_LR'],
                                           row['Slope angle_LR']), axis=1)

    # print(Loose_rock_filtered)
    # Loose_rock_filtered.to_excel(
    #     r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\Transitions\Loose rock filtered for transiton grass.xlsx')

    ## Basalton
    Result_Raw_Bas = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\3. Basalton\Result Basalton '
        r'complete.xlsx')

    Basalton_filtered = filterresults(Result_Raw_Bas, 1)
    Basalton_filtered = Basalton_filtered[Basalton_filtered['Waterlevel +mNAP'] >= 1.8].reset_index(drop=True)
    Basalton_filtered = Basalton_filtered[
        ['Waterlevel +mNAP', 'Layer thickness Basalton', 'Density concrete', 'Slope angle',
         'Probability of failure', 'ECI']]
    Basalton_filtered = Basalton_filtered.rename(
        columns={'Waterlevel +mNAP': 'Waterlevel +mNAP_Bas', 'Layer thickness Basalton': 'Layer thickness Basalton_Bas',
                 'Density concrete': 'Density concrete_Bas', 'Slope angle': 'Slope angle_Bas',
                 'Probability of failure': 'Probability of failure_Bas', 'ECI': 'ECI_Bas'})

    # Make sure that the thickness is only increasing. Otherwise designs with varying thicknesses.
    for i in range(1, len(Basalton_filtered)):
        # Check if the current layer thickness is higher than the previous layer thickness
        if Basalton_filtered.loc[i, 'Layer thickness Basalton_Bas'] < Basalton_filtered.loc[
            i - 1, 'Layer thickness Basalton_Bas']:
            # Change the current layer thickness to the previous value
            Basalton_filtered.loc[i, 'Layer thickness Basalton_Bas'] = Basalton_filtered.loc[
                i - 1, 'Layer thickness Basalton_Bas']
            # Change the current density concrete to the previous value
            Basalton_filtered.loc[i, 'Density concrete_Bas'] = Basalton_filtered.loc[i - 1, 'Density concrete_Bas']

    # Calculate the ECI based on the new designs.
    Basalton_filtered['ECI_Bas'] = Basalton_filtered.apply(lambda row: ECIFunc.ECIBasalton(
        row['Layer thickness Basalton_Bas'], row['Waterlevel +mNAP_Bas'], row['Slope angle_Bas']), axis=1)

    Basalton_filtered['costs_Basalton'] = Basalton_filtered.apply(
        lambda row: CostFunc.costBasalton(row['Layer thickness Basalton_Bas'], row['Waterlevel +mNAP_Bas'], row['Slope angle_Bas']), axis=1)

    # print(Basalton_filtered)
    # print(Basalton_filtered) Basalton_filtered.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (
    # Schijf)\Python scripts\Results\Transitions\Basalton filtered for transiton grass.xlsx')

    ## Asphalt
    Result_Raw_As = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\4. Asphalt\Result Asphalt complete.xlsx')

    def filterresults2(Result_Raw, selected_amount, Req_pf=1 / 60000):
        Result_filtered = Result_Raw[Result_Raw['Probability of failure2'] < Req_pf]
        Result_sorted = Result_filtered.sort_values(['Waterlevel +mNAP', 'ECI'], ascending=[True, True])
        Result_grouped = Result_sorted.groupby('Waterlevel +mNAP').head(selected_amount)
        return Result_grouped

    Asphalt_filtered = filterresults(Result_Raw_As, 1)
    Asphalt_filtered = Asphalt_filtered[Asphalt_filtered['Waterlevel +mNAP'] >= 1.8].reset_index(drop=True)
    Asphalt_filtered = Asphalt_filtered[
        ['Waterlevel +mNAP', 'Asphalt layer thickness', 'slope asphalt',
         'Probability of failure2', 'ECI']]
    Asphalt_filtered = Asphalt_filtered.rename(
        columns={'Waterlevel +mNAP': 'Waterlevel +mNAP_As', 'Asphalt layer thickness': 'Layer thickness Asphalt_As',
                 'slope asphalt': 'Slope angle_As',
                 'Probability of failure2': 'Probability of failure_As', 'ECI': 'ECI_As'})

    # Make sure that the thickness is only increasing. Otherwise designs with varying thicknesses.
    for i in range(1, len(Asphalt_filtered)):
        # Check if the current layer thickness is higher than the previous layer thickness
        if Asphalt_filtered.loc[i, 'Layer thickness Asphalt_As'] < Asphalt_filtered.loc[
            i - 1, 'Layer thickness Asphalt_As']:
            # Change the current layer thickness to the previous value
            Asphalt_filtered.loc[i, 'Layer thickness Asphalt_As'] = Asphalt_filtered.loc[
                i - 1, 'Layer thickness Asphalt_As']

    Asphalt_filtered['ECI_As'] = Asphalt_filtered.apply(
        lambda row: ECIFunc.ECIAsphalt(row['Layer thickness Asphalt_As'],
                                       row['Waterlevel +mNAP_As'], row['Slope angle_As']), axis=1)

    Asphalt_filtered['costs_As_max'] = Asphalt_filtered.apply(
        lambda row: CostFunc.costasphalt(row['Layer thickness Asphalt_As'], row['Waterlevel +mNAP_As'],
                                         row['Slope angle_As']), axis=1)

    # print(Asphalt_filtered)
    # print(Asphalt_filtered) Asphalt_filtered.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (
    # Schijf)\Python scripts\Results\Transitions\Asphalt filtered for transiton grass.xlsx')

    ## Grass
    Result_Grass = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\5. Grass\GEBU results.xlsx',
        usecols='A:C', nrows=23)

    Result_Grass['ECI_grass'] = ECIFunc.ECIGrass(Result_Grass['clay layer thickness'],
                                                 Result_Grass['Transition height asphalt-grass (+mNAP)'])
    # print(Result_Grass)
    values_to_select = [5.0, 5.2, 5.4, 5.6, 5.8, 6.0, 6.2]
    Result_Grass = Result_Grass[Result_Grass['Transition height asphalt-grass (+mNAP)'].isin(values_to_select)]
    Result_Grass = Result_Grass[Result_Grass['Transition height asphalt-grass (+mNAP)'] < 6.21].reset_index(drop=True)
    Result_Grass['height'] = 8.22 - Result_Grass['Transition height asphalt-grass (+mNAP)']
    Result_Grass = Result_Grass[
        ['Transition height asphalt-grass (+mNAP)', 'height', 'clay layer thickness', 'pf 1/66.666', 'ECI_grass']]
    Result_Grass = Result_Grass.rename(
        columns={'height': 'height_Grass', 'clay layer thickness': 'clay layer thickness_Grass',
                 'pf 1/66.666': 'Probability of failure_Grass'})

    Result_Grass['costs_Grass'] = Result_Grass.apply(
        lambda row: CostFunc.costGrass(row['clay layer thickness_Grass'], row['height_Grass']), axis=1)

    # print(Result_Grass)

    # Merge the three dataframes

    # Get unique water levels from each dataframe
    water_levels_LR = Loose_rock_filtered['Waterlevel +mNAP_LR'].unique()
    water_levels_Bas = Basalton_filtered['Waterlevel +mNAP_Bas'].unique()
    water_levels_As = Asphalt_filtered['Waterlevel +mNAP_As'].unique()
    water_levels_Grass = Result_Grass['Transition height asphalt-grass (+mNAP)'].unique()

    # Create all possible combinations of water levels using itertools.product
    combinations = list(itertools.product(water_levels_LR, water_levels_Bas, water_levels_As, water_levels_Grass))
    # print(len(combinations))
    # print(combinations)

    # Create a new dataframe to store the combinations
    columns_combination = ['Waterlevel_LR +mNAP_LR', 'Waterlevel_Bas +mNAP_Bas', 'Waterlevel_As +mNAP',
                           'Waterlevel_Grass']
    design_combinations = pd.DataFrame(combinations, columns=columns_combination)

    # Remove the rows where Basalton is lower than Loose rock
    design_combinations = design_combinations[design_combinations['Waterlevel_Bas +mNAP_Bas'] >= design_combinations['Waterlevel_LR +mNAP_LR']]

    # Remove the rows where Asphalt is lower than Basalton
    design_combinations = design_combinations[
        design_combinations['Waterlevel_As +mNAP'] >= design_combinations['Waterlevel_Bas +mNAP_Bas']]

    # Remove the rows where Grass is lower than Asphalt
    design_combinations = design_combinations[
        design_combinations['Waterlevel_Grass'] >= design_combinations['Waterlevel_As +mNAP']].reset_index(drop=True)

    # Merge the other columns from the original dataframes based on the waterstand values
    design_combinations = pd.merge(design_combinations, Loose_rock_filtered, left_on='Waterlevel_LR +mNAP_LR',
                                   right_on='Waterlevel +mNAP_LR', how='left')
    design_combinations = pd.merge(design_combinations, Basalton_filtered, left_on='Waterlevel_Bas +mNAP_Bas',
                                   right_on='Waterlevel +mNAP_Bas', how='left')
    design_combinations = pd.merge(design_combinations, Asphalt_filtered, left_on='Waterlevel_As +mNAP',
                                   right_on='Waterlevel +mNAP_As', how='left')
    design_combinations = pd.merge(design_combinations, Result_Grass, left_on='Waterlevel_Grass',
                                   right_on='Transition height asphalt-grass (+mNAP)', how='left')

    # Remove the duplicate waterstand columns
    design_combinations = design_combinations.drop(
        columns=['Waterlevel +mNAP_LR', 'Waterlevel +mNAP_Bas', 'Waterlevel +mNAP_As',
                 'Transition height asphalt-grass (+mNAP)'])

    # Add the height for Basalton and Asphalt
    design_combinations['height_Bas'] = design_combinations['Waterlevel_Bas +mNAP_Bas'] - \
                                        design_combinations['Waterlevel_LR +mNAP_LR']

    design_combinations['height_As'] = design_combinations['Waterlevel_As +mNAP'] - \
                                       design_combinations['Waterlevel_Bas +mNAP_Bas']

    design_combinations['TOTAL_height'] = design_combinations['height_LR'] + design_combinations['height_Bas'] + \
                                          design_combinations['height_As'] + design_combinations['height_Grass']

    design_combinations = design_combinations[design_combinations['TOTAL_height'] == 8.59].reset_index(drop=True)

    # Remove the bottom section of the ECI for the Basalton part
    def calculate_ECI_Bas(row):
        thickness = row['Layer thickness Basalton_Bas']
        waterlevel = row['Waterlevel_LR +mNAP_LR']
        slope = row['Slope angle_Bas']  # Or use the corresponding value from the row if needed
        return ECIFunc.ECIBasalton(thickness, waterlevel, slope)

    # Apply the calculate_ECI_Bas function to each row using apply
    design_combinations['Bottom_ECI_Bas'] = design_combinations.apply(calculate_ECI_Bas, axis=1)

    def calculate_ECI_As(row):
        thickness = row['Layer thickness Asphalt_As']
        waterlevel = row['Waterlevel_Bas +mNAP_Bas']
        slope = row['Slope angle_As']  # Or use the corresponding value from the row if needed
        return ECIFunc.ECIAsphalt(thickness, waterlevel, slope)

    # Apply the calculate_ECI_As function to each row using apply
    design_combinations['Bottom_ECI_As'] = design_combinations.apply(calculate_ECI_As, axis=1)

    design_combinations['TOTAL_ECI'] = design_combinations['ECI_LR'] + design_combinations['ECI_As'] + \
                                       design_combinations['ECI_Bas'] - design_combinations['Bottom_ECI_Bas'] - \
                                       design_combinations['Bottom_ECI_As'] + design_combinations['ECI_grass']

    def calculate_costs_Bas(row):
        thickness = row['Layer thickness Basalton_Bas']
        waterlevel = row['Waterlevel_LR +mNAP_LR']
        slope = row['Slope angle_Bas']
        return CostFunc.costBasalton(thickness, waterlevel, slope)
    design_combinations['Bottom_costs_bas'] = design_combinations.apply(calculate_costs_Bas, axis=1)

    def calculate_costs_As(row):
        thickness = row['Layer thickness Asphalt_As']
        waterlevel = row['Waterlevel_LR +mNAP_LR']
        slope = row['Slope angle_As']
        return CostFunc.costasphalt(thickness, waterlevel, slope)
    design_combinations['Bottom_costs_As'] = design_combinations.apply(calculate_costs_As, axis=1)

    design_combinations['Total costs'] = design_combinations['costs_LR'] + design_combinations['costs_Grass'] + \
                                         design_combinations['costs_Basalton'] + design_combinations['costs_As_max']- \
                                         design_combinations['Bottom_costs_bas'] - design_combinations['Bottom_costs_As']

    design_combinations = design_combinations.sort_values('TOTAL_ECI', ascending=True).reset_index(drop=True)
    design_combinations = design_combinations.head(100)

    # Print the resulting dataframe
    print(design_combinations)
    design_combinations.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\Transitions\Design combinations LR_Bas_As_Grass.xlsx')

    # -------------------------------------------------------------------------------------------------------------------
    # Create the figure and axes (STACKED BAR CHART)
    font = {'size': 20}
    matplotlib.rc('font', **font)

    fig, ax1 = plt.subplots()

    # Define x-axis values
    x = np.arange(0, len(design_combinations['TOTAL_ECI']))

    # Define the water level components
    height_LR = design_combinations['height_LR'] - 0.37
    height_Bas = design_combinations['height_Bas']
    height_As = design_combinations['height_As']
    height_Grass = design_combinations['height_Grass']

    # Create the bar chart on the left y-axis
    ax1.bar(x, height_LR, width=0.5, label='Loose rock', color='cornflowerblue')
    ax1.bar(x, height_Bas, bottom=height_LR, width=0.5, label='Basalton', color='lightsalmon')
    ax1.bar(x, height_As, bottom=height_LR + height_Bas, width=0.5, label='Asphalt', color='dimgrey')
    ax1.bar(x, height_Grass, bottom=height_LR + height_Bas + height_As, width=0.5, label='Grass', color='mediumseagreen')

    # Set the labels for the left y-axis and the title for the chart
    ax1.set_ylabel('Height (+mNAP)')
    ax1.set_xlabel('Design option')
    ax1.set_title('Design options with varying transition heights and their corresponding ECI')

    # Add a legend to the left y-axis bars
    ax1.legend(loc='upper left')

    # Create the right y-axis
    ax2 = ax1.twinx()

    # Create the line plot for the TOTAL_ECI on the right y-axis
    ax2.plot(x, design_combinations['TOTAL_ECI'], color='red', linewidth=2.5, linestyle='-', marker='o',
             label='Total ECI')
    # ax2.plot(x, design_combinations['Total costs']*10**-2, color='blue', linewidth=2.5, linestyle='-', marker='o', label='Total costs')


    # Set the label for the right y-axis
    ax2.set_ylabel('Total ECI for the combinations (€)')

    # Add a legend to the right y-axis line plot
    ax2.legend(loc='lower right')

    # Adjust the layout to prevent overlapping of bars
    fig.tight_layout()

    # Show the plot
    plt.show()
    # ------------------------------------------------------------------------------------------------------------------
    # Create the figure and axes (BAR chart traditional)
    # fig, ax1 = plt.subplots()
    #
    # # Define x-axis values (design 1 to 91)
    # x = np.arange(0, len(design_combinations['TOTAL_ECI']))
    #
    # # Define the water level components
    # height_LR = design_combinations['height_LR']
    # height_Bas = design_combinations['height_Bas']
    # height_Grass = design_combinations['height_Grass']
    #
    # # Create the bar chart on the left y-axis
    # ax1.bar(x - 0.2, height_LR, width=0.2, label='Loose rock', color='cornflowerblue')
    # ax1.bar(x, height_Bas, width=0.2, label='Basalton', color='lightsalmon')
    # ax1.bar(x + 0.2, height_Grass, width=0.2, label='Grass', color='mediumseagreen')
    #
    # # Set the labels for the left y-axis and the title for the chart
    # ax1.set_ylabel('Height (+mNAP)')
    # ax1.set_xlabel('Design option')
    # ax1.set_title('Design options with varying transition heights and their corresponding ECI')
    #
    # # Add a legend to the left y-axis bars
    # ax1.legend(loc='upper left')
    #
    # # Create the right y-axis
    # ax2 = ax1.twinx()
    #
    # # Create the line plot for the TOTAL_ECI on the right y-axis
    # ax2.plot(x, design_combinations['TOTAL_ECI'], color='red', linewidth=2.5, linestyle='-', marker='o',
    #          label='Total ECI')
    #
    # # Set the label for the right y-axis
    # ax2.set_ylabel('Total ECI for the combinations (€)')
    #
    # # Add a legend to the right y-axis line plot
    # ax2.legend(loc='lower right')
    #
    # # Adjust the layout to prevent overlapping of bars
    # fig.tight_layout()
    #
    # # Show the plot
    # plt.show()
