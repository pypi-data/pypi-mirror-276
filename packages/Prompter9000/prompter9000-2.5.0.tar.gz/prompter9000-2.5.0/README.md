## Prompter9000
Quick &amp; easy way to edit dictionaries and create counters. Console & programmatic 
usages are supported.

**NEW:** *Verson 2.0.2*
1. Data types can now be preserved. 
2. Boolean detection, as well.
3. Result Key [__conv_ok]
    - == *True* iff types preserved. 
    - *False* == at least one defaulted to string.
4.) Result Key [__btn_ok]
    - == *True* when [Okay] was pressed
    - else *False*.

### Programatic
Edit a dictionary:
```
from Prompter9000.PyEdit import *
params = {"NAME":'My', "ACCOUNT":123456, "Subscriber":False}
EditDict.edit(params)
```

Create a click-counter:
```
from Prompter9000.PyCount import *
params = {'Hits': '0', 'Miss': '0', 'Other': '10'}
Counter.edit(params)
```
*GUI*: Dictionary results will be returned ONLY IF the data was changed. Otherwise an empty dictionary will be returned.

May also be used from the C.L.I:

### Console

Dynamically edit a dictionary:
```
python PyEdit.py "{'NAME': 'My', 'PHONE': '123-456', 'EMAIL': 'a.Geekbo@zbobo.com'}"
{'NAME': 'My', 'PHONE': '123-456', 'EMAIL': 'a.Geekbo@zbobo.com', '__btn_ok': True}
```

Dynamic click-to-update counters:
```
python PyCount.py "{'Hits': '0', 'Miss': '0', 'Other': '10'}"
{'Hits': '12', 'Miss': '10', 'Other': '44', '__btn_ok': True}
```

*CLI*: The **__btn_ok** will be either **True** when user-selected, else **False**.

### PyPi

Now available on [PyPi](https://pypi.org/project/Prompter9000/)
