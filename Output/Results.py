# This is where all results of the calculations from the ECI and revetment types are merged and one table is formed to be able to rank the designs.

import numpy as np
import openturns as ot
import pandas as pd
import matplotlib.pyplot as plt
from Input.Parameters import Parameters

ot.Log.Show(ot.Log.NONE)


class ResultTable:

    # Analysis of Loose Rock

    Result_Raw = pd.read_excel(r'C:\Users\vandonsk5051\Documents\Afstuderen (Schijf)\Python scripts\GitHub Revetment tool\Dike-revetment-tool-\LooseRock_S1600_9_8_Table(1.6-1.8mNAP).xlsx')
    # print(Result_Raw)

    Req_pf = 0.9

    Result_filtered = Result_Raw[Result_Raw['Probability of failure'] > Req_pf]
    print(Result_filtered)

    plt.scatter(Result_filtered['ECI'], Result_filtered['Probability of failure'])
    plt.xlabel('Nominal diameter rock')
    plt.ylabel('Probability of failure')
    plt.title('TEST')
    ymin = 0
    ymax = 1
    plt.ylim(ymin, ymax)
    plt.show()
