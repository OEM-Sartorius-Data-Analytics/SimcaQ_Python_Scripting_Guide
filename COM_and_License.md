# Access the COM interface & check your license

SIMCA-Q offers a COM interface that can be accesed with Python by using the pywin32 extension. You can install it e.g., by running:
```
python -m pip install pywin32
```

The method *win32com.client.Dispatch()*, which takes as a parameter the ProgID or CLSID of SIMCA-Q, will then allow you to communicate with SIMCA-Q via its COM interface. By default, the ProgID of SIMCA-Q is *Umetrics.SIMCAQ*. 