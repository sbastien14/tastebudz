from gotrue.types import User as sbUser
import json

class User(dict):
    def __init__(self, usr:sbUser):
        # Create standard instance variables:
        self.id:str = usr.id
        self.email:str = usr.email
        self.phone:str = usr.phone
        self.role:str = usr.role
        self.user_metadata:dict = usr.user_metadata
        self.obj = usr
        
        # Create instance of dictionary representation:
        self._dict = {
            "id": self.id,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "user_metadata": self.user_metadata
        }
        
        dict.__init__(self, self._dict)
        
    def __repr__(self):
        return json.dumps(self._dict, indent=2)