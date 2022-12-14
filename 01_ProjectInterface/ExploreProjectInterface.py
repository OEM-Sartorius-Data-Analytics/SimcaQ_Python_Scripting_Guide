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
