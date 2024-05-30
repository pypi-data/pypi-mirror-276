r"""
Python library for interacting with scratch currencies.
"""


from scratchattach import Session
from scratchattach import login
from scratchattach import CloudRequests,TwCloudRequests,TwCloudConnection





class InvalidAuthType(Exception):pass


class Auth:
    def __init__(self,authdata):
        if authdata["type"] == "sessionid":
            self.account:Session = Session(authdata["sessionid"],username=authdata["username"])
            self.username = authdata["username"]
        elif authdata["type"] == "password":
            self.account:Session= login(authdata["username"],authdata["password"])
            self.username = authdata["username"]
        elif authdata["type"] == "tw":
            self.username = authdata["username"]
        else:
            raise InvalidAuthType("Authentication type is not valid. (tw/password/sessionid)")
        

class BaseCurrency:
    """Base Currency API handler"""
    def __init__(self) -> None:pass
    @staticmethod
    def check_transaction(sender,recipient,amount) -> bool:
        """Modify this to return True if the transaction has been made, otherwise False."""
        return False


from currencies.lrcoin import LRCOIN

_CURRENCY=[
    LRCOIN
]


_CURRENCY = {i.name():i for i in _CURRENCY}

class Server:
    def __init__(self,auth:Auth,project_id:int,on_turbowarp:bool=False) -> None:
        project_id = str(project_id)
        recipient = auth.username or auth.account.get_linked_user().username
        if on_turbowarp:
            self.cr = TwCloudRequests(TwCloudConnection(project_id,username=auth.username),used_cloud_vars=["1"])
        else:
            self.cr = CloudRequests(auth.account.connect_cloud(project_id),used_cloud_vars=["1"])
        @self.cr.request
        def payment(c,a):
            responder:BaseCurrency = _CURRENCY.get(c,BaseCurrency)
            return 1 if responder.check_transaction(self.cr.get_requester(),recipient,int(a)) else 0
    def run(self):
        self.cr.run()
