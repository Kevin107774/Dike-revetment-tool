# Library for all (non-hydraulic) parameters

import numpy as np
import openturns as ot
import pandas as pd

ot.Log.Show(ot.Log.NONE)

Hydraulic_BC = pd.read_excel(
    r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Hydra en Steentoets\Hydra-NL\Hydraulic boundary '
    r'conditions.xlsx')


class Parameters:
    # Signficant wave height
    Significant_wave_height = 0.5

    # Density rock
    Expected_value_rho_s = 2650
    COV = 0.03
    Standard_deviation = COV * Expected_value_rho_s
    # Distribution = 'Normal'
    Density_rock = ot.Normal(Expected_value_rho_s, Standard_deviation)

    # Density water
    Expected_value_rho_w = 1025
    COV = 0.03
    Standard_deviation = COV * Expected_value_rho_w
    # Distribution = 'Normal'
    Density_water = ot.Normal(Expected_value_rho_w, Standard_deviation)

    # Nominal diameter rock
    Standard_nominal_diameter = np.array([0.31, 0.34, 0.38, 0.59, 0.90, 1.18, 1.44])
    Dn50 = []
    mu_Dn50 = []
    for i in Standard_nominal_diameter:
        Expected_value_Dn50 = i
        COV = 0.03
        Standard_deviation = COV * Expected_value_Dn50
        # Distribution = 'Normal'
        mu_Dn50.append(Expected_value_Dn50)
        Nominaml_diameter_rock_50 = ot.Normal(Expected_value_Dn50, Standard_deviation)
        Dn50.append(Nominaml_diameter_rock_50)

    # Porosity
    Expected_value_P = 0.1
    Standard_deviation = 0.01
    mu = np.log(Expected_value_P ** 2 / np.sqrt(Standard_deviation ** 2 + Expected_value_P ** 2))
    sigma = np.log(1 + Standard_deviation ** 2 / Expected_value_P ** 2)
    # print(mu, sigma)
    Distribution = 'Lognormal'
    # Distribution = 'Normal'
    Porosity = ot.LogNormal(mu, sigma, 0)
    # print(Porosity)

    # Damage number [S]
    Damage_number = np.linspace(2, 17, 16)

    # Uncertainty parameter a (C_pl)
    Expected_value_a = 6.2
    Standard_deviation = 0.4
    # Distribution = 'Normal'
    Uncertainty_a = ot.Normal(Expected_value_a, Standard_deviation)

    # Uncertainty parameter b (C_s)
    Expected_value_b = 1
    Standard_deviation = 0.08
    # Distribution = 'Normal'
    Uncertainty_b = ot.Normal(Expected_value_b, Standard_deviation)

    # Storm duration
    Expected_value_t = 36000
    COV = 0.5
    Standard_deviation = COV * Expected_value_t
    mu = np.log(Expected_value_t ** 2 / np.sqrt(Standard_deviation ** 2 + Expected_value_t ** 2))
    sigma = np.log(1 + Standard_deviation ** 2 / Expected_value_t ** 2)
    Distribution = 'Lognormal'
    Storm_duration = ot.LogNormal(mu, sigma, 0)
    # print(mu, sigma)

    # Peak period
    Peak_period = 5

    # Wavelength
    Wavelength = Peak_period * np.sqrt(9.81 * 3)

    # Slope angle 1
    Expected_value_alpha1 = 1 / 5.68
    COV = 0.05
    Standard_deviation = COV * Expected_value_alpha1
    # Distribution = 'Normal'
    Slope_angle1 = ot.Normal(Expected_value_alpha1, Standard_deviation)

    # Create parameter combinations

    columns_Loose_Rock = ['Waterlevel +mNAP', 'Significant wave height', 'Peak period', 'Storm duration',
                          'Density rock', 'Density water', 'Nominal diameter rock', 'Porosity',
                          'Damage number [S]', 'Uncertainty parameter C_pl', 'Uncertainty parameter C_s', 'Slope angle']

    Data = []
    for index, k in Hydraulic_BC.iloc[6:8, :].iterrows():
        Hs = k[2]
        Tp = k[4]
        t = k[7]
        h = k[1]
        a = k[16]
        dfs = []
        for i in mu_Dn50:
            rows = []
            for j in Damage_number:
                input = {'Waterlevel +mNAP': h, 'Significant wave height': Hs, 'Peak period': Tp, 'Storm duration': t,
                         'Density rock': Expected_value_rho_s, 'Density water': Expected_value_rho_w,
                         'Nominal diameter rock': i, 'Porosity': Expected_value_P, 'Damage number [S]': j,
                         'Uncertainty parameter C_pl': Expected_value_a, 'Uncertainty parameter C_s': Expected_value_b,
                         'Slope angle': a}
                rows.append(input)
            combinations_LR = pd.DataFrame(rows, columns=columns_Loose_Rock)
            dfs.append(combinations_LR)
        Data.append(pd.concat(dfs, ignore_index=True))
    parameter_combinations_LR = pd.concat(Data, ignore_index=True)
    pd.set_option('display.max_columns', None)
    # print(parameter_combinations_LR)
    # Export the DataFrame to an Excel file


    # ------------------------------------------------------------------------
    # Asphalt layer thickness d [m]
    Asphalt_layer_thickness = np.array([0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.4, 0.45, 0.5])
    d_a = []
    mu_da = []
    for i in Asphalt_layer_thickness:
        Expected_value = i
        COV = 0.1
        Standard_deviation = COV * Expected_value

        asphalt_thickness = ot.Normal(Expected_value, Standard_deviation)
        mu_da.append(Expected_value)
        d_a.append(asphalt_thickness)

        # mu = np.log(Expected_value ** 2 / np.sqrt(Standard_deviation ** 2 + Expected_value ** 2))
        # sigma = np.log(1 + Standard_deviation ** 2 / Expected_value ** 2)
        # # Distribution = 'Lognormal'
        # mu_da.append(Expected_value)
        # Asphalt_thickness = ot.LogNormal(mu, sigma, 0)
        # d_a.append(Asphalt_thickness)



    # Slope depending factor Q_n [-] --> Depends on graph pg. 123 TAW 2002
    Slope_depending_uplift_factor = 1.005

    # Phreatic surface [mNAP]
    Ps = 5.28

    # Water level h [mNAP] --> Dit moet uit Hydra-NL worden gehaald
    h = 3.76

    # Vertical distance between lower bound impermeable layer to outer design water level a [m]
    Vert_a = h - 2.41

    # Vertical distance between the outer design water level and design level of the phreatic surface v [m]
    Vert_v = Ps - h

    # Density asphalt rho_a [kg/m3]
    Expected_value_rho_a = 2325
    # COV = 0.0217
    Standard_deviation = 10
    # Distribution = 'Normal'
    Density_asphalt = ot.Normal(Expected_value_rho_a, Standard_deviation)

    # Reduction factor due to the relative position of the outer water level to the phreatic surface R_w [-] --> From
    # graph pg 121 TAW 2002, depends on a and v.
    Reduction_factor = 1

    # Fatigue parameter beta [-]
    Beta = 5.4

    # Fatigue parameter alpha [-]
    alpha = 0.5

    # Cracking strength [Mpa]
    Expected_value_crackingstrength = 6.3*10**6
    COV = 0.2
    Standard_deviation = Expected_value_crackingstrength * COV
    # Distribution = 'Normal'
    crackingstrength = ot.Normal(Expected_value_crackingstrength, Standard_deviation)

    # Stiffness subsoil c [MPa/m]
    Expected_value_c = 100*10**6
    COV = 0.25
    Standard_deviation = COV * Expected_value_c
    mu = np.log(Expected_value_c ** 2 / np.sqrt(Standard_deviation ** 2 + Expected_value_c ** 2))
    sigma = np.log(1 + Standard_deviation ** 2 / Expected_value_c ** 2)
    # Distribution = 'Lognormal'
    Stiffness_subsoil = ot.LogNormal(mu, sigma, 0)

    # Elasticity modulus asphalt E [MPa]
    Expected_value_E = 4260*10**6
    COV = 0.2
    Standard_deviation = COV * Expected_value_E
    # Distribution = 'Normal'
    Elasticity_modulus = ot.Normal(Expected_value_E, Standard_deviation)

    # Transverse contraction coefficient v [-]
    v = 0.35

    # gravity g [m/s^2]
    g = 9.81

    # Slope depending impact factor q for slope 1:3.75 [-]
    # q_r = 0.0455
    Expected_value_q_r = 3.45
    COV = 0.5
    Standard_deviation = COV * Expected_value_q_r
    mu = np.log(Expected_value_q_r ** 2 / np.sqrt(Standard_deviation ** 2 + Expected_value_q_r ** 2))
    sigma = np.log(1 + Standard_deviation ** 2 / Expected_value_q_r ** 2)
    # Distribution = 'Lognormal'
    Slope_impact_factor = ot.LogNormal(mu, sigma, 0)

    # Slope Asphalt layer a3 [-]
    Expected_value_a3 = 1 / 3.75
    COV = 0.05
    Standard_deviation = COV * Expected_value_a3
    # Distribution = 'Normal'
    Slope_angle3 = ot.Normal(Expected_value_a3, Standard_deviation)

    # Create parameter combinations

    columns_Asphalt = ['Water level +mNAP', 'Significant wave height', 'Peak period', 'Storm duration',
                       'Phreatic surface', 'Vertical distance a', 'Vertical distance v', 'Reduction factor R',
                       'Asphalt layer thickness', 'Density asphalt', 'slope asphalt', 'Slope depending uplift factor',
                       'Fatigue parameter Beta', 'Fatigue parameter alpha', 'Limit strength', 'Stiffness subsoil',
                       'Elasticity modulus', 'Transverse contraction coefficient', 'gravity']

    hydra = []
    for index, k in Hydraulic_BC.iloc[12:32, :].iterrows():
        Hs = k[2]
        Tp = k[4]
        t = k[7]
        h = k[1]
        a = k[16]
        a_vert = k[18]
        v_vert = k[19]
        R = k[21]

        param = []
        for i in mu_da:
            input = {'Water level +mNAP': h, 'Significant wave height': Hs, 'Peak period': Tp, 'Storm duration': t,
                     'Phreatic surface': Ps, 'Vertical distance a': a_vert, 'Vertical distance v': v_vert,
                     'Reduction factor R': R, 'Asphalt layer thickness': i, 'Density asphalt': Expected_value_rho_a,
                     'slope asphalt': a, 'Slope depending uplift factor': Slope_depending_uplift_factor,
                     'Fatigue parameter Beta': Beta, 'Fatigue parameter alpha': alpha,
                     'Limit strength': Expected_value_crackingstrength, 'Stiffness subsoil': Expected_value_c,
                     'Elasticity modulus': Expected_value_E, 'Transverse contraction coefficient': v, 'gravity': g}
            param.append(input)
        combinations_asphalt = pd.DataFrame(param, columns=columns_Asphalt)
        hydra.append(combinations_asphalt)

    parameter_combinations_asphalt = pd.concat(hydra, ignore_index=True)
    pd.set_option('display.max_columns', None)
    # print(parameter_combinations_asphalt)

    # -----------------------------------------------------------------------------------------

    # Density concrete
    Density_concrete = np.linspace(2650, 3000, 8)
    rho_c = []
    mu_rho_c = []
    for i in Density_concrete:
        Expected_value_rho_c = i
        COV = 0.0103
        Standard_deviation = COV * Expected_value_rho_c
        mu_rho_c.append(Expected_value_rho_c)
        Density_Concrete_distributions = ot.Normal(Expected_value_rho_c, Standard_deviation)
        rho_c.append(Density_Concrete_distributions)

    # Layer thickness Basalton
    Layer_thickness_Basalton = np.linspace(0.2, 0.6, 9)
    d_B = []
    mu_d_B = []
    for i in Layer_thickness_Basalton:
        Expected_value_d_B = i
        COV = 0.0304
        Standard_deviation = COV * Expected_value_d_B
        mu_d_B.append(Expected_value_d_B)
        Layer_thickness_Basalton_distribution = ot.Normal(Expected_value_d_B, Standard_deviation)
        d_B.append(Layer_thickness_Basalton_distribution)

    # Layer thickness Verkalit
    Layer_thickness_Verkalit = np.linspace(0.2, 0.6, 9)
    d_V = []
    mu_d_V = []
    for i in Layer_thickness_Verkalit:
        Expected_value_d_V = i
        COV = 0.0304
        Standard_deviation = COV * Expected_value_d_V
        mu_d_V.append(Expected_value_d_V)
        Layer_thickness_Verkalit_distribution = ot.Normal(Expected_value_d_V, Standard_deviation)
        d_V.append(Layer_thickness_Verkalit_distribution)

    # Angle of incidence waves --> Hydra
    B = 0

    # Coefficient for length of loading 1
    c1 = 0.15

    # Coefficient for length of loading 2
    c2 = 0.85

    # Safety factor
    gamma_s = 1.1

    # Thickness filter 1
    b1 = 0.06

    # Permeability geotextile
    k2 = 0.00286

    # Thickness geotextile
    b2 = 0.0053

    # Kinematic viscosity water
    kin_v = 1.2 * 10 ** -6

    # Porosity granular material
    n_f = 0.35

    # Diameter filter material D15
    D_f15 = 0.004

    # Upper level transition height
    Zb = 2.41

    # Factor for Verkalit calculation
    f_V = 1.14

    # Create parameter combinations Basalton

    columns_Basalton = ['Waterlevel +mNAP', 'Significant wave height', 'Peak period', 'Mean wave period',
                        'Storm duration', 'Layer thickness Basalton', 'Density concrete', 'Slope angle',
                        'Angle of incidence', 'Coefficient for length of loading c1',
                        'Coefficient for length of loading c2', 'Thickness filter',
                        'Permeability geotextile', 'Thickness geotextile', 'Kinematic viscosity water',
                        'Porosity granular material', 'Diameter filter material D15', 'Upper level transition height']

    Hydra = []
    for index, k in Hydraulic_BC.iloc[13:21, :].iterrows():
        Hs = k[2]
        Tp = k[4]
        Tm = k[9]
        t = k[7]
        h = k[1]
        a = k[16]
        density = []
        for i in mu_rho_c:
            diameter = []
            for j in mu_d_B:
                input = {'Waterlevel +mNAP': h, 'Significant wave height': Hs, 'Peak period': Tp,
                         'Mean wave period': Tm, 'Storm duration': t, 'Layer thickness Basalton': j,
                         'Density concrete': i, 'Slope angle': a, 'Angle of incidence': B,
                         'Coefficient for length of loading c1': c1, 'Coefficient for length of loading c2': c2,
                         'Thickness filter': b1, 'Permeability geotextile': k2, 'Thickness geotextile': b2,
                         'Kinematic viscosity water': kin_v, 'Porosity granular material': n_f,
                         'Diameter filter material D15': D_f15, 'Upper level transition height': Zb}
                diameter.append(input)
            combinations_Basalton = pd.DataFrame(diameter, columns=columns_Basalton)
            density.append(combinations_Basalton)
        Hydra.append(pd.concat(density, ignore_index=True))
    parameter_combinations_Basalton = pd.concat(Hydra, ignore_index=True)
    pd.set_option('display.max_columns', None)
    # print(parameter_combinations_Basalton)


    # Create parameter combinations Verkalit

    columns_Verkalit = ['Waterlevel +mNAP', 'Significant wave height', 'Peak period', 'Mean wave period',
                        'Storm duration', 'Layer thickness Verkalit', 'Density concrete', 'Slope angle',
                        'Angle of incidence', 'Coefficient for length of loading c1',
                        'Coefficient for length of loading c2', 'Thickness filter',
                        'Permeability geotextile', 'Thickness geotextile', 'Kinematic viscosity water',
                        'Porosity granular material', 'Diameter filter material D15', 'Upper level transition height',
                        'Factor Verkalit']

    Hydra2 = []
    for index, k in Hydraulic_BC.iloc[13:21, :].iterrows():
        Hs = k[2]
        Tp = k[4]
        Tm = k[9]
        t = k[7]
        h = k[1]
        a = k[16]
        density2 = []
        for i in mu_rho_c:
            diameter2 = []
            for j in mu_d_V:
                input = {'Waterlevel +mNAP': h, 'Significant wave height': Hs, 'Peak period': Tp,
                         'Mean wave period': Tm, 'Storm duration': t, 'Layer thickness Verkalit': j,
                         'Density concrete': i, 'Slope angle': a, 'Angle of incidence': B,
                         'Coefficient for length of loading c1': c1, 'Coefficient for length of loading c2': c2,
                         'Thickness filter': b1, 'Permeability geotextile': k2, 'Thickness geotextile': b2,
                         'Kinematic viscosity water': kin_v, 'Porosity granular material': n_f,
                         'Diameter filter material D15': D_f15, 'Upper level transition height': Zb,
                         'Factor Verkalit': f_V}
                diameter2.append(input)
            combinations_Verkalit = pd.DataFrame(diameter2, columns=columns_Verkalit)
            density2.append(combinations_Verkalit)
        Hydra2.append(pd.concat(density2, ignore_index=True))
    parameter_combinations_Verkalit = pd.concat(Hydra2, ignore_index=True)
    pd.set_option('display.max_columns', None)
    # print(parameter_combinations_Verkalit)


