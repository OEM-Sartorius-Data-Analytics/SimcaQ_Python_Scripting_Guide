# Working with Batch Models: An Introduction

With a valid SIMCA-QP+ license, it is possible to use SIMCA-Q to load and investigate SIMCA Batch Models as well as to use them for predictions.

To start with, the Project Interface offers the GetIsBatchProject() method to determine whether the project is a batch project. If that is the case, the Project interface also offers the method GetNumberOfBatchModels() to retrieve the number of Batch Models within the project.

For loading a Batch Model into a BatchModel object, we first need to find the project number from its index by using the GetModelNumberFromIndex() method of the Project Interface. Once this number is know we can load the model into a IBatchModel object using the GetBatchModel() method.

To exemplify all this, the following code will load all Batch Models from a Project into a list:
```
from win32com import client as win32
simcaq = win32.dynamic.Dispatch('Umetrics.SIMCAQ')

project = simcaq.OpenProject(<pathSimcaProject>, "")

if project.GetIsBatchProject():
    batch_models = []
    for iModel in range(1,project.GetNumberOfBatchModels()+1):
        nModel = project.GetModelNumberFromIndex(iModel)
        batch_models.append(project.GetBatchModel(nModel))
```

We can then look into the IBatchModel. It is important to note at this point that, in the same way that SIMCA does, SIMCA-Q treats Batch Evolution Models and Batch Level Models as different types. 
From The IBatchModel interface we can get the number of Batch Evolution Models using the method GetNumberOfBEM() amd the number of Batch Level Models with the method GetNumberOfBLM().
Then we can iterate over the different Batch Model types, retrieve the corresponding model number with the methods GetBatchEvolutionModelNumber() and GetBatchLevelModelNumber(),
and from these numbers retrieve the corresponding IBatchEvolutionModel and IBatchLevelModel objects using the methods GetBatchEvolutionModel() and GetBatchLevelModel().

For instance, we can extend the previous code to load objects with the BEM and BLM of the first BM of a project:
```
nModel = project.GetModelNumberFromIndex(1)
BModel = project.GetBatchModel(nModel)

NumberBEMs = bModel.GetNumberOfBEM()
NumberBLMs = bModel.GetNumberOfBLM()

BEModels = []
BLModels = []

for iBEM in range(1,NumberBEMs+1):
    nBEM = bModel.GetBatchEvolutionModelNumber(iBEM)
    BEModels.append(BModel.GetBatchEvolutionModel(nBEM))

for iBLM in range(1,NumberBLMs+1):
    nBLM = bModel.GetBatchEvolutionModelNumber(iBLM)
    BLModels.append(BModel.GetBatchEvolutionModel(nBLM))
```

IBatchEvolutionModel and IBatchLevelModel objects provide access to the methods of the respective interfaces. 

Additionally, both can access the methods of the more generic IModel interface.
We can for instance know if the model is fitted by using the IsModelFitted() method.
We can get the name of the model with the method GetName(), the number of predictive components with GetNumberOfComponents(), or the score matrix with GetT().
These are just some examples. For a complete list of IModel methods refer to the official SIMCA-Q help.

As an example of the possibilities, the following code generates and prints a pandas dataframe with the scores of a Batch Level Model,
previously loaded into the variable BLModel:
```
def string_vector_to_list(simcaq_string_vector):
    string_vector_list = []
    for i in range(1,simcaq_string_vector.GetSize()+1):
        string_vector_list.append(simcaq_string_vector.GetData(i))
    return string_vector_list

def float_matrix_to_list(simcaq_float_matrix):
    float_matrix_2D_list = []
    for iRow in range(1, simcaq_float_matrix.GetNumberOfRows()+1):
        float_matrix_1D_list = []
        for iCol in range(1, simcaq_float_matrix.GetNumberOfCols()+1):
            float_matrix_1D_list.append(simcaq_float_matrix.GetData(iRow,iCol))
        float_matrix_2D_list.append(float_matrix_1D_list)
    return float_matrix_2D_list

scores = BLModel.GetT(None)

models = string_vector_to_list(scores.GetColumnNames())
batches = string_vector_to_list(scores.GetRowNames())
data = float_matrix_to_list(scores.GetDataMatrix())

df = pd.DataFrame(columns=batches, index=models)

for i in range(len(models)):
    df.loc[models[i]] = data[i]

print(df)
```