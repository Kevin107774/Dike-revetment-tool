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
            slopelength_LR = np.sqrt((h - 0.37) ** 2 + ((h - 0.37) * (1 / a)) ** 2)
        elif 1.79 < h <= 2.41:
            slopelength_LR = 8.34 + np.sqrt((h - 1.79) ** 2 + ((h - 1.79) * (1 / a)) ** 2)
        else:
            slopelength_LR = 8.34 + 4.81 + np.sqrt((h - 2.41) ** 2 + ((h - 2.41) * (1 / a)) ** 2)
        filter_thickness = 0.2
        m2_LR = slopelength_LR * (ECILib.ECI_installation_LR + ECILib.ECI_filter_LR * filter_thickness)
        m3_LR = slopelength_LR * (ECILib.ECI_Transport_LR + ECILib.ECI_LR)
        ECI_Loose_Rock1 = m2_LR + m3_LR * thickness
        return ECI_Loose_Rock1

    # for index, i in Hydraulic_BC.iloc[0:8, :].iterrows():
    #     h = i[1]
    #     a = i[16]
    #     x = ECILooseRock0(0.17, h, a)
    # print(x)

    def ECIVerkalit(thickness, waterlevel, slope):
        h = waterlevel
        a = slope
        if 1.79 < h <= 2.41:
            slopelength_Ver = np.sqrt((h - 1.79) ** 2 + ((h - 1.79) * (1 / a)) ** 2)
        else:
            slopelength_Ver = 4.81 + np.sqrt((h - 2.41) ** 2 + ((h - 2.41) * (1 / a)) ** 2)
        filter_thickness = 0.2
        m2_ver = slopelength_Ver * (ECILib.ECI_installation_Ver + ECILib.ECI_Geotextile_Ver +
                                   ECILib.ECI_filter_Ver * filter_thickness + ECILib.ECI_Installation_filter_Ver)
        m3_ver = slopelength_Ver * (ECILib.ECI_Transport_Ver + ECILib.ECI_verkalit)
        ECI_Verkalit = m2_ver + m3_ver * thickness
        return ECI_Verkalit

    # def ECIBasalton(thickness, waterlevel, slope):
    #     h = waterlevel
    #     a = slope
    #     if 1.79 < h <= 2.41:
    #         slopelength_Bas = np.sqrt((h - 1.79) ** 2 + ((h - 1.79) * (1 / a)) ** 2)
    #     else:
    #         slopelength_Bas = 4.81 + np.sqrt((h - 2.41) ** 2 + ((h - 2.41) * (1 / a)) ** 2)
    #     filter_thickness = 0.2
    #     m2_Bas = slopelength_Bas * (ECILib.ECI_installation_Bas + ECILib.ECI_Geotextile_Bas +
    #                                 (ECILib.ECI_filter_Bas + ECILib.ECI_split_Bas) * filter_thickness +
    #                                 ECILib.ECI_Installation_filter_Bas)
    #     m3_Bas = slopelength_Bas * (ECILib.ECI_Transport_Bas + ECILib.ECI_Basalton)
    #     ECI_Basalton = m2_Bas + m3_Bas * thickness
    #     return ECI_Basalton

    def ECIAsphalt(thickness, waterlevel, slope):
        h = waterlevel
        a = slope
        if 2.40 <= h <= 6.2:
            slopelength_As = np.sqrt((h - 2.41) ** 2 + ((h - 2.41) * (1 / a)) ** 2)
        else:
            slopelength_As = 14.54 + (4.81 - (np.sqrt((h - 1.79) ** 2 + ((h - 1.79) * (1 / a)) ** 2)))
        sandlayer_thickness = 0.2
        m2_As = slopelength_As * (ECILib.ECI_crusher_As + ECILib.ECI_installation_sand_As + ECILib.ECI_densify_sand_As +
                                  ECILib.ECI_crawler_crane_As + ECILib.ECI_roller_As + ECILib.ECI_coating_As +
                                  ECILib.ECI_sand_As * sandlayer_thickness)
        m3_As = slopelength_As * (ECILib.ECI_Transport_As + ECILib.ECI_Asphalt)
        ECI_Asphalt = m2_As + m3_As * thickness
        return ECI_Asphalt

    # def ECIGrass(volume_Gr):
    #     Slopelength_Gr = 8.49
    #     m2_Gr = Slopelength_Gr * (ECILib.ECI_transport_depot_Gr + ECILib.ECI_process_depot_Gr + ECILib.ECI_densify_Gr +
    #                               ECILib.ECI_bulldozer_prof_Gr + ECILib.ECI_sowing_Gr + ECILib.ECI_maintenance_Gr)
    #     m3_Gr = ECILib.ECI_Transport_Gr + ECILib.ECI_clay_Gr + ECILib.ECI_excavation_Gr
    #     ECI_Grass = m2_Gr + m3_Gr * volume_Gr
    #     return ECI_Grass
