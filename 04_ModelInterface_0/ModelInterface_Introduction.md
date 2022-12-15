# The Model Interface: Introduction

We can use a *Project* object to access the *Model* Interface. In this way we can create a Model object that we can use to access several properties of the Model as well as other interfaces needed e.g., for doing predictions.

For creating a *Model* object from a *Project* object we can use the *GetModel()* method. In the same way as for the *ModelInfo* interface, we need to pass as a parameter to the *GetModel()* method the number of the desired model within the SIMCA project/file. But to know the specific model number m,ight not be straigtforward. However, we can get the model number from the model index. All models withon a SIMCA project/file are associated within indices starting from 1 in the same order as they appear in the SIMCA project/file. Provided that we know the index of the model of interest, we can get the associated model number by calling the *Project* method *GetModelNumberFromIndex(model_index)* that receives as a parameter the model index. Once we know the desired model number, we can create the *Model* object by running the *Project* method *GetModel(model_of_interest_number)* that receives as a parameter the model number.

We show below an example script, similar to the one used to illustrate the use of the *ModelInfo* interface, where we iterate over indices for all models in the SIMCA project. For eac index, we get the associated model number and create a *Model* object. And for each of these objects we find and print the name and type with calling the *Model* methods *GetModelName()* and *GetModelTypeString()*.

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

            # Once we know the model number, we can retrieve the Model Interface
            # for the specific model
            model = project.GetModel(model_of_interest_number)

            # Retrieve the name and type of the model of interest
            # from the ModelInfo object
            model_of_interest_name = model.GetModelName()
            model_of_interest_type_name = model.GetModelTypeString()

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