'''
A very basic model for user entities
We manage a unique bitcoin address per user but we could imagine to allow several addresses
'''
import uuid
from datetime import datetime


class User(object):
    
    def __init__(self, address):
        '''
        Constructor
        Parameters:
            address = bitcoin address associated to the user
        '''
        self.address = address
        # Initializes the uid
        self.uid = str(uuid.uuid4())
        # Sets some additional attributes
        self.created = datetime.now()
        self.signin_count = 0
        
        
        