# The Project Interface

The SIMCAQ interface does not only provide access to some methods but also to other interfaces. One is the Project interface. The Project interface allows accessing SIMCA projects i.e., usp files, and retrieve all information they contain. Project objects are creted by using the SIMCAQ method OpenProject, which takes two input parameters. These are strings accounting for i) the full path to the SIMCA project file and ii) the corresponding password in case the usp file is encrypted.

A simple use of the Project interface is illustrated by the example below:

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
    except:
        print('Could not open the project.')
        raise SystemExit
        

    #Retrieve information about the SIMCA project
    project_name = project.GetProjectName() 
    number_models = project.GetNumberOfModels()
    number_datasets = project.GetNumberOfDatasets()
    
    # Print the output of the used Project interface methods
    print(f'You have loaded the project {project_name},')
    print(f'which has {number_models} models')
    print(f'and {number_datasets} datasets')

    # Dispose the project object
    project.DisposeProject()
```

The python script takes as an argument the path to a SIMCA project. FOr this, the *argparse* is used. Then, A SIMCA-Q COM object is created with the help of the pywin32 extension and used to open the project. FInally we used and printed the output of two methods of the Project interface:

- *GetProjectName()*: Retrieves the name of the project. 
- *GetNumberOfModels()*: Retrieves the number of models in the project, including unfitted models.
- *GetNumberOfDatasets()*: Retrieves the number of data sets in the project.

Finally, we used the Project method *DisposeProject()* to dispose of the Project object.
