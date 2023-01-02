# The IModel Interface: Exploring Models

The *IModel* interface allows accesing multiple properties and parameters of the models included in SIMCA project/files.

Here we will show some of thes possibilities.

## Getting Started

We would start with a Python script like that from the [previous section](../04_ModelInterface_0/ModelInterface_Introduction.md). We will use the argparse module to pass as input parameters the names of the SIMCA project and of the model of interest. Then, we iterate over all models within the SIMCA project, and if a model with a name that coincides with that passed as an input parameter exists, we load that model into a *IModel* object:
```
from win32com import client as win32
import argparse
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':

    # Retrieve the name of the SIMCA project and of the model name passed as
    # parameters when calling the python script
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--project", required=True, help="Path to the SIMCA project")
    ap.add_argument("-m", "--model", required=True, help="model name")
    args = vars(ap.parse_args())
    pathSimcaProject = args["project"]
    modelName = args["model"]

    # Boolean variable to determine if the model has been found
    modelFound = False

    #Connect to the SIMCA-Q COM interface
    try:
        simcaq = win32.Dispatch('Umetrics.SIMCAQ')
    except:
        print('Could not connect to SIMCA-Q.')
        raise SystemExit

    # Open the SIMCA project
    try:
        project = simcaq.OpenProject(pathSimcaProject, "")
    except:
        print('Could not open the project.')
        raise SystemExit

    #Retrieve the number of models in the SIMCA project
    number_models = project.GetNumberOfModels() 

    # Iterate over indices of all project models
    for model_index in range(1, number_models+1):

        # The index does not neccesarily coincide wit the model number
        # But we need the model number to retrieve information about the model
        model_of_interest_number = project.GetModelNumberFromIndex(model_index)

        # Once we know the model number, we can retrieve the Model Interface
        # for the specific model
        model = project.GetModel(model_of_interest_number)

        # Retrieve the name of the model of interest
        model_of_interest_name = model.GetModelName()

        # Check if the model name coincides with that passed as an input
        # parameter to the script
        # If it coincides, we update the boolean variable modelFound
        # and then exit the iteration
        if model_of_interest_name == modelName:
            modelFound = True
            break

    # If the model name passed as an input parameter was not found
    # in the SIMCA project, we exit the script
    if modelFound == False:
        print('Could not fiund the specified model')
        raise SystemExit
```

## Summary of Fit Parameters

You can use the *IModel* interface to e.g., retrieve parameters that summarize the quality of the fit like R2(cum) and Q2(cum).

To obtain Q2(cum) values, start by invoking the *GetQ2Cum()* method:
```
q2cum = model.GetQ2Cum()
```

This returns an *IVectorData* object that we can use to retrieve the *cumulative Q2* of the different components of the model. We can actually get the names of each of these components. The first step would be to use the *GetRowNames()* method to retrieve a handle (an *IStringVector* object) to these names:
```
q2cum_ComponentNames = q2cum.GetRowNames()
```

We can then get the number of components by:
```
numberComponentsQ2Cum = q2cum_ComponentNames.GetSize()
```

and retrieve the actual component name by invoking the 'GetData()* method that takes as an input parameter the index of the desired component. For instance, in the example below a list is populated with the component names:
```
q2cum_ComponentNamesArray = []
for i in range(1,numberComponentsQ2Cum+1):
    q2cum_ComponentNamesArray.append(q2cum_ComponentNames.GetData(i))
```

Finally, we can get the actual *cumulative Q2* values first by invoking the *IVectorData* method *GetDataMatrix()*, which returns an *IFloatMatrix* object:
```
q2cum_DataMatrix = q2cum.GetDataMatrix()
```

This object allows then retrieving the actual *cumulative Q2* values for all components by invoking the *GetData()* method which takes as input parameters the indices of the component and of the parameter that we want to retrieve (always 1 as there is only one parameter: Q2(cum)). For instance, to retrieve all values within a list:
```
q2cum_DataArray = []
for iComp in range(1,numberComponentsQ2Cum+1):
    q2cum_DataArray.append(q2cum_DataMatrix.GetData(iComp,1))
```

We can use exactly the same approach to retrieve e.g. R2X(cum) labels and values:
```
# Retrieve IVectorData object to handle R2X(cum)
r2xcum = model.GetR2XCum()
# Retrieve IStringVector object to handle names of components used
# for calculating R2X(cum)
r2xcum_ComponentNames = r2xcum.GetRowNames()
# Retrieve number of components used for calculating R2X(cum)
numberComponentsR2XCum = r2xcum_ComponentNames.GetSize()
# Populate an array with the names of the components used for
# calculating R2X(cum)
r2xcum_ComponentNamesArray = []
for iComponent in range(1,numberComponentsR2XCum+1):
    r2xcum_ComponentNamesArray.append(r2xcum_ComponentNames.GetData(iComponent))
# Retrieve IFloatMatrix object to handle R2X(cum) values    
r2xcum_DataMatrix = r2xcum.GetDataMatrix()
# Populate an array with the values of R2X(cum) for each component    
r2xcum_DataArray = []
for iComp in range(1,numberComponentsR2XCum+1):
    r2xcum_DataArray.append(r2xcum_DataMatrix.GetData(iComp,1))

```

## Scores

We can now use the *IModel* method *GetT()* to retrieve the T matrix from the mode i.e., the score vector for each of the model dimensions. *GetT()* receives as input parameters an *IIntVector* object indicating the indices of the components to retrieve. However, if we pass *None* we retrieve all components:
```
scoresVectorData = model.GetT(None)
```

which is equivalent to:
```
numComponents = model.GetNumberOfComponents()

componentVector = simcaq.GetNewIntVector(numComponents)

for i in range(1,numComponents+1):
    componentVector.SetData(i,i)

scoresVectorData = model.GetT(componentVector)
```

The *GetT()* method returns a *IVectorData* object. From this object we can retrieve not only the score values, but also the names of the observations for which scores have been retrieved as well as the names of the model components that were retrieved.

To retrieve the observation names we first call the *IVectorData* method *GetRowNames()*, which returns an *IStringVector*:
```
observationNamesScoresVectorData = scoresVectorData.GetRowNames()
```

we can now retrieve the number of observations by:
```
numberObservationNamesScoresVectorData = observationNamesScoresVectorData.GetSize()
```

and e.g., retrieve and print to the console all observation names by:
```
for iObs in range(1,numberObservationNamesScoresVectorData+1):
    print(observationNamesScoresVectorData.GetData(iObs))
```

An analogous proccess can be used to retrieve the names of the components for which scores were retrieved, just note that in this case the *IVectorData* *GetColumnNames()* function must be used instead:
```
# IStringVector to retrieve the score labels
labelsScoresVectorData = scoresVectorData.GetColumnNames()
# Number of Scores
numberLabelsScoresVectorData = labelsScoresVectorData.GetSize()
# Retrieve and print the score labels
for iScore in range(1,numberLabelsScoresVectorData+1):
    print(labelsScoresVectorData.GetData(iScore))
```

To retrieve the actual score values from the *IVectorData* object *scoresVectorData* we need to call the *IVectorData* method *GetDataMatrix()* which will return an *IFloatMatrix* object:
```
scoresDatamatrix = scoresVectorData.GetDataMatrix()
```

From here we can use the *IFloatMatrix* method *GetData()*, which receives as inputs 1) the observation number and 2) the component number for which we want to retrieve the score value. For instance, to retrieve the score for the second component of the eight observation:
```
iObs = 8
iComponent = 1
scoreValue = scoresDatamatrix.GetData(iObs,iComponent)
```

We can finally plot the score matrix e.g., by using the pandas and matplotlib modules:
```
namesColumnsScoresVectorData = scoresVectorData.GetColumnNames()
namesRowsScoresVectorData = scoresVectorData.GetRowNames()

scoresDatamatrixNumberRows = scoresDatamatrix.GetNumberOfRows()
scoresDatamatrixNumberColumns = scoresDatamatrix.GetNumberOfCols()    

df = pd.DataFrame(columns=[
    namesColumnsScoresVectorData.GetData(1),
    namesColumnsScoresVectorData.GetData(2)
])

for col in range(scoresDatamatrixNumberColumns):
    for row in range(scoresDatamatrixNumberRows):
        df.at[
            namesRowsScoresVectorData.GetData(row+1),
            namesColumnsScoresVectorData.GetData(col+1)
        ] = scoresDatamatrix.GetData(row+1,col+1)

df.plot(kind = 'scatter',
        x = namesColumnsScoresVectorData.GetData(1),
        y = namesColumnsScoresVectorData.GetData(2)
        )

plt.show()
```