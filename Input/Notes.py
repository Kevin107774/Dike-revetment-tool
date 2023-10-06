# Transition Loose rock to Basalton
## Verkalit
    Result_raw_Verkalit = pd.read_excel(
        r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\2. Verkalit\Result Verkalit complete.xlsx')
    Result_raw_Verkalit['ECI_slopelength'] = ECIFunc.ECIVerkalit(Result_raw_Verkalit['Layer thickness Verkalit'], 2.41,
                                                                 Result_raw_Verkalit['Slope angle'])
    # print(Result_raw_Verkalit)
    # Result_raw_Verkalit.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\2. Verkalit\Raw for original design Verkalit.xlsx')

    Verkalit_selection = Result_raw_Verkalit[Result_raw_Verkalit['Probability of failure'] < 1 / 60000]
    Verkalit_selection = Verkalit_selection[Verkalit_selection['Waterlevel +mNAP'] == 2.4]
    # Verkalit_selection = Verkalit_selection[Verkalit_selection['Waterlevel +mNAP'] < 2.6]
    Verkalit_selection = Verkalit_selection.sort_values(
        ['Layer thickness Verkalit', 'ECI_slopelength'], ascending=[True, True])

    Verkalit_selection = Verkalit_selection.groupby('Layer thickness Verkalit').head(1)
    # new_row = pd.DataFrame([[0] * len(Verkalit_selection.columns)], columns=Verkalit_selection.columns)
    # Verkalit_selection = pd.concat([new_row, Verkalit_selection], ignore_index=True)
    print(Verkalit_selection)
    # Verkalit_selection.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\2. Verkalit\Selection original design Verkalit2.xlsx')

    figure = plt.figure()
    x = np.arange(len(Basalton_selection['Layer thickness Basalton']))
    plt.bar(x-0.1, Basalton_selection['ECI_slopelength'], color='lightsalmon', width=0.2, label='Basalton')
    plt.bar(x+0.1, Verkalit_selection['ECI_slopelength'], color='peachpuff', width=0.2, label='Verkalit')
    plt.xticks(x, Basalton_selection['Layer thickness Basalton'])
    plt.xlabel('Element thickness placed revetment (m)')
    plt.ylabel('ECI (€)')
    plt.ylim(0, 100)
    plt.title(textwrap.fill('ECI per element thickness Basalton and Verkalit', 50),
              loc='center')
    plt.legend(loc='upper left')

    # Add y-values to the bars
    for i, v in enumerate(Basalton_selection['ECI_slopelength']):
        if v != 0:
            plt.text(i - 0.2, v + 1, f'ECI: {v:.1f}\nρ: {Basalton_selection["Density concrete"].iloc[i]}',
                     color='lightsalmon', ha='center')

    for i, v in enumerate(Verkalit_selection['ECI_slopelength']):
        if v != 0:
            plt.text(i + 0.2, v + 1, f'ECI: {v:.1f}\nρ: {Verkalit_selection["Density concrete"].iloc[i]}',
                     color='peachpuff', ha='center')
    # plt.show()

    Verkalit_filtered = filterresults(Result_raw_Verkalit, 5)
    # print(Verkalit_filtered)
    # Verkalit_filtered.to_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\Results\2. Verkalit\Filtered result table Verkalit.xlsx')

    # Select the water levels in the original design
    Verkalit_original_design = Verkalit_filtered.loc[Verkalit_filtered['Layer thickness Verkalit'].idxmax()]
    Verkalit_original_design = pd.DataFrame([Verkalit_original_design])
    # print(Verkalit_original_design)
    # Verkalit_original_design.to_excel('the highest value.xlsx')
