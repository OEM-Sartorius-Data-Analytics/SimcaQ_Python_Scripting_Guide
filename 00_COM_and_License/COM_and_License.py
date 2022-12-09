from win32com import client as win32

if __name__ == '__main__':
    simcaq = win32.Dispatch('Umetrics.SIMCAQ')

    if not simcaq.IsLicenseFileValid():
        sys.exit("Invalid license file")
    else:
        print("The license is vslid and it will expire in ", simcaq.GetLicenseFileExpireDate())
