# SIMCA-Q Python Scripting Guide

This guide provides examples on how to use Python to develope SIMCA-Q applications.

At present, Python only can interact with the SIMCA-Q COM interface. Therefore, these apps will only work on Windows systems.

This repo also contains a *requirements.txt* that list all packages used in the examples. To install them, ideally within a virtual environment, run:
```
python -m pip install -r requirements.txt
```

## Index

- [Access the COM interface & check your license](00_COM_and_License/COM_and_License.md).
- [The IProject Interface](01_ProjectInterface/ExploreProjectInterface.md).
- [The IModelInfo Interface](02_ModelInfoInterface/ExploreModelInfoInterface.md).
- [The IDataset Interface: accessing datasets in SIMCA projects](03_DatasetInterface/ExploreDatasetInterface.md).
- [The IModel Interface: Introduction](04_ModelInterface_0/ModelInterface_Introduction.md).
- [Exploring the IModel Interface: Getting the Score Plot from models](05_ModelInterface_ScorePlot/ModelInterface_ExampleScorePlot.md).
- [The IPrediction Interface](06_PredictionInterface_0/PredictionInterface_Introduction.md).