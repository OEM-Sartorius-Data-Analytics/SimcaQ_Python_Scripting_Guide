from win32com import client as win32

if __name__ == '__main__':
    
    simcaq = win32.Dispatch('Umetrics.SIMCAQ')

    project = simcaq.OpenProject(PathSimcaProject, "")
