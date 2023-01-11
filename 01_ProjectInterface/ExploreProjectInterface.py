import argparse

def dispatch(app_name:str):
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

if __name__ == '__main__':

    # Retrieve the name of the SIMCA project passed as a parameter
    # when calling the python script
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--project", required=True, help="Path to the SIMCA project")
    args = vars(ap.parse_args())
    pathSimcaProject = args["project"]
    
    #Connect to the SIMCA-Q COM interface
    try:
        simcaq = dispatch('Umetrics.SIMCAQ')
    except:
        print('Could not connect to SIMCA-Q.')
        raise SystemExit

    # Open the SIMCA project
    try:
        project = simcaq.OpenProject(pathSimcaProject, "")
    except:
        print('Could not open the project.')
        raise SystemExit        

    #Retrieve information about the SIMCA project
    projectName = project.GetProjectName() 
    numberModels = project.GetNumberOfModels()
    numberDatasets = project.GetNumberOfDatasets()
    
    # Print the output of the used Project interface methods
    print(f'You have loaded the project {projectName},')
    print(f'which has {numberModels} models')
    print(f'and {numberDatasets} datasets')

    # Dispose the project object
    project.DisposeProject()
