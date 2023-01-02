from win32com import client as win32
import argparse
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':

    # Retrieve the name of the SIMCA project and of the model name passed as
    # parameters when calling the python script
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--project", required=True, help="Path to the SIMCA project")
    ap.add_argument("-m", "--model", required=True, help="model name")
    args = vars(ap.parse_args())
    pathSimcaProject = args["project"]
    modelName = args["model"]

    # Boolean variable to determine if the model has been found
    modelFound = False

    #Connect to the SIMCA-Q COM interface
    try:
        # simcaq = win32.Dispatch('Umetrics.SIMCAQ')
        simcaq = win32.gencache.EnsureDispatch('Umetrics.SIMCAQ')
    except:
        print('Could not connect to SIMCA-Q.')
        raise SystemExit

    # Open the SIMCA project
    try:
        project = simcaq.OpenProject(pathSimcaProject, "")
    except:
        print('Could not open the project.')
        raise SystemExit

    #Retrieve the number of models in the SIMCA project
    number_models = project.GetNumberOfModels() 

    # Iterate over indices of all project models
    for model_index in range(1, number_models+1):

        # The index does not neccesarily coincide wit the model number
        # But we need the model number to retrieve information about the model
        model_of_interest_number = project.GetModelNumberFromIndex(model_index)

        # Once we know the model number, we can retrieve the Model Interface
        # for the specific model
        model = project.GetModel(model_of_interest_number)

        # Retrieve the name of the model of interest
        model_of_interest_name = model.GetModelName()

        # Check if the model name coincides with that passed as an input
        # parameter to the script
        # If it coincides, we update the boolean variable modelFound
        # and then exit the iteration
        if model_of_interest_name == modelName:
            modelFound = True
            break

    # If the model name passed as an input parameter was not found
    # in the SIMCA project, we exit the script
    if modelFound == False:
        print('Could not find the specified model')
        raise SystemExit

    ############################################################
    ################ SUMMARY OF FIT PARAMETERS
    ############################################################

    
    # Retrieve IVectorData object to handle Q2(cum)
    q2cum = model.GetQ2Cum()
    # Retrieve IStringVector object to handle names of components used
    # for calculating Q2(cum)
    q2cum_ComponentNames = q2cum.GetRowNames()
    # Retrieve number of components used for calculating Q2(cum)
    numberComponentsQ2Cum = q2cum_ComponentNames.GetSize()
    # Populate an array with the names of the components used for
    # calculating Q2(cum)
    q2cum_ComponentNamesArray = []
    for iComponent in range(1,numberComponentsQ2Cum+1):
        q2cum_ComponentNamesArray.append(q2cum_ComponentNames.GetData(iComponent))
    # Retrieve IFloatMatrix object to handle Q2(cum) values    
    q2cum_DataMatrix = q2cum.GetDataMatrix()
    # Populate an array with the values of Q2(cum) for each component    
    q2cum_DataArray = []
    for iComp in range(1,numberComponentsQ2Cum+1):
        q2cum_DataArray.append(q2cum_DataMatrix.GetData(iComp,1))
    

    # Retrieve IVectorData object to handle R2X(cum)
    r2xcum = model.GetR2XCum()
    # Retrieve IStringVector object to handle names of components used
    # for calculating R2X(cum)
    r2xcum_ComponentNames = r2xcum.GetRowNames()
    # Retrieve number of components used for calculating R2X(cum)
    numberComponentsR2XCum = r2xcum_ComponentNames.GetSize()
    # Populate an array with the names of the components used for
    # calculating R2X(cum)
    r2xcum_ComponentNamesArray = []
    for iComponent in range(1,numberComponentsR2XCum+1):
        r2xcum_ComponentNamesArray.append(r2xcum_ComponentNames.GetData(iComponent))
    # Retrieve IFloatMatrix object to handle R2X(cum) values    
    r2xcum_DataMatrix = r2xcum.GetDataMatrix()
    # Populate an array with the values of R2X(cum) for each component    
    r2xcum_DataArray = []
    for iComp in range(1,numberComponentsR2XCum+1):
        r2xcum_DataArray.append(r2xcum_DataMatrix.GetData(iComp,1))


    ############################################################
    ################ SCORES
    ############################################################
    
    # Retrieve an IVectorData object to handle scores for all model dimensions
    scoresVectorData = model.GetT(None)

    #A different way to do it passing an IIntVector as input parameter
    """
    numComponents = model.GetNumberOfComponents()

    componentVector = simcaq.GetNewIntVector(numComponents)

    for i in range(1,numComponents+1):
        componentVector.SetData(i,i)

    scoresVectorData = model.GetT(componentVector)
    """
    
    # IStringVector to retrieve the names of observations
    # for which scores were retrieved:
    observationNamesScoresVectorData = scoresVectorData.GetRowNames()
    # Number of observations for which the scores have been retrieved:
    numberObservationNamesScoresVectorData = observationNamesScoresVectorData.GetSize()
    # Retrieve and print the names of the observations for which the scores were retrieved:
    for iObs in range(1,numberObservationNamesScoresVectorData+1):
        #print(observationNamesScoresVectorData.GetData(iObs))
        pass
    

    # IStringVector to retrieve the score labels
    labelsScoresVectorData = scoresVectorData.GetColumnNames()
    # Number of Scores
    numberLabelsScoresVectorData = labelsScoresVectorData.GetSize()
    # Retrieve and print the score labels
    for iScore in range(1,numberLabelsScoresVectorData+1):
        #print(labelsScoresVectorData.GetData(iScore))
        pass

    # IFloatMatrix to retrieve score values
    scoresDatamatrix = scoresVectorData.GetDataMatrix()
    iObs = 8
    iComponent = 1
    #print(scoresDatamatrix.GetData(iObs,iComponent))

    iScoreX = 1
    iScoreY = 2

    df = pd.DataFrame(columns=[
        labelsScoresVectorData.GetData(iScoreX),
        labelsScoresVectorData.GetData(iScoreY)
    ])

    for col in range(numberLabelsScoresVectorData):
        for row in range(numberObservationNamesScoresVectorData):
            df.at[
                observationNamesScoresVectorData.GetData(row+1),
                labelsScoresVectorData.GetData(col+1)
            ] = scoresDatamatrix.GetData(row+1,col+1)

    df.plot(kind = 'scatter',
            x = labelsScoresVectorData.GetData(iScoreX),
            y = labelsScoresVectorData.GetData(iScoreY)
            )

    plt.show()

    ############################################################
    ################ LOADINGS
    ############################################################

    isWaveletCompressed = False
    # IVectorData object to handle loadings
    loadingsVectorData = model.GetP(None,isWaveletCompressed)

    print(loadingsVectorData)

    # IStringVector object to handle the name of variables
    variablesLoadingsVectorData = loadingsVectorData.GetRowNames()

    # IStringVector object to handle the name of components
    componentsLoadingsVectorData = loadingsVectorData.GetColumnNames()

    print(variablesLoadingsVectorData)
    print(componentsLoadingsVectorData)

    # Number of variables
    numberVariablesLoadingsVectorData = variablesLoadingsVectorData.GetSize()

    # Number of components
    numberComponentsLoadingsVectorData = componentsLoadingsVectorData.GetSize()

    print('numberVariablesLoadingsVectorData ',numberVariablesLoadingsVectorData)
    print('numberComponentsLoadingsVectorData ',numberComponentsLoadingsVectorData)

    # Populate an array with the names of variables
    namesVariablesLoadingsVectorData = []
    for iVar in range(1,numberVariablesLoadingsVectorData+1):
        namesVariablesLoadingsVectorData.append(variablesLoadingsVectorData.GetData(iVar))

    # Populate an array with the names of components
    namesComponentsLoadingsVectorData = []
    for iComp in range(1,numberComponentsLoadingsVectorData+1):
        namesComponentsLoadingsVectorData.append(componentsLoadingsVectorData.GetData(iComp))

    loadingsDataMatrix = loadingsVectorData.GetDataMatrix()

    iVar = 47
    iComp =1
    loadingValue = loadingsDataMatrix.GetData(iVar,iComp)

    print(loadingValue)
                                                
    
