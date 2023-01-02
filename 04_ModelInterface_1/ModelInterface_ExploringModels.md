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