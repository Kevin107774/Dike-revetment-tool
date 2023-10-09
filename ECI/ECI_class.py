# THis is where the ECI for all different components is being calculated. The total ECI score is being calculated in one class.
import numpy as np
import openturns as ot
import pandas as pd
from ECI.ECI_Library import ECILib
from Input.Parameters import Parameters

Hydraulic_BC = pd.read_excel(
    r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Hydra en Steentoets\Hydra-NL\Hydraulic boundary '
    r'conditions.xlsx')
ot.Log.Show(ot.Log.NONE)


class ECIFunc:

    def ECILooseRock(thickness, waterlevel, slope):
        h = waterlevel
        a = slope
        if h <= 1.79:
            slopelength_LR = np.sqrt((h + 0.37) ** 2 + ((h + 0.37) * (1 / a)) ** 2)
        elif 1.79 < h <= 2.41:
            slopelength_LR = 8.34 + np.sqrt((h - 1.79) ** 2 + ((h - 1.79) * (1 / a)) ** 2)
        else:
            slopelength_LR = 8.34 + 4.81 + np.sqrt((h - 2.41) ** 2 + ((h - 2.41) * (1 / a)) ** 2)
        filter_thickness = 0.2
        m2_LR = slopelength_LR * (ECILib.ECI_installation_LR + ECILib.ECI_filter_LR * filter_thickness)
        m3_LR = slopelength_LR * (ECILib.ECI_Transport_LR + ECILib.ECI_LR)
        ECI_Loose_Rock1 = m2_LR + m3_LR * thickness * 2

        return ECI_Loose_Rock1
    print(ECILooseRock(1.44, 2, 4))

    def ECIVerkalit(thickness, waterlevel, slope):
        h = waterlevel
        a = slope
        if 1.79 < h <= 2.41:
            slopelength_Ver = np.sqrt((h - 1.79) ** 2 + ((h - 1.79) * (1 / a)) ** 2)
        else:
            slopelength_Ver = 4.81 + np.sqrt((h - 2.41) ** 2 + ((h - 2.41) * (1 / a)) ** 2)

        filter_thickness = 0.2
        m2_ver = slopelength_Ver * (ECILib.ECI_installation_Ver + ECILib.ECI_Geotextile_Ver +
                                    ECILib.ECI_filter_Ver * filter_thickness)
        m3_ver = slopelength_Ver * (ECILib.ECI_Transport_Ver + ECILib.ECI_verkalit)
        ECI_Verkalit = m2_ver + m3_ver * thickness
        return ECI_Verkalit
    # x1 = ECIVerkalit(0.3, 2.4, 1/7.7)
    # print('ECI ver', x1)

    def ECIBasalton(thickness, waterlevel, slope):
        h = waterlevel
        a = slope
        if 1.79 < h <= 2.41:
            slopelength_Bas = np.sqrt((h - 1.8) ** 2 + ((h - 1.79) * (1 / a)) ** 2)
        else:
            slopelength_Bas = 4.81 + np.sqrt((h - 2.41) ** 2 + ((h - 2.41) * (1 / a)) ** 2)
        filter_thickness = 0.2
        m2_Bas = slopelength_Bas * (ECILib.ECI_installation_Bas + ECILib.ECI_Geotextile_Bas +
                                    (ECILib.ECI_filter_Bas * filter_thickness) + ECILib.ECI_split_Bas * 0.1)
        m3_Bas = slopelength_Bas * (ECILib.ECI_Transport_Bas + ECILib.ECI_Basalton)
        ECI_Basalton = m2_Bas + m3_Bas * thickness
        return ECI_Basalton

    def ECIAsphalt(thickness, waterlevel, slope):
        h = waterlevel
        a = slope
        if 1.80 <= h < 2.4:
            slopelength_As = np.sqrt((h - 1.8) ** 2 + ((h - 1.80) * (1 / a)) ** 2)
        elif 2.40 <= h <= 6.2:
            slopelength_As = 4.81 + np.sqrt((h - 2.4) ** 2 + ((h - 2.4) * (1 / a)) ** 2)

        sandlayer_thickness = 0.2
        m2_As = slopelength_As * (ECILib.ECI_installation_As + ECILib.ECI_coating_As +
                                  ECILib.ECI_sand_As * sandlayer_thickness)
        m3_As = slopelength_As * (ECILib.ECI_Transport_As + ECILib.ECI_Asphalt)
        ECI_Asphalt = m2_As + m3_As * thickness
        return ECI_Asphalt
    # x2 = ECIAsphalt(0.30, 6.15, 1/3.75)
    # print('ECI as', x2[0])

    def ECIGrass(thickness, transition):
        h = transition
        a = 4
        slopelength_Gr = np.sqrt((8.22 - h) ** 2 + ((8.22 - h) * a) ** 2)  # gemeten vanaf boven (8.22 mNAP). Hoe lager de

        # transitie, hoe langer de slopelength.
        # print(slopelength_Gr)
        m2_Gr = slopelength_Gr * (ECILib.ECI_sowing_Gr + ECILib.ECI_maintenance_Gr)
        m3_Gr = slopelength_Gr * (
                    ECILib.ECI_Transport_Gr + ECILib.ECI_clay_Gr + ECILib.ECI_apply_clay_GR)
        ECI_Grass = m2_Gr + m3_Gr * thickness
        return ECI_Grass
    #
    # x3 = ECIGrass(1.4, 6.15)
    # print('ECI gr', x3)