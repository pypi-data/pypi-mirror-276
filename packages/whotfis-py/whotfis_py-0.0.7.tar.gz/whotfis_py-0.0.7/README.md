# Avaiability
| Platform | Status               |
|----------|----------------------|
| MacOS    | Supported ✅          |
| Linux    | In Progress 🚧       |
| Windows  | Not supported yet  ❌ |


# Installation
To install the package, just run the following command:
```bash
pip install whotfis-py
```
# Usage
```python
import whotfis_py
result = whotfis_py.lookup("QUERY", registry)
```
The package has different classes for different registers on which will the whois lookup be performed, so when executing the query is possible to specify the database MACRO

```python
import whotfis_py
from whotfis_py import registries

whotfis_py.lookup("QUERY", registries.RADB)
```
From the available registers the program supports:

- ARPIN
- APNIC
- ABUSE
- AFRINIC
- USMILITARY
- INTERNIC
- IANA
- KRNIC
- LACNIC
- RIPE
- RADB

If you want to specify a custom register you also need to provide the server name for that register

```python
whotfis_py.lookup("QUERY", registries.CUSTOM, "whois.radb.net")
```

## Results
The `lookup()` function will return a class depending on the registry you passed, all the classes are specified in the file `whois_py/result.py`, if you want to list all the possible values at runtime you can use the `dir()`method on the object

```python
result = whotfis_py.lookup("QUERY", registries.RADB)
attributes = dir(result)
```

All the classes inherit from the `whois_result` super class, which provide the `dict()` method to convert all the instances of the class to dictionary
```python
result = whotfis_py.lookup("QUERY", registries.RADB)
print(result.dict())
```

Since the CUSTOM registry output is unknown the parameters will be setted at runtime during the lookup, the accepted parameters are only in the `key:value` shape.

In case of duplicate keys in the output there are two policies, a list of appendable keys is provided for each class in the `whois_result` class, if the key is not in the list the value will be overwritten, otherwise the value will be appended to the others.