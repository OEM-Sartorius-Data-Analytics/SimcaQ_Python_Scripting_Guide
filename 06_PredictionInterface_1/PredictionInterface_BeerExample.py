from win32com import client as win32
import argparse
import pandas as pd

def LoadInputCSVFile_v1(predictionDataFile):
    #pred_sample = pd.read_excel(predictionDataFile, index_col=0)
    pred_sample = pd.read_csv(predictionDataFile, index_col=0)
    #print(pred_sample.head())
    #pred_sample.to_csv("predictionDataFile.csv", index=False)
    #print('hola')
    #print(pred_sample.iloc[0,0:10])
    inputVariableNames = list(pred_sample.columns.values)
    inputData = pred_sample.iloc[0,:].to_list()

    return inputVariableNames, inputData

    

if __name__ == '__main__':

    # Retrieve the name of the SIMCA project and of the model name passed as
    # parameters when calling the python script
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--project", required=True, help="Path to the SIMCA project")
    ap.add_argument("-m", "--model", required=True, help="model name")
    ap.add_argument("-i", "--input", required=True, help="data file for prediction")
    args = vars(ap.parse_args()) 
    pathSimcaProject = args["project"] 
    modelName = args["model"]
    predictionDataFile = args["input"]
    
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
        oProject = simcaq.OpenProject(pathSimcaProject, "")
    except:
        print('Could not open the project.')
        raise SystemExit

    #Retrieve the number of models in the SIMCA project
    numberModels = oProject.GetNumberOfModels() 

    # Iterate over indices of all project models
    for iModelIndex in range(1, numberModels+1):

        # The index does not neccesarily coincide wit the model number
        # But we need the model number to retrieve information about the model
        modelNumber = oProject.GetModelNumberFromIndex(iModelIndex)

        # Once we know the model number, we can retrieve the Model Interface
        # for the specific model
        oModel = oProject.GetModel(modelNumber)

        # Retrieve the name of the model of interest
        oModelName = oModel.GetModelName()

        # Check if the model name coincides with that passed as an input
        # parameter to the script
        # If it coincides, we update the boolean variable modelFound
        # and then exit the iteration
        if oModelName == modelName:
            modelFound = True
            break

    # If the model name passed as an input parameter was not found
    # in the SIMCA project, we exit the script
    if modelFound == False:
        print('Could not find the specified model')
        raise SystemExit

    inputVariableNames, inputData = LoadInputCSVFile_v1(predictionDataFile)

    print(len(inputVariableNames))
    print(len(inputData))
    print(inputVariableNames)

    oPrepPred = oModel.PreparePrediction()

    variableVector = oPrepPred.GetVariablesForPrediction()
    variables_vec = [variableVector.GetVariable(i+1).GetName(1) for i in range(variableVector.GetSize())]
    NameLookup = {name: ix+1 for ix, name in enumerate(variables_vec)}

    for i, name in enumerate(inputVariableNames):
        if name in NameLookup:
            oPrepPred.SetQuantitativeData(1, NameLookup[name], inputData[i])

    oPrediction = oPrepPred.GetPrediction()

    resultData = oPrediction.GetYPredPS(1,True,True,None)

    predictionDataMatrix = resultData.GetDataMatrix()
    predictedY = predictionDataMatrix.GetData(1,1)




    # Dispose the project object
    oProject.DisposeProject()
