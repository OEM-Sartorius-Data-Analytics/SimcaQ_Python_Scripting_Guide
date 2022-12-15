# The ModelInfo Interface

The Project interface allows calling the ModelInfo interface for specific models.

The ModelInfo interface allows to retrieve information about the model of interest without actually loading the model.

A *ModelInfo* object can be created from a *Project* object by calling the *GetModelInfo()* method. This method needs as a parameter the number of the model of interest within the SIMCA project. It is not straightforward to know this number. However, one can get it from the model index. All models withon a SIMCA project/file are associated within indices starting from 1 in the same order as they appear in the SIMCA project/file. Provided that we know the index of the model of interest, we can get the associated model number by calling the *Project* method *GetModelNumberFromIndex(model_index)* that receives as a parameter the model index. Once we know the desired model number, we can create the *ModelInfo* object by running the *Project* method *GetModelInfo(model_of_interest_number)* that receives as a parameter the model number.

The created *ModelInfo* object has several methods that retrieve information about the model. This is shown in the example below. In the script we iterate over indices for all models in the SIMCA project. For eac index, we get the associated model number and create a *ModelInfo* object. And for each of these objects we find and print the name and type with calling the *ModelInfo* methods *GetModelName()* and *GetModelTypeName()*.

```
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

        #Retrieve the number of models in the SIMCA project
        number_models = project.GetNumberOfModels()
    
        # Iterate over indices of all project models
        for model_index in range(1, number_models+1):

            # The index does not neccesarily coincide wit the model number
            # But we need the model number to retrieve information about the model
            model_of_interest_number = project.GetModelNumberFromIndex(model_index)

            # Once we know the model number, we can retrieve the ModelInfo interface
            # for the specific model
            model_info = project.GetModelInfo(model_of_interest_number)

            # Retrieve the name and type of the model of interest
            # from the ModelInfo object
            model_of_interest_name = model_info.GetModelName()
            model_of_interest_type_name = model_info.GetModelTypeName()

            # and print the putput
            print(f'For the model with index {model_index} and number {model_of_interest_number}:')
            print(f'Name: {model_of_interest_name}')
            print(f'Type: {model_of_interest_type_name}')

        # Dispose the project object
        project.DisposeProject()
        
    except:
        print('Could not open the project.')
        raise SystemExit
```