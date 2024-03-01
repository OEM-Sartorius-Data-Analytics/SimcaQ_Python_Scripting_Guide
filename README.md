# SIMCA-Q Python Scripting Guide

This repository aims to serve as a guide on how to use Python to develop SIMCA-Q applications.

At present, Python only can interact with SIMCA-Q via its COM interface. Therefore, these apps will only work on Windows systems.

When writing Python SIMCA-Q apps, you will first need to create a SIMCA-Q COM object. This object will have methods of its own that you can use in your script. Moreover, some of these methods will allow to create different types of objects, each with a new collection of methods, that will allow you to handle SIMCA projects, methods, predictions, etc.

We will not cover here all the possibilities of SIMCA-Q, only the most common so you can have a broad idea on how to interface with SIMCA-Q. For a complete list of available classes and methods I would suggest to have a look to the [Help Files](https://www.sartorius.com/download/961736/simca-q-17-0-1-help-files-en-b-00260-sartorius-zip-data.zip) available at the [Sartorius SIMCA-Q web](https://www.sartorius.com/en/products/oem/oem-data-analytics/simca-q). In this web you can also find useful tutorials and examples on a variety of programming languages.

## Index

### SIMCA-QP

- [Access the COM interface of SIMCA-Q & write a first script to check your SIMCA-Q license](00_COM_and_License/COM_and_License.md).
- [The IProject Interface](01_ProjectInterface/ExploreProjectInterface.md).
- [The IModelInfo Interface](02_ModelInfoInterface_0/ExploreModelInfoInterface.md).
- [The IDataset Interface: accessing datasets in SIMCA projects](03_DatasetInterface/ExploreDatasetInterface.md).
- [The IModel Interface: Introduction](04_ModelInterface_0/ModelInterface_Introduction.md).
- [The IModel Interface: Exploring Models](04_ModelInterface_1/ModelInterface_ExploringModels.md).
- [Making Predictions: The IPreparePrediction and IPrediction Interfaces](06_PredictionInterface_0/PredictionInterface_Introduction.md).
- [Making Predictions: An Example Using the Beer Dataset](06_PredictionInterface_1/PredictionInterface_BeerExample.ipynb).

### SIMCA-QM

...

### SIMCA-QP+

- [Working with Batch Models: An Introduction](20_Batch_Models/Batch_Models.md).
- [Making Predictions with Batch Level Models](20_Batch_Models/BLM_Predictions.md).