# ELEMENTS (Basalton)
# Retrieve results from elements, Basalton

Parameter_combinations_Basalton = Parameters.parameter_combinations_Basalton
Number_samples = BasaltonFunc.nr_samples
Probability_failure_Basalton = BasaltonFunc.Pf_Basalton

# Add the Pf as a column to the dataframe
Parameter_combinations_Basalton['Probability of failure Basalton'] = Probability_failure_Basalton
Parameter_combinations_Basalton['Number of samples'] = Number_samples

# Add the Pf for the design lifetime to the dataframe
Parameter_combinations_Basalton['Pf Basalton 50 year'] = pflifetime(
    Parameter_combinations_Basalton['Probability of failure Basalton'])

# Add ECI as column to the dataframe
Parameter_combinations_Basalton['ECI'] = Parameter_combinations_Basalton.apply(lambda row: ECIFunc.ECIBasalton(row['Layer thickness Basalton'], row['Waterlevel +mNAP'], row['Slope angle']), axis=1)

print(Parameter_combinations_Basalton)
Parameter_combinations_Basalton.to_excel("Test Basalton 1.xlsx")