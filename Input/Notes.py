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
