# eclipse-pay

Python library for interacting with scratch currencies.

# Documentation

### Running a server

#### Run a server with password on scratch
```python
from eclipse_pay import Auth,Server

auth = Auth({
    "type": "password",
    "username": "LIZARD_OFFICIAL",
    "password": "nuh uh"
})

server = Server(
    auth=auth,
    project_id="<project id>",
)

server.run()
```

#### Run a server with session id on scratch
```python
from eclipse_pay import Auth,Server

auth = Auth({
    "type": "sessionid",
    "username": "LIZARD_OFFICIAL",
    "sessionid": "nuh uh"
})

server = Server(
    auth=auth,
    project_id="<project id>",
)

server.run()
```

#### Run a server with username on turbowarp
```python
from eclipse_pay import Auth,Server

auth = Auth({
    "type": "tw",
    "username": "LIZARD_OFFICIAL"
})

server = Server(
    auth=auth,
    project_id="<project id>",
    on_turbowarp=True
)

server.run()
```

### Adding new currencies
Create a new file in eclipse_pay/currencies (e.g. coolcoin.py):
```python

from eclipse_pay import BaseCurrency

class CoolCoin(BaseCurrency):
    @property
    def name():
        return "coolcoin" # in lowercase
    def check_transaction(sender,recipient,amount):
        """Make this function check, if *sender* sent *recipient* *amount* CoolCoins. (Usually with an API.)"""
        return True
```

And then, add your currency in eclipse_pay/\_\_init\_\_.py

```python
from currencies.lrcoin import LRCOIN
from currencies.coolcoin import CoolCoin
_CURRENCY = [
    LRCOIN,
    CoolCoin
]
```