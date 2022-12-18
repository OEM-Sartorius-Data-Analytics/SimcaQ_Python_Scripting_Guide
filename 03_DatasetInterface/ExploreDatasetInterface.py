from win32com import client as win32
import argparse
import csv

if __name__ == '__main__':

    # Retrieve the name of the SIMCA project and of the dataset passed as parameters
    # when calling the python script
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--project", required=True, help="Path to the SIMCA project")
    ap.add_argument("-d", "--dataset", required=True, help="Dataset name")
    args = vars(ap.parse_args())
    pathSimcaProject = args["project"]
    datasetName = args["dataset"]

    #Connect to the SIMCA-Q COM interface
    try:
        simcaq = win32.Dispatch('Umetrics.SIMCAQ')
        #simcaq = win32.gencache.EnsureDispatch('Umetrics.SIMCAQ')
    except:
        print('Could not connect to SIMCA-Q.')
        raise SystemExit

    # Open the SIMCA project
    project = simcaq.OpenProject(pathSimcaProject, "") 

    #Retrieve the number of datasets in the SIMCA project
    number_datasets = project.GetNumberOfDatasets() 
        
    
    # Iterate over indices of all project datasets
    for dataset_index in range(1, number_datasets+1):

        # The index does not neccesarily coincide wit the dataset number
        # But we need the dataset number to retrieve information in the dataset
        dataset_of_interest_number = project.GetDatasetNumberFromIndex(dataset_index)            

        # Once we know the model number, we can retrieve the ModelInfo interface
        # for the specific model
        dataset = project.GetDataset(dataset_of_interest_number)            

        # Retrieve the name and type of the dataset of interest
        # from the Dataset object
        dataset_of_interest_name = dataset.GetDataSetName()

        # Leave the iteration if we have loaded a dataset with a name that
        # matches that passed to the main script as an input parameter i.e., datasetName
        if dataset_of_interest_name == datasetName:
            break

    # Number of observation IDs in the dataset
    n_observation_ids = dataset.GetNumberOfObservationIDs()

    # List that will contain te names for the observation IDs
    observation_ID_names = []

    # List of lists that will contain the value/string of the different
    # observation IDS for each observation
    observation_names = []
        
    # Populating observation_ID_names and observation_names
    for i in range(1,n_observation_ids+1):
        observation_ID_names.append(dataset.GetDataSetObservationIDName(i))

        temporal_list_observation_names = []

        obs_names = dataset.GetDataSetObservationNames(i)
        
        for observation_index in range(1,obs_names.GetSize()+1):
            temporal_list_observation_names.append(obs_names.GetData(observation_index))

        observation_names.append(temporal_list_observation_names)

    observations = dataset.GetDataSetObservations(None)

    observation_labels = []
    variable_labels = []
    
    for iObs in range(1,observations.GetColumnNames().GetSize()+1):
        observation_labels.append(observations.GetColumnNames().GetData(iObs))

    for iVar in range(1,observations.GetRowNames().GetSize()+1):
        variable_labels.append(observations.GetRowNames().GetData(iVar))

    dataset_values = []

    for iObs in range(1,observations.GetColumnNames().GetSize()+1):
        data_specific_observation = []
        for iVar in range(1,observations.GetRowNames().GetSize()+1):
            data_specific_observation.append(observations.GetDataMatrix().GetData(iVar,iObs))
        dataset_values.append(data_specific_observation)
    
    # Code for exporting the dataser in csv format to a file named dataset.csv
    # in the current working directory
    with open('dataset.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(observation_ID_names+variable_labels)
        for i in range(len(observation_labels)):
            row = []
            for j in range(len(observation_names)):
                row.append(observation_names[j][i])
            for k in range(len(variable_labels)):
                print(k)
                row.append(dataset_values[i][k])
            
            writer.writerow(row)
        
