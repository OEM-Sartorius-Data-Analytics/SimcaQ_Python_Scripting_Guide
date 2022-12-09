# Access the COM interface & check your license

SIMCA-Q offers a COM interface that can be accesed with Python by using the pywin32 extension. You can install it e.g., by running:
```
python -m pip install pywin32
```

The method *win32com.client.Dispatch()*, which takes as a parameter the ProgID or CLSID of SIMCA-Q, will then allow you to communicate with SIMCA-Q via its COM interface. By default, the ProgID of SIMCA-Q is *Umetrics.SIMCAQ*. Specifically, we can create a COM object, let's name it *simcaq*, which will give us access to SIMCA-Q e.g., by including in the Python code:
```
from win32com import client as win32
simcaq = win32.Dispatch('Umetrics.SIMCAQ')
```

The simcaq object not only provide access to additional interfaces but also to some methods. For instance, those dealing with SIMCA-Q licensing. In the example below we used two of this methods:
- *IsLicenseFileValid()*: Checks if a license file is present and in that case valid. 
- *GetLicenseFileExpireDate()*: Provides the date until the license file is valid.

Specifically, the script below will print whether the lices is valid and, if so, until when:
```
from win32com import client as win32

if __name__ == '__main__':
    simcaq = win32.Dispatch('Umetrics.SIMCAQ')

    if not simcaq.IsLicenseFileValid():
        sys.exit("Invalid license file")
    else:
        print("The license is vslid and it will expire in ", simcaq.GetLicenseFileExpireDate())
```


