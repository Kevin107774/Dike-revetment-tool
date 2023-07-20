import openturns as ot
from matplotlib import pylab as plt

# We define a generalized extreme value distribution with parameters \mu = 1.3, \sigma = 1.0 and \xi = 0.05 for the
# water level
distWaterlevel = ot.GeneralizedExtremeValue(1.3, 1.0, 0.005)

# We define a normal distribution with parameters \mu = 1.3, \sigma = 1.0 for the height of the dike
distDikeheight = ot.Normal(3.5, 0.05)

# Combine all distributions into a single one
distX = ot.ComposedDistribution([distWaterlevel, distDikeheight])

print(distX)
# Define the failure model, in this case overflow when the water level exceeds the dike height:
def FailureModel(vector):
    """
    :param vector: vector with [Waterlevel, DikeHeight]
    :return Z: limitstate Z
    """
    Waterlevel = vector[0]
    DikeHeight = vector[1]

    # Limit state function:
    Z = [DikeHeight - Waterlevel]
    return Z
ot_failure_model = ot.PythonFunction(2, 1, FailureModel)

# Define the event:
vect = ot.RandomVector(distX)  # vector of samples to be drawn from distributions
Z = ot.CompositeRandomVector(ot_failure_model, vect) #  New distribution generated from the other distributions processed by the model
event = ot.ThresholdEvent(Z, ot.Less(), 0.0)  # overflow failure when Z<0
event.setName("overflow")

# Using FORM, define a solver:
optimAlgo = ot.Cobyla()
optimAlgo.setMaximumEvaluationNumber(100000)
optimAlgo.setMaximumAbsoluteError(1.0e-10)
optimAlgo.setMaximumRelativeError(1.0e-10)
optimAlgo.setMaximumResidualError(1.0e-10)
optimAlgo.setMaximumConstraintError(1.0e-10)

# Run FORM
startingPoint = [3.5, 3.5]
algo = ot.FORM(optimAlgo, event, startingPoint)
algo.run()
result = algo.getResult()
standardSpaceDesignPoint = result.getStandardSpaceDesignPoint()

# Retrieve results
result = algo.getResult()
probability = result.getEventProbability()
beta = result.getHasoferReliabilityIndex()
print(f"Pf={probability}, beta = {beta}")

# get importance factors
importance_factors = result.getImportanceFactors()
labels = ['Water level', 'Dike height']

fig, ax = plt.subplots()
ax.pie(importance_factors, labels=labels)
plt.show()