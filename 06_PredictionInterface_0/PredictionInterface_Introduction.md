# Perform Predictions: The IPreparePrediction and IPrediction Interfaces

In SIMCA-Q, predictions can be inferred by combining the *IPreparePrediction* and the *IPrediction* interfaces. The first step is to use the *IModel* interface to generate a *IPreparePrediction* prediction object. *PreparePrediction* objects are then 1) populated with the data from where quantities will be predicted and 2) subsequently used to create a *IPrediction* object. *IPrediction* objects can then be used to obtain the desired predicted quantities.

## IPreparePrediction Interface

Let's say that we have a *IModel* object named *oModel*. We can use it to create a *IPreparePrediction* object, let's name it oPrepPred, by using the *IModel* method *PreparePrediction()*:
```
oPrepPred = oModel.PreparePrediction()
```

*IPreparePrediction* offers the method *GetVariablesForPrediction()*, which returns a *IVariableVector* object that we can subsequently use to obtain the number of variables needed for doing the prediction, by using the *GetSize()* method, as well as the name of these variables, by using the *GetVariable()* method (which recveives as an input parameter the index of the variable of interest. Specifically, *GetVariable()* will return a *IVariable* object that can provide the variable name by invoking the *GetName()* method:
```
predictionVariables = oPrepPred.GetVariablesForPrediction()
numberPredictionVariables = predictionVariables.GetSize()

indexVariableOfInterest = 1;
variableOfInterestForPrediction = predictionVariables.GetVariable(indexVariableOfInterest)
nameVariableOfInterestForPrediction = variableOfInterestForPrediction.GetName(1)
```

These methods can be extremly important when preparing a prediction as we will see below.

The next step would be to populate the *IPreparePrediction* object with the input data from where predictions will be made. For this, *IPreparePrediction* offers a variety of methods. Here, we will focus on *SetQuantitativeData()* that, unsurprisingly, is used when the input data is of qualitative nature. *SetQuantitativeData()* receives as input parameters two integers, the first one accounting for the observation number (several observations can be used for prediction simultaneously) and the second one accounting for the variable number.

In the simple case where all variables are used for prediction, and where the input data is in the shape of e.g., a 2D python list, let's name it *inputData* , we could populate the *IPreparePrediction* object by:

```
for iVar in range(1,numberOfVariables):
    for iObs in range(1,numberOfObservations):
        oPrepPred.SetQuantitativeData(iObs, iVar, inputData[obs][var])
```

However, in many cases this will be a buggy approach. For prediction, SIMCA-Q requires only the data of the variables used for building the model, but it _requires that they are provided in the correct order_. And the order is that of the dataset used to build the model. It is not uncommon that datasets include Y variables before the X variables, and even that not all X variables are used to build the model. Even if this is not explicit, it can happen e.g., when the derivates of the data are used instead of the original data. While SIMCA-Q will automatically apply the same preprocessing to the data that was used to build the model, derivating leaves out of the model building the first and last variables.

If you know in advance the structure of your dataset, you can hardcode the script in order to place the input data in the correct positions. Just adjust the iVar variable in the above code accordingly. Actually, this would be the only option if you data file i.e., the file containing the data used for prediction, does not include the names of the variables these data corresponds to, or if these names do not coincide with those of the dataset used to build the model.

However, we propose here a workaround if your input file contains the variable names, and they coincide with those used by the dataset used to build the model. Basically, you can create a dictionary with the names of the variables used to build the models as keys, and the position of these variables in the *IVariableVector* object returned by the *IPreparePrediction* method *GetVariablesForPrediction()* as values. Once this dictionary is created, we can iterate over the data lists for prediction, and only provided SIMCA-Q with the variables whose names coincide with those used to build the specific model, and also in the correct order. For instance, if you process your file for prediction so that you have a list with the names of the variables of the data within that file, let's name it *variable_names*, and a 2D list encapsulating the actual data, let's name it *prediction_data*, you could populate the *IPreparePrediction* object as follows:
```
variableVector = prepPred.GetVariablesForPrediction()
variables_vec = [variableVector.GetVariable(i+1).GetName(1) for i in range(variableVector.GetSize())]
NameLookup = {name: ix+1 for ix, name in enumerate(variables_vec)}

for i, name in enumerate(test_variable_names):
    if name in NameLookup:
        for iObs in range(1,numberOfObservations):
            oPrepPred.SetQuantitativeData(iObs, NameLookup[name], prediction_data[iObs][i])
```

## IPrediction Interface

Once we have feed SIMCA-Q with the correct data and in the correct order, we can access the *IPrediction* interface, that will allow us to handle predicted data:
```
oPrediction = oPrepPred.GetPrediction()
```

Once this object is created, we can inmediately access all predicted quantities.

For instance, to retrieve the predicted scores we can use the *GetTPS()* method. This method receives as input parameters either *None*, if we want to retrieve the predicted scores for all the components of the model, or a *IntVector* object listing the desired components. For instance, to predict scores in all components:
```
oPrediction.GetTPS(None)
```

but to retrieve only the score for e.g., the first component:
```
# Create a prediction vector according to SIMCA-Q requirements
# for retrieving prediction parameters afterwards
predictionVector = simcaq.GetNewIntVector(1)
predictionVector.SetData(1, 1)

# Retrieve the score
predictedScores = oPrediction.GetTPS(predictionVector)
```

In this example, *predictedScores* is a *VectorData* object. To retrieve the actual data we need first to retrieve a *FloatMatrix* object to handle this data:
```
predictedScoresDataMatrix = predictedScores.GetDataMatrix()
```

We can access the number of rows/observations of this data matrix by invoking the *GetNumberOfRows()* method and the number of columns/scores by invoking the *GetNumberOfColumns()* method. But, most improtantly, we can access the actual score values by invoking the *GetData()* method, which receives as input parameters the indices for observation and component of the scores that we want to retrieve. For instance, to retrieve the score for observation #1 and component #2:
```
iObs = 1
iComp = 2
value = predictedScoresDataMatrix.GetData(iObs, iComp)
```

We can follow a similar process to ontain other predicted quantities.

For instance, to retrieve predicted DModX and DModX+ values we would use the *GetDModXPS()* and *GetDModXPSCombined()* methods respectively. These tow methods receive as input parameters 1) None if all components shopuld be used or a *IntVector* object listing the desired components (see above), 2) a boolean parameter indicating whether the results will be in units of standard deviation of the pooled RSD of the model (or absolute values in case of *False*), 3) a boolean parameter indicating whether the function will weight the residuals by the modeling power of the variables. Both of these functions will return *VectorData* objects, and the process to get the actual DModX and DModX+ would be similar to that detailed above for the predicted scores. For instance:
```
predictedGetDModX = oPrediction.GetDModXPS(None, True, True)
predictedGetDModXPlus = oPrediction.GetDModXPSCombined(None, True, True)

predictedGetDModXDataMatrix = predictedGetDModX.GetDataMatrix()
predictedGetDModXPlusDataMatrix = predictedGetDModX.GetDataMatrix()

iObs = 1
iComp = 2
valueDModX = predictedGetDModXDataMatrix.GetData(iObs, iComp)
valueDModXPlus = predictedGetDModXPlusDataMatrix.GetData(iObs, iComp)
```

In the same way we could access the predicted Y values inn PLS or OPLS models:
```
numPredictiveScores = model.GetNumberOfPredictiveComponents()

# Create a prediction vector according to SIMCA-Q requirements
# for retrieving prediction parameters afterwards
predictionVector = simcaq.GetNewIntVector(1)
predictionVector.SetData(1, 1)

# Retrieve and print predicted y
resultData = prediction.GetYPredPS(numPredictiveScores,True,True,predictionVector)
predictionDataMatrix = resultData.GetDataMatrix()
predictedY = predictionDataMatrix.GetData(1,1)
```

