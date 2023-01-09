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
    inputData = pred_sample.iloc[1,5:].to_list()

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
        oModel = project.GetModel(model_of_interest_number)

        # Retrieve the name of the model of interest
        model_of_interest_name = oModel.GetModelName()

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

    inputVariableNames, inputData = LoadInputCSVFile_v1(predictionDataFile)



    # Dispose the project object
    project.DisposeProject()
