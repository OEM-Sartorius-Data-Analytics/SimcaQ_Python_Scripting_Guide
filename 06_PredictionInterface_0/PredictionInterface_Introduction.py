from win32com import client as win32
import argparse

if __name__ == '__main__':

    # Retrieve the name of the SIMCA project passed as a parameter
    # when calling the python script
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--project", required=True, help="Path to the SIMCA project")
    args = vars(ap.parse_args())
    PathSimcaProject = args["project"]
    
    #Connect to the SIMCA-Q COM interface
    try:
        simcaq = win32.Dispatch('Umetrics.SIMCAQ')
    except:
        print('Could not connect to SIMCA-Q.')
        raise SystemExit

    # Open the SIMCA project
    try:
        project = simcaq.OpenProject(PathSimcaProject, "")
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

        # Retrieve the name and type of the model of interest
        # from the ModelInfo object
        model_of_interest_name = oModel.GetModelName()
        model_of_interest_type_name = oModel.GetModelTypeString()

        # and print the putput
        print(f'For the model with index {model_index} and number {model_of_interest_number}:')
        print(f'Name: {model_of_interest_name}')
        print(f'Type: {model_of_interest_type_name}')

    oPrepPred = oModel.PreparePrediction()

    print(oPrepPred.GetVariablesForPrediction())

    print(oPrepPred.GetVariablesForPrediction().GetVariable(1))

    predictionVariables = oPrepPred.GetVariablesForPrediction()
    numberPredictionVariables = predictionVariables.GetSize()

    indexVariableOfInterest = 1;
    variableOfInterestForPrediction = predictionVariables.GetVariable(indexVariableOfInterest)
    nameVariableOfInterestForPrediction = variableOfInterestForPrediction.GetName(1)

    print(nameVariableOfInterestForPrediction)
    

    # Dispose the project object
    project.DisposeProject()
        
    
