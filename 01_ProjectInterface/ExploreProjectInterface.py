from win32com import client as win32
import argparse

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--project", required=True, help="Path to the Simca project")
    args = vars(ap.parse_args())

    PathSimcaProject = args["project"]
    
    simcaq = win32.Dispatch('Umetrics.SIMCAQ')

    project = simcaq.OpenProject(PathSimcaProject, "")

    print("You have loaded the project ", project.GetProjectName(), ", which has ", project.GetNumberOfModels(), " models.")

    project.DisposeProject()


