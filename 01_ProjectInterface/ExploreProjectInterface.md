# The IProject Interface

The SIMCAQ interface provides access to methods to access additional interfaces/create additional type of objects. One is the *IProject* interface. The *IProject* interface allows accessing SIMCA projects i.e., usp files, and retrieve all information they contain. As we will see later, this interface also allows to access additional interface to handle e.g., models and datasets.

*IProject* objects are creted by using the SIMCAQ method *OpenProject()*, which takes two input parameters. These are strings accounting for i) the full path to the SIMCA project file and ii) the corresponding password in case the usp file is encrypted (this can be an empty string if there is no password).

For instance, assuming that you have already created a SIMCA-Q COM object as describe in the [previous section](), let's name it *simcaq*, and that you have the path to a SIMCA project within a variable named e.g., *pathSimcaProject*, you could create an *IProject* object with no password by:
```
project = simcaq.OpenProject(pathSimcaProject, "")
```

This *IProject* has methods that allow to retrieve straightaway some main parameters of the SIMCA project. For instance, we could retrieve the name of the project by using the *GetProjectName()* method:
```
projectName = project.GetProjectName() 
```

the number of models within the SIMCA project by using the *GetNumberOfModels()* method:
```
numberModels = project.GetNumberOfModels()
```

and the number of datasets within the SIMCA project by using the *GetNumberOfDatasets()* method:
```
numberDatasets = project.GetNumberOfDatasets()
```

When needed, we can also dispose of the *IProject* object by using the *DisposeProject()* method:
```
project.DisposeProject()
```

In this repository you can find a standalone [example script](ExploreProjectInterface.py) that takes as an argument the path to a SIMCA project and that will print to the console the name of the project and its numbers of models and datasets.

