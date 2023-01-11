# SIMCA-Q Python Scripting Guide

This guide focuses through examples on how to use Python to develop SIMCA-Q applications.

At present, Python only can interact with the SIMCA-Q COM interface. Therefore, these apps will only work on Windows systems.

This repo also contains a *requirements.txt* that list all packages used in the examples. To install them, ideally within a virtual environment, run:
```
python -m pip install -r requirements.txt
```

## Index

- [Access the COM interface of SIMCA-Q & write a first script to check your SIMCA-Q license](00_COM_and_License/COM_and_License.md).
- [The IProject Interface](01_ProjectInterface/ExploreProjectInterface.md).
- [The IModelInfo Interface](02_ModelInfoInterface_0/ExploreModelInfoInterface.md).
- [The IDataset Interface: accessing datasets in SIMCA projects](03_DatasetInterface/ExploreDatasetInterface.md).
- [The IModel Interface: Introduction](04_ModelInterface_0/ModelInterface_Introduction.md).
- [The IModel Interface: Exploring Models](04_ModelInterface_1/ModelInterface_ExploringModels.md).
- [Making Predictions: The IPreparePrediction and IPrediction Interfaces](06_PredictionInterface_0/PredictionInterface_Introduction.md).
- [Making Predictions: An Example Using the Beer Dataset](06_PredictionInterface_1/PredictionInterface_BeerExample.md).