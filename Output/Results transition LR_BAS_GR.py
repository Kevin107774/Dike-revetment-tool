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

ot.Log.Show(ot.Log.NONE)


def maintenance_lr(diameter, ECI_main):
    amount_maintenance_year = 0.20
    # eens per drie jaar onderhoud
    design_lifetime = 50
    maintenance = diameter * ECI_main * amount_maintenance_year * design_lifetime
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

    Loose_rock_filtered = filterresults(Result_Raw_LR, 1)
    Loose_rock_filtered = Loose_rock_filtered[Loose_rock_filtered['Waterlevel +mNAP'] > 1.7].reset_index(drop=True)
    Loose_rock_filtered['height'] = Loose_rock_filtered['Waterlevel +mNAP'] + 0.37
    Loose_rock_filtered = Loose_rock_filtered[
        ['Waterlevel +mNAP', 'height', 'Nominal diameter rock', 'Damage number [S]', 'Slope angle',
         'Probability of failure', 'ECI']]
    Loose_rock_filtered = Loose_rock_filtered.rename(
        columns={'Waterlevel +mNAP': 'Waterlevel +mNAP_LR', 'height': 'height_LR',
                 'Nominal diameter rock': 'Nomnal diameter rock_LR', 'Damage number [S]': 'Damage number S_LR',
                 'Slope angle': 'Slope angle_LR',
                 'Probability of failure': 'Probability of failure_LR', 'ECI': 'ECI_LR'})
    # print(Loose_rock_filtered)
    Loose_rock_filtered.to_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\Transitions\Loose rock filtered for transiton grass.xlsx')

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

    # print(Basalton_filtered)
    # Basalton_filtered.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen ('
    # 'Schijf)\Python scripts\Results\Transitions\Basalton filtered for transiton grass2.xlsx')

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
    # print(Result_Grass)

    # Merge the two dataframes

    # Get unique water levels from each dataframe
    water_levels_LR = Loose_rock_filtered['Waterlevel +mNAP_LR'].unique()
    water_levels_Bas = Basalton_filtered['Waterlevel +mNAP_Bas'].unique()
    water_levels_Grass = Result_Grass['Transition height asphalt-grass (+mNAP)'].unique()

    # Create all possible combinations of water levels using itertools.product
    combinations = list(itertools.product(water_levels_LR, water_levels_Bas, water_levels_Grass))

    # Create a new dataframe to store the combinations
    columns_combination = ['Waterlevel_LR +mNAP_LR', 'Waterlevel_Bas +mNAP_Bas', 'Waterlevel_Grass']
    design_combinations = pd.DataFrame(combinations, columns=columns_combination)
    # print(design_combinations)

    # Merge the other columns from the original dataframes based on the waterstand values
    design_combinations = pd.merge(design_combinations, Loose_rock_filtered, left_on='Waterlevel_LR +mNAP_LR',
                                   right_on='Waterlevel +mNAP_LR', how='left')
    design_combinations = pd.merge(design_combinations, Basalton_filtered, left_on='Waterlevel_Bas +mNAP_Bas',
                                   right_on='Waterlevel +mNAP_Bas', how='left')
    design_combinations = pd.merge(design_combinations, Result_Grass, left_on='Waterlevel_Grass',
                                   right_on='Transition height asphalt-grass (+mNAP)', how='left')

    # Remove the duplicate waterstand columns
    design_combinations = design_combinations.drop(
        columns=['Waterlevel +mNAP_LR', 'Waterlevel +mNAP_Bas', 'Transition height asphalt-grass (+mNAP)'])

    # Add the height for Basalton
    design_combinations['height_Bas'] = design_combinations['Waterlevel_Bas +mNAP_Bas'] - design_combinations[
        'height_LR']
    design_combinations['TOTAL_height'] = design_combinations['height_Bas'] + design_combinations['height_Grass'] + \
                                          design_combinations['height_LR']
    design_combinations = design_combinations[design_combinations['TOTAL_height'] == 8.22]

    # Remove the bottom section of the ECI for the Basalton part
    def calculate_ECI_Bas(row):
        thickness = row['Layer thickness Basalton_Bas']
        waterlevel = row['Waterlevel_LR +mNAP_LR']
        slope = row['Slope angle_Bas']  # Or use the corresponding value from the row if needed
        return ECIFunc.ECIBasalton(thickness, waterlevel, slope)

    # Apply the calculate_ECI_Bas function to each row using apply
    design_combinations['Bottom_ECI_Bas'] = design_combinations.apply(calculate_ECI_Bas, axis=1)
    design_combinations['TOTAL_ECI'] = design_combinations['ECI_LR'] + design_combinations['ECI_Bas'] - \
                                       design_combinations['Bottom_ECI_Bas'] + design_combinations['ECI_grass']
    design_combinations = design_combinations.sort_values('TOTAL_ECI', ascending=True).reset_index(drop=True)
    # design_combinations = design_combinations.head(20)

    # Print the resulting dataframe
    # print(design_combinations)
    # design_combinations.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\Transitions\Design combinations LR_Bas_Grass.xlsx')

    #-------------------------------------------------------------------------------------------------------------------
    # Create the figure and axes (STACKED BAR CHART)
    font = {'size': 20}
    matplotlib.rc('font', **font)

    fig, ax1 = plt.subplots()

    # Define x-axis values (design 1 to 91)
    x = np.arange(0, len(design_combinations['TOTAL_ECI']))

    # Define the water level components
    height_LR = design_combinations['height_LR']
    height_Bas = design_combinations['height_Bas']
    height_Grass = design_combinations['height_Grass']

    # Create the bar chart on the left y-axis
    ax1.bar(x, height_LR, width=0.6, label='Loose rock', color='cornflowerblue')
    ax1.bar(x, height_Bas, bottom=height_LR, width=0.6, label='Basalton', color='lightsalmon')
    ax1.bar(x, height_Grass, bottom=height_LR + height_Bas, width=0.6, label='Grass', color='mediumseagreen')

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
