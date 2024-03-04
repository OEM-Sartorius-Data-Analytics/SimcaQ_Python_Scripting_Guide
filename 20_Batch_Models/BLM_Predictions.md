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
have a different value for each maturity value of the model.




