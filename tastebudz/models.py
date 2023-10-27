from gotrue.types import User as sbUser
import json

class User(dict):
    def __init__(self, usr:sbUser):
        # Create standard instance variables:
        self.id:str = usr.id
        self.email:str = usr.email
        self.username:str = usr.user_metadata.get('username')
        self.phone:str = usr.phone
        self.role:bool = usr.user_metadata.get('role')
        self.first_name:str = usr.user_metadata.get('first_name')
        self.last_name:str = usr.user_metadata.get('last_name')
        self.dob:str = usr.user_metadata.get('dob')
        # self.user_metadata:dict = usr.user_metadata
        # self.obj = usr
        
        # Create instance of dictionary representation:
        self._dict = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "dob": self.dob
        }
        
        dict.__init__(self, self._dict)
        
    def __repr__(self):
        return json.dumps(self._dict, indent=2)