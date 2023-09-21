import numpy as np
import openturns as ot
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as matplotlib
from Input.Parameters import Parameters
from ECI.ECI_class import ECIFunc
from ECI.ECI_Library import ECILib
import textwrap


def maintenance_LR_2(diameter, ECI_maintenance, S):
    Treshold_S = 6
    design_lifetime = 50
    frequency = 0.2
    maintenance = diameter * ECI_maintenance * (S / Treshold_S) * design_lifetime * frequency
    return maintenance

def ECILooseRock2(thickness, waterlevel, slope):
    h = waterlevel
    a = slope
    slopelength_LR = np.sqrt((h + 0.37) ** 2 + ((h + 0.37) * (1 / a)) ** 2)
    print(slopelength_LR)

    filter_thickness = 0.2
    m2_LR = slopelength_LR * (ECILib.ECI_installation_LR + ECILib.ECI_filter_LR * filter_thickness)
    m3_LR = slopelength_LR * (ECILib.ECI_Transport_LR + ECILib.ECI_LR)
    ECI_Loose_Rock1 = m2_LR + m3_LR * thickness
    return ECI_Loose_Rock1

ECI_LR_aanleg = ECILooseRock2(0.59, 2.2, 1/4)
ECI_LR_maintenance = maintenance_LR_2(0.59, ECILib.ECI_LR_maintenance, 10)
ECI_LR = ECI_LR_maintenance + ECI_LR_aanleg
print(ECI_LR)

def ECIVerkalit2(thickness, waterlevel, slope):
    h = waterlevel
    a = slope
    slopelength_Ver = np.sqrt((h - 2.2) ** 2 + ((h - 2.2) * (1 / a)) ** 2)
    print(slopelength_Ver)
    filter_thickness = 0.2
    m2_ver = slopelength_Ver * (ECILib.ECI_installation_Ver + ECILib.ECI_Geotextile_Ver +
                                ECILib.ECI_filter_Ver * filter_thickness + ECILib.ECI_Installation_filter_Ver)
    m3_ver = slopelength_Ver * (ECILib.ECI_Transport_Ver + ECILib.ECI_verkalit)
    ECI_Verkalit = m2_ver + m3_ver * thickness
    return ECI_Verkalit

ECI_Ver = ECIVerkalit2(0.3, 3.1, 1/4.1)
print(ECI_Ver)

def ECIAsphalt2(thickness, waterlevel, slope):
    h = waterlevel
    a = slope
    slopelength_As = np.sqrt((h - 3.1) ** 2 + ((h - 3.1) * (1 / a)) ** 2)

    sandlayer_thickness = 0.2
    m2_As = slopelength_As * (ECILib.ECI_crusher_As + ECILib.ECI_installation_sand_As + ECILib.ECI_densify_sand_As +
                              ECILib.ECI_crawler_crane_As + ECILib.ECI_roller_As + ECILib.ECI_coating_As +
                              ECILib.ECI_sand_As * sandlayer_thickness)
    m3_As = slopelength_As * (ECILib.ECI_Transport_As + ECILib.ECI_Asphalt)
    ECI_Asphalt = m2_As + m3_As * thickness
    return ECI_Asphalt

ECI_As = ECIAsphalt2(0.15, 5.5, 1/4.1)
print(ECI_As)

def ECIGrass2(thickness, transition, slope):
    h = transition
    a = slope
    slopelength_Gr = np.sqrt((8.80 - h) ** 2 + ((8.80 - h) * 1 / a) ** 2)  # gemeten vanaf boven (8.80 mNAP). Hoe lager de
    # transitie, hoe langer de slopelength.
    # print(slopelength_Gr)
    m2_Gr = slopelength_Gr * (ECILib.ECI_sowing_Gr + ECILib.ECI_maintenance_Gr)
    m3_Gr = slopelength_Gr * (
            ECILib.ECI_Transport_Gr + ECILib.ECI_clay_Gr + ECILib.ECI_excavation_Gr + ECILib.ECI_transport_depot_Gr + ECILib.ECI_process_depot_Gr + ECILib.ECI_densify_Gr + ECILib.ECI_bulldozer_prof_Gr)
    ECI_Grass = m2_Gr + m3_Gr * thickness
    return ECI_Grass

ECI_Grass = ECIGrass2(1.4, 5.5, 1/3)
print(ECI_Grass)

ECI_Arcadis_design = ECI_LR + ECI_Ver + ECI_As + ECI_Grass
print(ECI_Arcadis_design)