# Access the COM interface of SIMCA-Q & write a first script to check your SIMCA-Q license

SIMCA-Q offers a COM interface that can be accesed with Python by using the *pywin32* extension. You can install it e.g., by running:
```
python -m pip install pywin32
```

The method *win32com.client.Dispatch()*, which takes as a parameter the *ProgID* or the *CLSID* of SIMCA-Q, will then allow you to communicate with SIMCA-Q via its COM interface. By default, the *ProgID* of SIMCA-Q is *Umetrics.SIMCAQ*. Specifically, we can use the Python extension *pywin32* to create a COM object, let's name it *simcaq*, which will give us access to SIMCA-Q e.g., by including in the Python code:
```
from win32com import client as win32
simcaq = win32.Dispatch('Umetrics.SIMCAQ')
```

This approach is known as *late binding*. However, if MakePy support for SIMCA-Q objects is available, the above code will provide what is called *early binding*. This could happen if e.g., at some point you have connected to SIMCA-Q by using:
```
from win32com import client as win32
simcaq = win32.gencache.EnsureDispatch('Umetrics.SIMCAQ')
```

Without going into the details of the difference between *late binding* and *early binding*, *early binding* is a more efficient approach. However, it is of relevance to know that *early binding* with *pywin32* might fail occasionally. If this happens, one should delete a *gen_py* folder usually located in your *Temp* directory. There are different ways around this. If you want to always enforce *late binding* you could write instead:
```
from win32com import client as win32
simcaq = win32.dynamic.Dispatch('Umetrics.SIMCAQ')
```

However, if you would still like to have the benefits of *early binding*, you could instead automate the deletion of the *gen_py* folder in case the first dispatch intent fails e.g. as suggested in this [GitHub discussion](https://gist.github.com/rdapaz/63590adb94a46039ca4a10994dff9dbe#gistcomment-2918299) by including a dedicated function:
```
def dispatch(app_name:str):
    try:
        from win32com import client
        app = client.gencache.EnsureDispatch(app_name)
    except AttributeError:
        # Corner case dependencies.
        import os
        import re
        import sys
        import shutil
        # Remove cache and try again.
        MODULE_LIST = [m.__name__ for m in sys.modules.values()]
        for module in MODULE_LIST:
            if re.match(r'win32com\.gen_py\..+', module):
                del sys.modules[module]
        shutil.rmtree(os.path.join(os.environ.get('LOCALAPPDATA'), 'Temp', 'gen_py'))
        from win32com import client
        app = client.gencache.EnsureDispatch(app_name)
    return app

if __name__ == '__main__':
    simcaq = dispatch('Umetrics.SIMCAQ')
```

The SIMCA-Q COM object provides access to additional interfaces that will allow to handle Models, Predictions etc., as we will see in later section. Moreover, the SIMCA-Q COM object also has some methods of its own. For instance, this object has methods to check the validity of your SIMCA-Q license.

We will now write a first SIMCA-Q script that will make usse of these methods. Specifically, we will use the following methods:
- *IsLicenseFileValid()*: Checks if a license file is present and, if so, if it is valid. 
- *GetLicenseFileExpireDate()*: Provides the date until the license file is valid.

The following [script] will print to the console whether the SIMCA-Q license is valid and, if so, until when:
```
from win32com import client as win32

if __name__ == '__main__':
    simcaq = win32.Dispatch('Umetrics.SIMCAQ')

    if not simcaq.IsLicenseFileValid():
        sys.exit("Invalid license file")
    else:
        print("The license is vslid and it will expire in ", simcaq.GetLicenseFileExpireDate())
```


