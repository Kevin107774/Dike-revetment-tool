# This is where all ECI values for different components are stored as a library for further calculations.


import numpy as np
import openturns as ot
import pandas as pd

ot.Log.Show(ot.Log.NONE)


class ECILib:
    # Loose Rock
    # Transport per bulk carrier from Norway [m3]
    ECI_Transport_LR = 3.89

    # Loose Rock [m3]
    ECI_LR = 2.95

    # Loose Rock Maintenance [m3]
    ECI_LR_maintenance = 3.94

    # Installation loose rock [m2]
    ECI_crawler_crane_LR = 0.04
    ECI_excavator_LR = 0.003
    ECI_installation_LR = ECI_crawler_crane_LR + ECI_excavator_LR

    # Filter layer [m3]
    ECI_filter_LR = 7.80
# ------------------------------------------------------------------------
    # Placed elements (Verkalit)
    # Transport per truck from Friesland [m3]
    ECI_Transport_Ver = 1.00

    # Verkalit [m3]
    ECI_verkalit = 26.30

    # Installation Verkalit [m2]
    ECI_vessel_Ver = 0.11
    ECI_excavator_Ver = 0.07
    ECI_installation_Ver = ECI_excavator_Ver + ECI_vessel_Ver

    # Geotextile [m2]
    ECI_Geotextile_Ver = 0.45

    # Filter [m3]
    ECI_filter_Ver = 7.80

    # Installation filter [m2]
    ECI_crawler_crane_Ver = 0.02
    ECI_truck_crane_Ver = 0.01
    ECI_Installation_filter_Ver = ECI_crawler_crane_Ver + ECI_truck_crane_Ver
# ------------------------------------------------------------------------
    # Placed elements (Basalton)
    # Transport per truck from Alphen a/d Rijn [m3]
    ECI_Transport_Bas = 6.04

    # Basalton [m3]
    ECI_Basalton = 17.88

    # Installation Basalton [m2]
    ECI_vessel_Bas = 0.11
    ECI_excavator_Bas = 0.07
    ECI_installation_Bas = ECI_excavator_Bas + ECI_vessel_Bas

    # Geotextile [m2]
    ECI_Geotextile_Bas = 0.45

    # Filter [m3]
    ECI_filter_Bas = 7.80

    # Installation filter [m2]
    ECI_crawler_crane_Bas = 0.02
    ECI_truck_crane_Bas = 0.01
    ECI_Installation_filter_Bas = ECI_crawler_crane_Bas + ECI_truck_crane_Bas

    # Filling material [m3]
    ECI_split_Bas = 7.80
# ------------------------------------------------------------------------
    # Asphalt
    # Transport asphalt from factory 36 km [m3]
    ECI_Transport_As = 0.73

    # Asphalt [m3]
    ECI_Asphalt = 47.71

    # Removing asphalt [m2]
    ECI_crusher_As = 0.03

    # Foundation sand [m3]
    ECI_sand_As = 4.04

    # Installation sand [m2]
    ECI_crawler_crane_sand_As = 0.07
    ECI_bulldozer_As = 0.04
    ECI_installation_sand_As = ECI_crawler_crane_sand_As + ECI_bulldozer_As

    # Densify sand [m2]
    ECI_bulldozer_dens_As = 0.02
    ECI_tractor_water_As = 0.04
    ECI_roller_sand_As = 0.02
    ECI_densify_sand_As = ECI_bulldozer_dens_As + ECI_tractor_water_As + ECI_roller_sand_As

    # Profiling slope and aply asphalt [m2]
    ECI_crawler_crane_As = 2.57

    # Densify asphalt [m2]
    ECI_roller_As = 0.47

    # Adhesive coating [m2]
    ECI_coating_As = 0.12
# ------------------------------------------------------------------------
    # Grass
    # Transport grass from Betuwe (312 km) [m3]
    ECI_Transport_Gr = 2.78

    # Clay [m3]
    ECI_clay_Gr = 2.56

    # Excavation works [m3]
    ECI_crawler_crane_Gr = 0.03
    ECI_bulldozer_Gr = 0.03
    ECI_excavation_Gr = ECI_bulldozer_Gr + ECI_crawler_crane_Gr

    # Transport soil to depot [m3]
    ECI_transport_depot_Gr = 0.17

    # Processing soil in depot [m3]
    ECI_process_depot_Gr = 0.02

    # Densify clay [m3]
    ECI_densify_Gr = 0.02

    # Profiling [m3]
    ECI_bulldozer_prof_Gr = 0.02

    # Sowing grass [m2]
    ECI_sowing_Gr = 1.03

    # Maintenance (sheep) [m2]
    ECI_maintenance_Gr = 0.00



