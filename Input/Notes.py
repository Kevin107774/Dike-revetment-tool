# Transition Loose rock to Basalton

    def filterresults(Result_Raw, selected_amount, Req_pf=1 / 60000):
        Result_filtered = Result_Raw[Result_Raw['Probability of failure'] < Req_pf]
        Result_sorted = Result_filtered.sort_values(['Waterlevel +mNAP', 'ECI'], ascending=[True, True])
        Result_grouped = Result_sorted.groupby('Waterlevel +mNAP').head(selected_amount)
        return Result_grouped

    ## Loose Rock
    Result_Raw_LR = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\1. Loose Rock\Result Loose Rock complete.xlsx')

    Loose_rock_filtered = filterresults(Result_Raw_LR, 1)
    Loose_rock_filtered = Loose_rock_filtered[Loose_rock_filtered['Waterlevel +mNAP'] > 1.7].reset_index(drop=True)
    # print(Loose_rock_filtered)

    # Basalton
    Result_raw_Basalton = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\3. Basalton\Result Basalton complete.xlsx')

    Basalton_filtered = filterresults(Result_raw_Basalton, 1).reset_index(drop=True)
    Basalton_filtered['ECI Basalton flipped'] = Basalton_filtered['ECI'].sort_values(ascending=False).values
    # print(Basalton_filtered)

    # Merge the two dataframes
    Subset_LR = Loose_rock_filtered[['Waterlevel +mNAP', 'ECI']]
    Subset_Basalton = Basalton_filtered[['ECI Basalton flipped']]

    Transition_LR_BAS = pd.concat([Subset_LR, Subset_Basalton], axis=1)
    Transition_LR_BAS['Sum_ECI'] = Transition_LR_BAS['ECI'] + Transition_LR_BAS['ECI Basalton flipped']
    print(Transition_LR_BAS)

    plt.figure()
    x = np.arange(len(Transition_LR_BAS['Waterlevel +mNAP']))
    plt.plot(x, Transition_LR_BAS['ECI'], color='b', label='ECI Loose rock')
    plt.plot(x, Transition_LR_BAS['ECI Basalton flipped'], color='r', label='ECI Basalton')
    plt.plot(x, Transition_LR_BAS['Sum_ECI'], color='black', linestyle='--', label='Total ECI')
    plt.xticks(x, Transition_LR_BAS['Waterlevel +mNAP'])
    plt.xlabel('Waterlevel +mNAP')
    plt.ylabel('ECI (€)')
    plt.ylim(0, 300)
    plt.title(textwrap.fill('Transition height from Loose rock to Basalton', 50), loc='center')
    plt.legend(loc='upper left')
    plt.show()

columns_Loose_Rock = ['Waterlevel +mNAP', 'Significant wave height', 'Peak period', 'Storm duration',
                      'Density rock', 'Density water', 'Nominal diameter rock', 'Porosity',
                      'Damage number [S]', 'Uncertainty parameter C_pl', 'Uncertainty parameter C_s', 'Slope angle']

Data = []
for index, k in Hydraulic_BC.iloc[21:32, :].iterrows():
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
