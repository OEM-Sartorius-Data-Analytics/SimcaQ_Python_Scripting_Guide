# The Dataset Interface

The *Dataset* interface can be accessed from *Project* objects and it provides access to the datasets within the SIMCA project/file.

THe *Dataset* interfaces can be accessed through the *Project* method *GetDataset()*. This method needs as a parameter the number of the dataset of interest within the SIMCA project. It is not straightforward to know this number. However, one can get it from the model index. All datasets withon a SIMCA project/file are associated within indices starting from 1 and up to the total number of datasets that can be retrieved from the *Project* method *GetNumberOfDatasets()*. Provided that we know (or find out) the index of the dataset of interest, we can get the associated dataset number by calling the Project method *GetDatasetNumberFromIndex(dataset_index)* that receives as a parameter the dataset index. Once we know the desired dataset number, we can create the *Dataset* object by running the Project method *GetDataset(dataset_of_interest_number)* that receives as a parameter the dataset number.


![train dataset](Dataset_Images/DatasetTrainset.png)