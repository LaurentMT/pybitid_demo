'''
A model for nonces objects
'''
from datetime import datetime
from pybitid import bitid


class Nonce(object):
    
    # Expiration delay (in seconds)
    EXPIRATION_DELAY = 600
    
    def __init__(self, sid):
        '''
        Constructor
        Parameters:
            sid = session id associated to the nonce
        '''
        self.sid = sid
        self.uid = None
        # Initializes a value for the nonce (let's call that the nonce id)
        self.nid = bitid.generate_nonce()
        # Sets the creation date
        self.created = datetime.now()
        
    
    def has_expired(self):
        '''
        Checks if nonce has expired
        '''
        delta = datetime.now() - self.created
        return delta.total_seconds() > Nonce.EXPIRATION_DELAY