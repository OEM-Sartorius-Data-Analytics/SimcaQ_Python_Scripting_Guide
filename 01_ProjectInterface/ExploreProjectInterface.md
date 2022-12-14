# The Project Interface

The SIMCAQ interface does not only provide access to some methods but also to other interfaces. One is the Project interface. The Project interface allows accessing SIMCA projects i.e., usp files, and retrieve all information they contain. Project objects are creted by using the SIMCAQ method OpenProject, which takes two input parameters. These are strings accounting for i) the full path to the SIMCA project file and ii) the corresponding password in case the usp file is encrypted.

A simple use of the Project interface is illustrated by the example below:

```
from win32com import client as win32
import argparse

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--project", required=True, help="Path to the SIMCA project")
    args = vars(ap.parse_args())

    PathSimcaProject = args["project"]
    
    try:
        simcaq = win32.Dispatch('Umetrics.SIMCAQ')

        try:
            project = simcaq.OpenProject(PathSimcaProject, "")
            print("You have loaded the project ", project.GetProjectName())
            print("which has ", project.GetNumberOfModels(), " models.")
            print("and ", project.GetNumberOfDatasets(), " datasets")
	    project.DisposeProject()

        except:
            print('Could not open project.')

    except:
        print('Could connect to SIMCA-Q.')
```

The python script takes as an argument the path to a SIMCA project. FOr this, the *argparse* is used. Then, A SIMCA-Q COM object is created with the help of the pywin32 extension and used to open the project. FInally we used and printed the output of two methods of the Project interface:

- *GetProjectName()*: Retrieves the name of the project. 
- *GetNumberOfModels()*: Retrieves the number of models in the project, including unfitted models.
- *GetNumberOfDatasets()*: Retrieves the number of data sets in the project.

Finally, we used the Project method *DisposeProject()* to dispose of the Project object.
