'''
A class simulating a wrapper to access a database storing Nonces.
For this toy project, we store Nonces in memory.
'''

class FakeNonceDbService(object):
    
    def __init__(self):
        # Initializes some dictionaries to store nonces
        self._nonces_by_sid = dict()
        self._nonces_by_nid = dict()
                
    
    def create_nonce(self, nonce):
        '''
        Create a nonce entry in db
        Parameters:
            nonce = Nonce object to store in db
        '''
        # Checks parameter
        if not self._check_nonce(nonce):
            return False
        # Checks that a nonce with same values has not already been stored in db
        if (self.get_nonce_by_sid(nonce.sid) is None) and (self.get_nonce_by_nid(nonce.nid) is None):
            # Creates the nonce in db
            self._nonces_by_sid[nonce.sid] = nonce
            self._nonces_by_nid[nonce.nid] = nonce
            return True
        else:
            return False       

    def update_nonce(self, nonce):
        '''
        Update a nonce entry in db
        Parameters:
            nonce = Nonce object to update in db
        '''
        # Checks parameter
        if not self._check_nonce(nonce):
            return False
        # Checks that a nonce with same values exists in db
        if (not self.get_nonce_by_sid(nonce.sid) is None) or (not self.get_nonce_by_nid(nonce.nid) is None):
            # Updates the nonce in db
            self._nonces_by_sid[nonce.sid] = nonce
            self._nonces_by_nid[nonce.nid] = nonce
            return True
        else:
            return False        
    
    def delete_nonce(self, nonce):
        '''
        Delete a nonce entry from db
        Parameters:
            nonce = Nonce object to delete
        '''
        # Checks parameter
        if nonce is None: return False
        # Checks that a nonce with same values exists in db
        if (not self.get_nonce_by_sid(nonce.sid) is None) or (not self.get_nonce_by_nid(nonce.nid) is None):
            del self._nonces_by_sid[nonce.sid]
            del self._nonces_by_nid[nonce.nid]
            return True
        else:
            return False        
    
    def get_nonce_by_sid(self, sid):
        '''
        Gets a nonce associated to a given session id
        Parameters:
            sid = session id
        '''
        return self._nonces_by_sid.get(sid, None) if sid else None        
    
    def get_nonce_by_nid(self, nid):
        '''
        Gets a nonce associated to a given nonce id
        Parameters:
            nid = nonce id
        '''
        return self._nonces_by_nid.get(nid, None) if nid else None                
    
    def _check_nonce(self, nonce):
        if (nonce is None) or (not nonce.sid) or (not nonce.nid):
            return False
        else:
            return True        
        