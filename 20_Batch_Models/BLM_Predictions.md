# Making Predictions with Batch Level Models

Let's say that we have alreaya Batch Level Model, ie a IBatchLevelModel object, previously loaded into the variable BLModel. 
The process to make predictions using this model starts from this object.
Specifically, it allows to create an IPrepareBatchPrediction object by means of the GetPrepareBatchPrediction() method. We can obtain
the corresponding IPrepareBatchPrediction object by:
```
PrepareBatchPrediction = BLModel.GetPrepareBatchPrediction()
```

Note that for this to work BLModel needs to be fitted.

An IPrepareBatchPrediction object can already tell us the variables required to make predictions. For each phase (Batch Evolution Model)
of the parent Batch Model we can obtain the name of these variables eg by:
```
def simcaq_variable_vector_to_list(simcaq_variable_vector):
    variable_vector_list = []
    for i in range(1, simcaq_variable_vector.GetSize()+1):
        variable_vector_list.append(simcaq_variable_vector.GetVariable(i).GetName(1))
    return variable_vector_list

for iPhase in range(1,bModel.GetNumberOfBEM()+1):
    VariablesForBatchPrediction = PrepareBatchPrediction.GetVariablesForBatchPrediction(iPhase)
    VariablesForBatchPredictionList = simcaq_variable_vector_to_list(VariablesForBatchPrediction)
    print(VariablesForBatchPredictionList)
```

One can then feed into the IPrepareBatchPrediction object the data required to make a prediction.
At this point one needs to be careful, as each of the variables retrieved by GetVariablesForBatchPrediction(iPhase) will 
have a different value for each maturity value of the model. Actually, maturity will most probably be one of the variables 
retrieved by GetVariablesForBatchPrediction(iPhase).

For making predictions with Batch Level Models we will need to provide values for process parameters measured at maturity values 
at least close to the maturity values used when building the model. These maturity values ie the ones for which the corresponding Barch Evolution model was built,
can be retrieved by many different ways. One is to retrieve the names for the rows of the matrix retrieve by methods of the 
corresponding Batch Evolution Model such as GetYPred() and GetAlignedYPred().

The IPrepareBatchPrediction offers several methods to load data to make predictions with the corresponding Batch Level Model. 
One is SetQuantitativeBatchData(iPhase, iObs, iVar, value). Here iPhase corresponds to the number of the underlying Batch 
Evolution Model. iObs to the _observation_ index. Note that here this index is actually the index of the _maturity stamp_. For instance,
if during the process variables were measured at x maturity values, iObs could be provided up to a value of x. Note that most probably
you will need at least two maturity stamps ie, process parameter values for at least two maturity stamps, to be able to make a prediction.





