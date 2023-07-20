# This is the file where (potentially) the grass revetment is calculated.
import pandas as pd
import numpy as np
from ECI.ECI import ECIFunc


class Grass:

    # columns_grass = ('Transition height asphalt-grass (+mNAP)', 'Clay layer thickness', 'pf 1/66.666', 'Clay layer thickness 50 year', 'probability of failure (50 year)', 'pf 50 year')
    # Import the dat a from the Excel file
    Excel_file = 'C:/Users/vandonsk5051/Documents/Afstuderen (Schijf)/GEBU Analyse/GEBU results.xlsx'
    GEBU_results = pd.read_excel(Excel_file)
    GEBU_results = GEBU_results.drop(GEBU_results.columns[6:13], axis=1)

    # To delete NaN valued rows
    GEBU_results = GEBU_results.drop([2, 3])

    # Retrieve table
    # print(GEBU_results.iloc[:, 1])



