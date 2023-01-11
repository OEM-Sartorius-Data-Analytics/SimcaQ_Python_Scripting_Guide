import argparse

def Dispatch(app_name:str):
    try:
        from win32com import client
        app = client.gencache.EnsureDispatch(app_name)
    except AttributeError:
        # Corner case dependencies.
        import os
        import re
        import sys
        import shutil
        # Remove cache and try again.
        MODULE_LIST = [m.__name__ for m in sys.modules.values()]
        for module in MODULE_LIST:
            if re.match(r'win32com\.gen_py\..+', module):
                del sys.modules[module]
        shutil.rmtree(os.path.join(os.environ.get('LOCALAPPDATA'), 'Temp', 'gen_py'))
        from win32com import client
        app = client.gencache.EnsureDispatch(app_name)
    return app

def CreateFakeLowarpData_v1(oModel):
    inputVariableNames = ['glas', 'crtp', 'mica', 'amtp']
    inputData = [40, 10, 10, 40]
    return inputVariableNames, inputData

if __name__ == '__main__':

    # Retrieve the name of the SIMCA project and of the model name passed as
    # parameters when calling the python script
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--project", required=True, help="Path to the SIMCA project")
    ap.add_argument("-m", "--model", required=True, help="model name")
    #ap.add_argument("-i", "--input", required=True, help="data file for prediction")
    args = vars(ap.parse_args()) 
    pathSimcaProject = args["project"] 
    modelName = args["model"]
    
    # Boolean variable to determine if the model has been found
    modelFound = False

    #Connect to the SIMCA-Q COM interface
    try:
        simcaq = Dispatch('Umetrics.SIMCAQ')
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

    
    oPrepPred = oModel.PreparePrediction()

    ############################################################
    ############## GET INPUT DATA FOR PREDICTION
    ############################################################

    inputVariableNames, inputData = CreateFakeLowarpData_v1(oModel)

    ############################################################
    ############## VARIABLE-POSITION DICTIONARY
    ############################################################    

    variableVector = oPrepPred.GetVariablesForPrediction()
    variables_vec = [variableVector.GetVariable(i+1).GetName(1) for i in range(variableVector.GetSize())]
    NameLookup = {name: ix+1 for ix, name in enumerate(variables_vec)}

    ############################################################
    ############## POPULATING PREPARE PREDICTION WITH DATA
    ############################################################

    for i, name in enumerate(inputVariableNames):
        if name in NameLookup:
            oPrepPred.SetQuantitativeData(1, NameLookup[name], inputData[i])

    ############################################################
    ############## GET THE PREDICTION
    ############################################################

    oPrediction = oPrepPred.GetPrediction()

    ############################################################
    ############## PREDICTING Y VALUES
    ############################################################

    numPredictiveScores = oModel.GetNumberOfPredictiveComponents()

    hPredictedY = oPrediction.GetYPredPS(numPredictiveScores,True,True,None)

    numYVariables = oModel.GetColumnYSize()

    predictionDataMatrix = hPredictedY.GetDataMatrix()
    iObs = 1
    #iVarY = 1
    for iVarY in range(1, numYVariables+1):
        predictedY = predictionDataMatrix.GetData(iObs,iVarY)
        print('predicted y: ', predictedY)

    # Dispose the project object
    oProject.DisposeProject()
        
    
