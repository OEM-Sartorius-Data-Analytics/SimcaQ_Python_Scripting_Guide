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
            project.DisposeProject()

        except:
            print('Could not open project.')

    except:
        print('Could connect to SIMCA-Q.')
            

    


