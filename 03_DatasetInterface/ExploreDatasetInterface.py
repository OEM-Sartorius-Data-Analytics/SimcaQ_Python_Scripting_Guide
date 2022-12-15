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
        

        #Retrieve the number of datasets in the SIMCA project
        number_datasets = project.GetNumberOfDatasets()
        
    
        # Iterate over indices of all project models
        for dataset_index in range(1, number_datasets+1):

            # The index does not neccesarily coincide wit the model number
            # But we need the model number to retrieve information about the model
            dataset_of_interest_number = project.GetDatasetNumberFromIndex(dataset_index)
            

            # Once we know the model number, we can retrieve the ModelInfo interface
            # for the specific model
            dataset = project.GetDataset(dataset_of_interest_number)
            

            # Retrieve the name and type of the dataset of interest
            # from the Dataset object
            dataset_of_interest_name = dataset.GetDataSetName()
            

            # and print the putput
            print(f'For the dataset with index {dataset_index} and number {dataset_of_interest_number}:')
            print(f'Name: {dataset_of_interest_name}')

        # Dispose the project object
        project.DisposeProject()
        
    except:
        print('Could not open the project.')
        raise SystemExit        
