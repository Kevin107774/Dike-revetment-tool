# This is where all ECI values for different components are stored as a library for further calculations.


import numpy as np
import openturns as ot
import pandas as pd
import matplotlib.pyplot as plt

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
    ECI_installation = 0.043


    # Filter layer [m3]
    ECI_filter_LR = 7.80

    # Pie chart Data
    labels = ['Transport', 'Loose Rock [m3]', 'Installation Loose Rock [m2]',
              'Filter Layer [m3]']
    sizes = [ECI_Transport_LR, ECI_LR, ECI_installation, ECI_filter_LR]

    # Create a pie chart
    plt.figure(figsize=(20, 20))
    plt.subplot(3, 2, 1)
    # Create the pie chart with actual values as labels
    plt.pie(sizes, labels=sizes, startangle=0)


    plt.legend(labels=labels, bbox_to_anchor=(1, 0.5), loc='center right')

    # Title
    plt.title('ECI Distribution Loose Rock')

    # Display the pie chart
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # plt.show()

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

    # Pie chart Data
    labels = ['Transport', 'Verkalit', 'Installation', 'Geotextile', 'Filter material', 'Installation filter']
    sizes = [ECI_Transport_Ver, ECI_verkalit, ECI_installation_Ver, ECI_Geotextile_Ver, ECI_filter_Ver, ECI_Installation_filter_Ver]

    # Create a pie chart
    plt.subplot(3, 2, 2)
    # Create the pie chart with actual values as labels
    plt.pie(sizes, labels=sizes, startangle=0)
    plt.legend(labels=labels, bbox_to_anchor=(1, 0.5), loc='center right')

    # Title
    plt.title('ECI Distribution Verkalit')

    # Display the pie chart
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # plt.show()

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

    # Pie chart Data
    labels = ['Transport', 'Basalton', 'Installation', 'Geotextile', 'Filter material', 'Installation filter', 'Filling material']
    sizes = [ECI_Transport_Bas, ECI_Basalton, ECI_installation_Bas, ECI_Geotextile_Bas, ECI_filter_Bas, ECI_Installation_filter_Bas, ECI_split_Bas]

    # Create a pie chart
    # plt.figure(figsize=(8, 8))
    plt.subplot(3, 2, 3)
    plt.pie(sizes, labels=sizes, startangle=0)
    plt.legend(labels=labels, bbox_to_anchor=(1, 0.5), loc='center right')

    # Title
    plt.title('ECI Distribution Basalton')

    # Display the pie chart
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # plt.show()
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

    # Pie chart Data
    labels = ['Transport', 'Asphalt', 'Removing asphalt', 'Foundation material sand', 'Installation sand', 'Densify sand', 'Apply asphalt', 'Densify asphalt', 'Adhesive coating']
    sizes = [ECI_Transport_As, ECI_Asphalt, ECI_crusher_As, ECI_sand_As, ECI_installation_sand_As, ECI_densify_sand_As, ECI_crawler_crane_As, ECI_roller_As, ECI_coating_As]

    # Create a pie chart
    # plt.figure(figsize=(8, 8))
    plt.subplot(3, 2, 4)
    plt.pie(sizes, labels=sizes, startangle=0)
    plt.legend(labels=labels, bbox_to_anchor=(1, 0.5), loc='center right')

    # Title
    plt.title('ECI Distribution Asphalt')

    # Display the pie chart
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # plt.show()
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

    # Pie chart Data
    labels = ['Transport', 'Clay', 'Excavation works', 'Transport soil to depot', 'Processing soil in depot', 'Densify clay', 'Profiling', 'Sowing grass', 'Maintenance']
    sizes = [ECI_Transport_Gr, ECI_clay_Gr, ECI_excavation_Gr, ECI_transport_depot_Gr, ECI_process_depot_Gr, ECI_densify_Gr, ECI_bulldozer_prof_Gr, ECI_sowing_Gr, ECI_maintenance_Gr]

    # Create a pie chart
    # plt.figure(figsize=(8, 8))
    plt.subplot(3, 2, 5)
    plt.pie(sizes, labels=sizes, startangle=0)
    plt.legend(labels=labels, bbox_to_anchor=(1, 0.5), loc='center right')

    # Title
    plt.title('ECI Distribution Grass')

    # Display the pie chart
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

