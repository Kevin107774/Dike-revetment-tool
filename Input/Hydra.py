# This is where the Hydra input is being imported and converted to a class such that it can be used as an input parameter for the probabilistic calculations.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import openturns as ot


ot.Log.Show(ot.Log.NONE)


class HydraulicBoundary:

    # Main file
    Hydraulic_BC = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Hydra en Steentoets\Hydra-NL\Hydraulic boundary '
        r'conditions.xlsx')

# ----------------------------------------------------------------------------------------------------------------------
# Hydraulic boundary conditions Loose Rock

    def HydraulicBoundariesLR(Table = Hydraulic_BC.iloc[21:32, :]):
        Loose_rock = Table

        data = []
        columns = ['Waterlevel_LR', 'Significant_waveheight_LR', 'Peak_period_LR', 'Storm_duration_LR', 'Slope angle_LR']

        for index, i in Loose_rock.iterrows():
            Waterlevel_LR = ot.Normal(i[1], i[12])
            Significant_waveheight_LR = ot.Normal(i[2], i[3])
            Peak_period_LR = ot.Normal(i[4], i[5])
            Storm_duration_LR = ot.Normal(i[7], i[8])
            Slope_angle_LR = ot.Normal(i[16], i[17])

            row = [Waterlevel_LR, Significant_waveheight_LR, Peak_period_LR, Storm_duration_LR, Slope_angle_LR]
            data.append(row)

        Loose_rock_Hydraulic_BC_Distribution = pd.DataFrame(data, columns=columns)
        return Loose_rock_Hydraulic_BC_Distribution

        # print(Loose_rock_Hydraulic_BC_Distribution)

    # Loose_rock = Hydraulic_BC.iloc[0:8, :]
    Hb_LR = HydraulicBoundariesLR()
    pd.set_option('display.max_columns', None)
    # print(Hb_LR)

    def HydraulicBoundariesVerkalit(Table = Hydraulic_BC.iloc[8:12, :]):
        Verkalit = Table

        data = []
        columns = ['Waterlevel_Verkalit', 'Significant_waveheight_Verkalit', 'Peak_period_Verkalit',
                   'Mean_period_Verkalit', 'Storm_duration_Verkalit', 'Slope_angle_Verkalit']

        for index, i in Verkalit.iterrows():
            Waterlevel_Verkalit = ot.Normal(i[1], i[12])
            Significant_waveheight_Verkalit = ot.Normal(i[2], i[3])
            Peak_period_Verkalit = ot.Normal(i[4], i[5])
            Mean_period_Verkalit = ot.Normal(i[9], i[10])
            Storm_duration_Verkalit = ot.Normal(i[7], i[8])
            Slope_angle_Verkalit = ot.Normal(i[16], i[17])

            row = [Waterlevel_Verkalit, Significant_waveheight_Verkalit, Peak_period_Verkalit, Mean_period_Verkalit,
                   Storm_duration_Verkalit, Slope_angle_Verkalit]
            data.append(row)

        Verkalit_Hydraulic_BC_Distribution = pd.DataFrame(data, columns=columns)
        return Verkalit_Hydraulic_BC_Distribution

        # print(Verkalit_Hydraulic_BC_Distribution)

    Hb_ver = HydraulicBoundariesVerkalit()
    pd.set_option('display.max_columns', None)
    # print(Hb_ver)

    def HydraulicBoundariesBasalton(Table = Hydraulic_BC.iloc[13:21, :]):
        Basalton = Table

        data = []
        columns = ['Waterlevel_Basalton', 'Significant_waveheight_Basalton', 'Peak_period_Basalton',
                   'Mean_period_Basalton', 'Storm_duration_Basalton', 'Slope_angle_Basalton']

        for index, i in Basalton.iterrows():
            Waterlevel_Basalton = ot.Normal(i[1], i[12])
            Significant_waveheight_Basalton = ot.Normal(i[2], i[3])
            Peak_period_Basalton = ot.Normal(i[4], i[5])
            Mean_period_Basalton = ot.Normal(i[9], i[10])
            Storm_duration_Basalton = ot.Normal(i[7], i[8])
            Slope_angle_Basalton = ot.Normal(i[16], i[17])

            row = [Waterlevel_Basalton, Significant_waveheight_Basalton, Peak_period_Basalton, Mean_period_Basalton,
                   Storm_duration_Basalton, Slope_angle_Basalton]
            data.append(row)

        Basalton_Hydraulic_BC_Distribution = pd.DataFrame(data, columns=columns)
        return Basalton_Hydraulic_BC_Distribution

        # print(Basalton_Hydraulic_BC_Distribution)

    Hb_bas = HydraulicBoundariesBasalton()
    pd.set_option('display.max_columns', None)
    # # print(Hb_bas)

    def HydraulicBoundariesAsphalt(Table = Hydraulic_BC.iloc[12:18, :]):
        Asphalt = Table

        data = []
        columns = ['Waterlevel_Asphalt', 'Significant_waveheight_Asphalt', 'Peak_period_Asphalt',
                   'Storm_duration_Asphalt', 'Slope_angle_Asphalt', 'Vertical_a', 'Vertical_v', 'Reduction_factor',
                   'Mean_period_Asphalt']

        for index, i in Asphalt.iterrows():
            Waterlevel_Asphalt = ot.Normal(i[1], i[12])
            Significant_waveheight_Asphalt = ot.Normal(i[2], i[3])
            Peak_period_Asphalt = ot.Normal(i[4], i[5])
            Mean_period_Asphalt = ot.Normal(i[9], i[10])
            Storm_duration_Asphalt = ot.Normal(i[7], i[8])
            Slope_angle_Asphalt = ot.Normal(i[16], i[17])
            Vertical_a = ot.Normal(i[18], i[12])
            Vertical_v = ot.Normal(i[19], i[12])
            Reduction_factor = ot.Normal(i[21], i[12])

            row = [Waterlevel_Asphalt, Significant_waveheight_Asphalt, Peak_period_Asphalt, Mean_period_Asphalt,
                   Storm_duration_Asphalt, Slope_angle_Asphalt, Vertical_a, Vertical_v, Reduction_factor]
            data.append(row)

        Asphalt_Hydraulic_BC_Distribution = pd.DataFrame(data, columns=columns)
        return Asphalt_Hydraulic_BC_Distribution

        # print(Asphalt_Hydraulic_BC_Distribution)

    Hb_As = HydraulicBoundariesAsphalt()
    pd.set_option('display.max_columns', None)
    # print(Hb_As)


