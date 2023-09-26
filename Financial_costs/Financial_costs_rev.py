# THis is where the ECI for all different components is being calculated. The total ECI score is being calculated in one class.
import numpy as np
import openturns as ot
import pandas as pd

from Input.Parameters import Parameters

Hydraulic_BC = pd.read_excel(
    r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Hydra en Steentoets\Hydra-NL\Hydraulic boundary '
    r'conditions.xlsx')
ot.Log.Show(ot.Log.NONE)


class CostFunc:

    def costLooseRock(rock_class, waterlevel, slope):
        h = waterlevel
        a = slope
        rock15_300 = 73     # Euro/m3
        rock40_200 = 75     # Euro/m3
        rock60_300 = 77     # Euro/m3
        rock300_1000 = 81   # Euro/m3
        rock1_3t = 89       # Euro/m3
        rock3_6t = 225      # Euro/m3
        rock6_10t = 400     # Euro/m3
        filter = 20         # Euro/m3 CHECKEN!!

        if h <= 1.79:
            slopelength_LR = np.sqrt((h + 0.37) ** 2 + ((h + 0.37) * (1 / a)) ** 2)
        elif 1.79 < h <= 2.41:
            slopelength_LR = 8.34 + np.sqrt((h - 1.79) ** 2 + ((h - 1.79) * (1 / a)) ** 2)
        else:
            slopelength_LR = 8.34 + 4.81 + np.sqrt((h - 2.41) ** 2 + ((h - 2.41) * (1 / a)) ** 2)
        filter_thickness = 0.2

        if rock_class == 0.31:
            costs_LR = (slopelength_LR * 2 * 0.31) * rock15_300 + filter_thickness * filter
        elif rock_class == 0.34:
            costs_LR = (slopelength_LR * 2 * 0.34) * rock40_200 + filter_thickness * filter
        elif rock_class == 0.38:
            costs_LR = (slopelength_LR * 2 * 0.38) * rock60_300 + filter_thickness * filter
        elif rock_class == 0.59:
            costs_LR = (slopelength_LR * 2 * 0.59) * rock300_1000 + filter_thickness * filter
        elif rock_class == 0.9:
            costs_LR = (slopelength_LR * 2 * 0.9) * rock1_3t + filter_thickness * filter
        elif rock_class == 1.18:
            costs_LR = (slopelength_LR * 2 * 1.18) * rock3_6t + filter_thickness * filter
        else:
            costs_LR = (slopelength_LR * 2 * 1.44) * rock6_10t + filter_thickness * filter
        return costs_LR

    def costverkalit(thickness, waterlevel, slope):
        h = waterlevel
        a = slope
        Verkalit = 70       # Euro/m3
        apply_ver = 11      # Euro/m2
        geotextile = 9      # Euro/m2
        filter_ver = 10     # Euro/m3

        if 1.79 < h <= 2.41:
            slopelength_Ver = np.sqrt((h - 1.79) ** 2 + ((h - 1.79) * (1 / a)) ** 2)
        else:
            slopelength_Ver = 4.81 + np.sqrt((h - 2.41) ** 2 + ((h - 2.41) * (1 / a)) ** 2)
        filter_thickness = 0.2

        costs_Ver = (slopelength_Ver * thickness * Verkalit) + (slopelength_Ver * filter_thickness * filter_ver) + (slopelength_Ver * (geotextile + apply_ver))
        return costs_Ver

    def costBasalton(thickness, waterlevel, slope):
        h = waterlevel
        a = slope
        Basalton = 70       # Euro/m3
        apply_bas = 11      # Euro/m2
        geotextile = 9      # Euro/m2
        filter_bas = 10     # Euro/m3

        if 1.79 < h <= 2.41:
            slopelength_Bas = np.sqrt((h - 1.8) ** 2 + ((h - 1.79) * (1 / a)) ** 2)
        else:
            slopelength_Bas = 4.81 + np.sqrt((h - 2.41) ** 2 + ((h - 2.41) * (1 / a)) ** 2)
        filter_thickness = 0.2

        costs_bas = (slopelength_Bas * thickness * Basalton) + (slopelength_Bas * filter_thickness * filter_bas) + (slopelength_Bas * (geotextile + apply_bas))
        return costs_bas

    def costasphalt(thickness, waterlevel, slope):
        h = waterlevel
        a = slope
        asphalt = 80
        sand = 13
        kleeflaag = 1

        if 1.80 <= h < 2.4:
            slopelength_As = np.sqrt((h - 1.8) ** 2 + ((h - 1.80) * (1 / a)) ** 2)
        elif 2.40 <= h <= 6.2:
            slopelength_As = 4.81 + np.sqrt((h - 2.4) ** 2 + ((h - 2.4) * (1 / a)) ** 2)

        sandlayer_thickness = 0.2

        costs_asphalt = (slopelength_As * thickness * asphalt) + (slopelength_As * sandlayer_thickness * sand) + (slopelength_As * kleeflaag)
        return costs_asphalt

    def costGrass(thickness, transition):
        h = transition
        a = 4
        clay = 17           #Euro/m3
        apply_clay = 2      #Euro/m3
        grass = 2           #Euro/m2

        slopelength_Gr = np.sqrt((8.22 - h) ** 2 + ((8.22 - h) * a) ** 2)  # gemeten vanaf boven (8.22 mNAP). Hoe lager de
                                                                           # transitie, hoe langer de slopelength.
        Volume_Gr = (((thickness - 0.8) * slopelength_Gr) / 2) + (0.8 * slopelength_Gr)

        costs_grass = (Volume_Gr * (clay + apply_clay)) + (slopelength_Gr * grass)

        return costs_grass
