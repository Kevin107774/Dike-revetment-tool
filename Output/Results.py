# This is where all results of the calculations from the ECI and revetment types are merged and one table is formed to be able to rank the designs.

import numpy as np
import openturns as ot
import pandas as pd
from Input.Parameters import Parameters
from Revetment_types import Loose_Rock3
ot.Log.Show(ot.Log.NONE)


class ResultTable:

    # Poisson's distribution for probability of failure lifetime
        # lifetime = 50
        # probabilty_lft = 1 - (1 - probability)**lifetime
