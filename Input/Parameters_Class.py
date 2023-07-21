import openturns as ot
import pandas as pd
from Input.Parameters import Parameters
from Input.Hydra import HydraulicBoundary

ot.Log.Show(ot.Log.NONE)


class VdMeerInput:
    distributionvdmeer2 = []
    deterministicvdmeer2 = []

    for index, i in HydraulicBoundary.HydraulicBoundariesLR().iterrows():
        Hs = i[1]
        Tp = i[2]
        t = i[3]
        h = i[0]
        a1 = i[4]
        for j in Parameters.Dn50:
            Dn50 = j
            rho_s = Parameters.Density_rock
            rho_w = Parameters.Density_water
            P = Parameters.Porosity
            C_pl = Parameters.Uncertainty_a
            C_s = Parameters.Uncertainty_b

            distributionvdmeer = ot.ComposedDistribution([Dn50, rho_w, rho_s, P, C_pl, C_s, t, a1, Hs, Tp, h])
            distributionvdmeer2.append(distributionvdmeer)

    for k in Parameters.Damage_number:
        S = k
        deterministicvdmeer = S
        deterministicvdmeer2.append(deterministicvdmeer)

    # print(len(distributionvdmeer2))
    # print(len(deterministicvdmeer2))


class ElementInput:
    # distributionbasalton = []
    distributionverkalit = []

    # for index, k in HydraulicBoundary.HydraulicBoundariesBasalton().iterrows():
    #     Hs = k[1]
    #     Tp = k[2]
    #     t = k[4]
    #     h = k[0]
    #     a = k[5]
    #     for i in Parameters.rho_c:
    #         rho_c = i
    #         for j in Parameters.d_B:
    #             d_B = j
    #             rho_w = Parameters.Density_water
    #
    #             distribution = ot.ComposedDistribution([Hs, Tp, t, h, a, rho_c, d_B, rho_w])
    #             distributionbasalton.append(distribution)
    #
    # B = Parameters.B
    # c1 = Parameters.c1
    # c2 = Parameters.c2
    # b1 = Parameters.b1
    # k2 = Parameters.k2
    # b2 = Parameters.b2
    # v_kin = Parameters.kin_v
    # n_f = Parameters.n_f
    # D_f15 = Parameters.D_f15
    # g = Parameters.g
    # Zb = Parameters.Zb
    #
    # deterministicbasalton = (B, c1, c2, b1, k2, b2, v_kin, n_f, D_f15, g, Zb)

    # print(distributionbasalton)
    # print(deterministicbasalton)

    for index, k in HydraulicBoundary.HydraulicBoundariesVerkalit().iterrows():
        Hs = k[1]
        Tp = k[2]
        t = k[4]
        h = k[0]
        a = k[5]
        for i in Parameters.rho_c:
            rho_c = i
            for j in Parameters.d_V:
                d_V = j
                rho_w = Parameters.Density_water

                distribution = ot.ComposedDistribution([Hs, Tp, t, h, a, rho_c, d_V, rho_w])
                distributionverkalit.append(distribution)

    B = Parameters.B
    c1 = Parameters.c1
    c2 = Parameters.c2
    b1 = Parameters.b1
    k2 = Parameters.k2
    b2 = Parameters.b2
    v_kin = Parameters.kin_v
    n_f = Parameters.n_f
    D_f15 = Parameters.D_f15
    g = Parameters.g
    Zb = Parameters.Zb
    f_V = Parameters.f_V

    deterministicverkalit = (B, c1, c2, b1, k2, b2, v_kin, n_f, D_f15, g, Zb, f_V)

    # print(distributionverkalit)
    # print(deterministicverkalit)


class AsphaltUpliftInput:
    distribution_uplift_asphalt = []

    for index, k in HydraulicBoundary.HydraulicBoundariesAsphalt().iterrows():
        a_vert = k[6]
        v_vert = k[7]
        R = k[8]
        a = k[5]

        for i in Parameters.d_a:
            d = i
            rho_w = Parameters.Density_water
            rho_a = Parameters.Density_asphalt

            distribution_uplift_asphalt2 = ot.ComposedDistribution([a_vert, v_vert, R, a, d, rho_w, rho_a])
            distribution_uplift_asphalt.append(distribution_uplift_asphalt2)

    # print(distribution_uplift_asphalt[0])


class AsphaltImpactInput:
    distribution_impact_asphalt = []

    for index, k in HydraulicBoundary.HydraulicBoundariesAsphalt().iterrows():
        Hs = k[1]
        Tp = k[2]
        t = k[4]
        a = k[5]
        h = k[0]

        for i in Parameters.d_a:
            q_r = Parameters.Slope_impact_factor
            rho_w = Parameters.Density_water
            c = Parameters.Stiffness_subsoil
            E = Parameters.Elasticity_modulus
            d = i
            sigma_b = Parameters.crackingstrength

            distribution_impact_asphalt2 = ot.ComposedDistribution([Hs, Tp, t, a, q_r, rho_w, c, E, d, sigma_b, h])
            distribution_impact_asphalt.append(distribution_impact_asphalt2)

    g = Parameters.g
    v = Parameters.v
    alpha = Parameters.alpha
    B = Parameters.Beta

    deterministic_impact_asphalt = (g, v, alpha, B)
    # print(distribution_impact_asphalt)
    # print(deterministic_impact_asphalt)

