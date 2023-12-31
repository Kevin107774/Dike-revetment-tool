# This is where all ECI values for different components are stored as a library for further calculations.


import numpy as np
import openturns as ot
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as matplotlib

ot.Log.Show(ot.Log.NONE)


class ECILib:

    length =np.sqrt((1.80 + 0.37)**2 + ((1.80 + 0.37) * 3.73)**2)
    kuubs = length * 2 * 0.59
    vierkant = length
    Maintenance_S2 = 0.59 * (2 / 10) * 50 * 0.2
    kuubs90 = length * 2 * 0.90
    Maintenance_S290 = 0.90 * (2 / 10) * 50 * 0.2
    # print(length)

    # Loose Rock
    # Transport per bulk carrier from Norway [m3]
    ECI_Transport_LR = 3.89     #650 km
    ECI_Transport_LR_100 = 0.60 #100 km

    # Loose Rock [m3]
    ECI_LR = 2.95

    # Loose Rock Maintenance [m3]
    ECI_LR_maintenance = 3.94

    # Installation loose rock [m2]
    ECI_crawler_crane_LR = 0.04
    ECI_excavator_LR = 0.003
    ECI_installation_LR = 0.043
    ECI_installation_electric = 0

    # Filter layer [m3]
    ECI_filter_LR = 7.80

    # Pie chart Data
    labels = ['Transport [m3]', 'Loose Rock [m3]', 'Installation [m2]',
              'Filter Layer [m3]', 'Maintenance [m3]']
    sizes = [round(ECI_Transport_LR * kuubs, 1), round(ECI_LR * kuubs, 1), round(ECI_installation_LR * vierkant, 1), round(ECI_filter_LR * vierkant * 0.2, 1), round(ECI_LR_maintenance * Maintenance_S2, 1)]
    sizestransp = [round(ECI_Transport_LR_100 * kuubs, 1), round(ECI_LR * kuubs, 1), round(ECI_installation_LR * vierkant, 1), round(ECI_filter_LR * vierkant * 0.2, 1), round(ECI_LR_maintenance * Maintenance_S2, 1)]
    sizes90 = [round(ECI_Transport_LR * kuubs90, 1), round(ECI_LR * kuubs90, 1), round(ECI_installation_LR * vierkant, 1), round(ECI_filter_LR * vierkant * 0.2, 1), round(ECI_LR_maintenance * Maintenance_S290, 1)]
    sizeselec = [round(ECI_Transport_LR * kuubs, 1), round(ECI_LR * kuubs, 1), round(ECI_installation_electric * vierkant, 1), round(ECI_filter_LR * vierkant * 0.2, 1), round(ECI_LR_maintenance * Maintenance_S2, 1)]

    # sizes = [round(ECI_Transport_LR, 1), round(ECI_LR, 1), round(ECI_installation_LR, 1), round(ECI_filter_LR, 1), round(ECI_LR_maintenance, 1)]

    # Create a pie chart
    # plt.figure(figsize=(7, 10))
    font = {'size': 15}
    matplotlib.rc('font', **font)
    f, a = plt.subplots(1, 3)
    # Create the pie chart with actual values as labels
    a[0].pie(sizes, labels=sizes, autopct='%0.1f%%', startangle=0)
    a[1].pie(sizestransp, labels=sizestransp, autopct='%0.1f%%', startangle=0)
    a[2].pie(sizes90, labels=sizes90, autopct='%0.1f%%', startangle=0)
    # a[1, 1].pie(sizeselec, labels=sizeselec, autopct='%0.1f%%', startangle=0)

    a[0].set_title("Original ECI distribution\nECI = 85.8 Euro")
    a[1].set_title("Transport distance to 100 km\nECI = 53.2 Euro")
    a[2].set_title("Nominal rock diameter of 0.90 m\nECI = 123.8 Euro")
    # a[1, 1].set_title("Sustainable installation, ECI = 88 Euro")

    plt.legend(labels=labels, bbox_to_anchor=(1.7, 0.5), fontsize="12", loc='center right')

    # Display the pie chart
    f.tight_layout()
    # plt.show()

# ------------------------------------------------------------------------
    # Placed elements (Verkalit)
    length = np.sqrt((2.4 - 1.79)**2 + ((2.4-1.79) * 7.7)**2)
    kuubs_ver = length * 0.2
    vierkant_ver = length
    kuubs_ver40 = length * 0.4

    # Transport per truck from Friesland [m3]
    ECI_Transport_Ver = 1.01    # 38 km
    ECI_Transport_Ver_200 = 6.04 # 228 km

    # Verkalit [m3]
    ECI_verkalit = 26.30

    # Installation Verkalit [m2]
    ECI_vessel_Ver = 0.11
    ECI_excavator_Ver = 0.07
    ECI_installation_Ver = ECI_excavator_Ver + ECI_vessel_Ver
    ECI_installation_Ver_elec = 0

    # Geotextile [m2]
    ECI_Geotextile_Ver = 0.45

    # Filter [m3]
    ECI_filter_Ver = 7.80

    # Pie chart Data
    labels = ['Transport [m3]', 'Verkalit [m3]', 'Installation [m2]', 'Filter material [m3]', 'Geotextile [m2]']
    sizes = [round(ECI_Transport_Ver * kuubs_ver, 1), round(ECI_verkalit * kuubs_ver, 1), round(ECI_installation_Ver * vierkant_ver, 1), round(ECI_filter_Ver * vierkant_ver * 0.2, 1), round(ECI_Geotextile_Ver * vierkant_ver, 1)]
    sizestransp = [round(ECI_Transport_Ver_200 * kuubs_ver, 1), round(ECI_verkalit * kuubs_ver, 1), round(ECI_installation_Ver * vierkant_ver, 1), round(ECI_filter_Ver * vierkant_ver * 0.2, 1), round(ECI_Geotextile_Ver * vierkant_ver, 1)]
    sizes40 = [round(ECI_Transport_Ver * kuubs_ver40, 1), round(ECI_verkalit * kuubs_ver40, 1), round(ECI_installation_Ver * vierkant_ver, 1), round(ECI_filter_Ver * vierkant_ver * 0.2, 1), round(ECI_Geotextile_Ver * vierkant_ver, 1)]
    sizeselec = [round(ECI_Transport_Ver * kuubs_ver, 1), round(ECI_verkalit * kuubs_ver, 1), round(ECI_installation_Ver_elec * vierkant_ver, 1), round(ECI_filter_Ver * vierkant_ver * 0.2, 1), round(ECI_Geotextile_Ver * vierkant_ver, 1)]
    # sizes = [round(ECI_Transport_Ver_200, 1), round(ECI_verkalit, 1), round(ECI_installation_Ver, 1), round(ECI_filter_Ver, 1), round(ECI_Geotextile_Ver, 1)]

    # Create a pie chart
    # plt.figure(figsize=(7, 10))
    font = {'size': 15}
    matplotlib.rc('font', **font)
    f, a = plt.subplots(1, 3)
    # Create the pie chart with actual values as labels
    a[0].pie(sizes, labels=sizes, autopct='%0.1f%%', startangle=0)
    a[1].pie(sizestransp, labels=sizestransp, autopct='%0.1f%%', startangle=0)
    a[2].pie(sizes40, labels=sizes40, autopct='%0.1f%%', startangle=0)
    # a[1, 1].pie(sizeselec, labels=sizeselec, autopct='%0.1f%%', startangle=0)

    a[0].set_title("Original ECI distribution\nECI = 36.3 Euro")
    a[1].set_title("Transport distance to 228 km\nECI = 41 Euro")
    a[2].set_title("Element diameter to 0.4 m\nECI = 62.1 Euro")
    # a[1, 1].set_title("Sustainable installation, ECI = 42.6 Euro")

    plt.legend(labels=labels, bbox_to_anchor=(1.7, 0.5), fontsize="12", loc='center right')

    # Display the pie chart
    f.tight_layout()
    # plt.show()

# ------------------------------------------------------------------------
    # Placed elements (Basalton)
    kuubs_Bas = length * 0.2
    vierkant_Bas = length
    kuubs_Bas40 = length * 0.4

    # Transport per truck from Alphen a/d Rijn [m3]
    ECI_Transport_Bas = 6.04        # Transport 200 km
    ECI_Transport_Bas_30 = 1.01     # Transport 38 km

    # Basalton [m3]
    ECI_Basalton = 17.88

    # Installation Basalton [m2]
    ECI_vessel_Bas = 0.11
    ECI_excavator_Bas = 0.07
    ECI_installation_Bas = ECI_excavator_Bas + ECI_vessel_Bas
    ECI_installation_Bas_elec = 0

    # Geotextile [m2]
    ECI_Geotextile_Bas = 0.45

    # Filter [m3]
    ECI_filter_Bas = 7.80

    # Filling material [m3]
    ECI_split_Bas = 7.80

    # Pie chart Data
    labels = ['Transport [m3]', 'Basalton [m3]', 'Installation [m2]', 'Filter material [m3]', 'Geotextile [m2]', 'Filling material [m3]']
    sizes = [round(ECI_Transport_Bas * kuubs_Bas, 1), round(ECI_Basalton * kuubs_Bas, 1), round(ECI_installation_Bas * vierkant_Bas, 1), round(ECI_filter_Bas * vierkant_Bas * 0.2, 1), round(ECI_Geotextile_Bas * vierkant_Bas, 1), round(ECI_split_Bas * 0.1 * vierkant_Bas, 1)]
    sizestransp = [round(ECI_Transport_Bas_30 * kuubs_Bas, 1), round(ECI_Basalton * kuubs_Bas, 1), round(ECI_installation_Bas * vierkant_Bas, 1), round(ECI_filter_Bas * vierkant_Bas * 0.2, 1), round(ECI_Geotextile_Bas * vierkant_Bas, 1), round(ECI_split_Bas * 0.1 * vierkant_Bas, 1)]
    sizes40 = [round(ECI_Transport_Bas * kuubs_Bas40, 1), round(ECI_Basalton * kuubs_Bas40, 1), round(ECI_installation_Bas * vierkant_Bas, 1), round(ECI_filter_Bas * vierkant_Bas * 0.2, 1), round(ECI_Geotextile_Bas * vierkant_Bas, 1), round(ECI_split_Bas * 0.1 * vierkant_Bas, 1)]
    sizeselec = [round(ECI_Transport_Bas * kuubs_Bas, 1), round(ECI_Basalton * kuubs_Bas, 1), round(ECI_installation_Bas_elec * vierkant_Bas, 1), round(ECI_filter_Bas * vierkant_Bas * 0.2, 1), round(ECI_Geotextile_Bas * vierkant_Bas, 1), round(ECI_split_Bas * 0.1 * vierkant_Bas, 1)]
    # sizes = [round(ECI_Transport_Bas, 1), round(ECI_Basalton, 1), round(ECI_installation_Bas, 1), round(ECI_filter_Bas, 1), round(ECI_Geotextile_Bas, 1), round(ECI_split_Bas, 1)]

    # Create a pie chart
    # plt.figure(figsize=(7, 10))
    font = {'size': 15}
    matplotlib.rc('font', **font)
    f, a = plt.subplots(1, 3)
    # Create the pie chart with actual values as labels
    a[0].pie(sizes, labels=sizes, autopct='%0.1f%%', startangle=0)
    a[1].pie(sizestransp, labels=sizestransp, autopct='%0.1f%%', startangle=0)
    a[2].pie(sizes40, labels=sizes40, autopct='%0.1f%%', startangle=0)
    # a[1, 1].pie(sizeselec, labels=sizeselec, autopct='%0.1f%%', startangle=0)

    a[0].set_title("Original ECI distribution\nECI = 36.7 Euro")
    a[1].set_title("Transport distance to 38 km\nECI = 32 Euro")
    a[2].set_title("Element diameter to 0.4 m\nECI = 59.4 Euro")
    # a[1, 1].set_title("Sustainable installation, ECI = 42.3 Euro")

    plt.legend(labels=labels, bbox_to_anchor=(1.7, 0.5), fontsize="12", loc='center right')

    # Display the pie chart
    f.tight_layout()
    # plt.show()
# ------------------------------------------------------------------------
    # Asphalt
    length = np.sqrt((6.15 - 2.4) ** 2 + ((6.15 - 2.4) * 3.75) ** 2)
    kuubs_As = length * 0.30
    vierkant_As = length
    kuubs_As30 = length * 0.15        # 0.3m thick layer
    print(length)

    # Transport asphalt from factory 36 km [m3]
    ECI_Transport_As = 0.86
    ECI_Transport_As100 = 2.4         # 100 km transport

    # Asphalt [m3]
    ECI_Asphalt = 47.71

    # Foundation sand [m3]
    ECI_sand_As = 4.04

    # Profiling slope and apply asphalt [m2]
    ECI_crawler_crane_As = 2.57
    ECI_densify_asphalt = 0.47
    ECI_installation_As = ECI_crawler_crane_As + ECI_densify_asphalt
    ECI_installation_As_elec = 0

    # Adhesive coating [m2]
    ECI_coating_As = 0.12

    # Pie chart Data
    labels = ['Transport [m3]', 'Asphalt [m3]', 'Apply asphalt [m2]', 'Foundation sand [m3]', 'Adhesive coating [m2]']
    sizes = [round(ECI_Transport_As * kuubs_As, 1), round(ECI_Asphalt * kuubs_As, 1), round(ECI_installation_As * vierkant_As, 1), round(ECI_sand_As * vierkant_As * 0.2, 1),  round(ECI_coating_As * vierkant_As, 1)]
    sizestransp = [round(ECI_Transport_As100 * kuubs_As, 1), round(ECI_Asphalt * kuubs_As, 1), round(ECI_installation_As * vierkant_As, 1), round(ECI_sand_As * vierkant_As * 0.2, 1),  round(ECI_coating_As * vierkant_As, 1)]
    sizes30 = [round(ECI_Transport_As * kuubs_As30, 1), round(ECI_Asphalt * kuubs_As30, 1), round(ECI_installation_As * vierkant_As, 1), round(ECI_sand_As * vierkant_As * 0.2, 1),  round(ECI_coating_As * vierkant_As, 1)]
    sizeselec = [round(ECI_Transport_As * kuubs_As, 1), round(ECI_Asphalt * kuubs_As, 1), round(ECI_installation_As_elec * vierkant_As, 1), round(ECI_sand_As * vierkant_As * 0.2, 1),  round(ECI_coating_As * vierkant_As, 1)]
    # sizes = [round(ECI_Transport_As, 1), round(ECI_Asphalt, 1), round(ECI_installation_As, 1), round(ECI_sand_As, 1),  round(ECI_coating_As, 1)]

    # Create a pie chart
    # plt.figure(figsize=(7, 10))
    font = {'size': 15}
    matplotlib.rc('font', **font)
    f, a = plt.subplots(1, 3)
    # Create the pie chart with actual values as labels
    a[0].pie(sizes, labels=sizes, autopct='%0.1f%%', startangle=0)
    a[1].pie(sizestransp, labels=sizestransp, autopct='%0.1f%%', startangle=0)
    a[2].pie(sizes30, labels=sizes30, autopct='%0.1f%%', startangle=0)
    # a[1, 1].pie(sizeselec, labels=sizeselec, autopct='%0.1f%%', startangle=0)

    a[0].set_title("Original ECI distribution\nECI = 269.8 Euro")
    a[1].set_title("Transport distance to 100 km\nECI = 276.5 Euro")
    a[2].set_title("Layer thickness to 0.3 m\nECI = 163.8 Euro")
    # a[1, 1].set_title("Sustainable installation, ECI = 119.4 Euro")

    plt.legend(labels=labels, bbox_to_anchor=(1.7, 0.5), fontsize="12", loc='center right')

    # Display the pie chart
    f.tight_layout()
    # plt.show()
# ------------------------------------------------------------------------
    # Grass
    length = np.sqrt((8.22-6.15) ** 2 + ((8.22-6.15) * 4) ** 2)
    kuubs_Gr = length * 1.4
    vierkant_Gr = length
    kuubs_Gr2 = length * 2

    # Transport grass from Betuwe (312 km) [m3] (binnenvaartschip)
    ECI_Transport_Gr = 2.78
    ECI_Transport_Gr_40 = 1.06  # Transport 40 km met vrachtwagen

    # Clay [m3]
    ECI_clay_Gr = 2.56

    # Apply Clay [m3]
    ECI_crawler_crane_Gr = 0.03
    ECI_bulldozer_Gr = 0.03
    ECI_densify_Gr = 0.02
    ECI_bulldozer_prof_Gr = 0.02
    ECI_apply_clay_GR = ECI_crawler_crane_Gr + ECI_bulldozer_Gr + ECI_densify_Gr + ECI_bulldozer_prof_Gr
    ECI_apply_clay_GR_elec = 0

    # Sowing grass [m2]
    ECI_sowing_Gr = 0.01
    ECI_sowing_Gr_elec = 0

    # Maintenance (sheep) [m2]
    ECI_maintenance_Gr = 0.00

    # Pie chart Data
    labels = ['Transport [m3]', 'Clay [m3]', 'Apply clay [m3]', 'Sowing grass [m2]', 'Maintenance [m2]']
    sizes = [round(ECI_Transport_Gr * kuubs_Gr, 1), round(ECI_clay_Gr * kuubs_Gr, 1), round(ECI_apply_clay_GR * kuubs_Gr, 1), round(ECI_sowing_Gr * vierkant_Gr, 1), round(ECI_maintenance_Gr * vierkant_Gr, 1)]
    sizestransp = [round(ECI_Transport_Gr_40 * kuubs_Gr, 1), round(ECI_clay_Gr * kuubs_Gr, 1), round(ECI_apply_clay_GR * kuubs_Gr, 1), round(ECI_sowing_Gr * vierkant_Gr, 1), round(ECI_maintenance_Gr * vierkant_Gr, 1)]
    sizes2 = [round(ECI_Transport_Gr * kuubs_Gr2, 1), round(ECI_clay_Gr * kuubs_Gr2, 1), round(ECI_apply_clay_GR * kuubs_Gr2, 1), round(ECI_sowing_Gr * vierkant_Gr, 1), round(ECI_maintenance_Gr * vierkant_Gr, 1)]
    sizeselec = [round(ECI_Transport_Gr * kuubs_Gr, 1), round(ECI_clay_Gr * kuubs_Gr, 1), round(ECI_apply_clay_GR_elec * kuubs_Gr, 1), round(ECI_sowing_Gr_elec * vierkant_Gr, 1), round(ECI_maintenance_Gr * vierkant_Gr, 1)]
    # sizes = [round(ECI_Transport_Gr, 1), round(ECI_clay_Gr, 1), round(ECI_apply_clay_GR, 1), round(ECI_sowing_Gr, 1), round(ECI_maintenance_Gr, 1)]

    # Create a pie chart
    # plt.figure(figsize=(7, 10))
    font = {'size': 15}
    matplotlib.rc('font', **font)
    f, a = plt.subplots(1, 3)
    # Create the pie chart with actual values as labels
    a[0].pie(sizes, labels=sizes, autopct='%0.1f%%', startangle=0)
    a[1].pie(sizestransp, labels=sizestransp, autopct='%0.1f%%', startangle=0)
    a[2].pie(sizes2, labels=sizes2, autopct='%0.1f%%', startangle=0)
    # a[1, 1].pie(sizeselec, labels=sizeselec, autopct='%0.1f%%', startangle=0)

    a[0].set_title("Original ECI distribution\nECI = 65.1 Euro")
    a[1].set_title("Transport distance to 40 km\nECI = 44.6 Euro")
    a[2].set_title("Clay layer thicknes to 2 m\nECI = 93 Euro")
    # a[1, 1].set_title("Sustainable installation, ECI = 63.4 Euro")

    plt.legend(labels=labels, bbox_to_anchor=(1.7, 0.5), fontsize="12", loc='center right')

    # Display the pie chart
    f.tight_layout()
    plt.show()

