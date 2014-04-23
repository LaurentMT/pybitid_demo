'''
A class simulating a wrapper to access a database storing Users.
For this toy project, we store Users in memory.
'''

class FakeUserDbService(object):
    
    def __init__(self):
        # Initializes some dictionaries to store users
        self._users_by_uid = dict()
        self._users_by_addr = dict()
        
    
    def create_user(self, user):
        '''
        Create a user entry in db
        Parameters:
            user = User object to store in db
        '''
        # Checks parameter
        if not self._check_user(user):
            return False
        # Checks that a user with same values has not already been stored in db
        if (self.get_user_by_uid(user.uid) is None) and (self.get_user_by_address(user.address) is None):
            # Creates the user in db
            self._users_by_uid[user.uid] = user
            self._users_by_addr[user.address] = user
            return True
        else:
            return False         

    def update_user(self, user):
        '''
        Update a user entry in db
        Parameters:
            user = User object to update in db
        '''
        # Checks parameter
        if not self._check_user(user):
            return False
        # Checks that a user with same values exists in db
        if (not self.get_user_by_uid(user.uid) is None) or (not self.get_user_by_address(user.address) is None):
            # Updates the user in db
            self._users_by_uid[user.uid] = user
            self._users_by_addr[user.address] = user
            return True
        else:
            return False        
    
    def delete_user(self, user):
        '''
        Delete a user entry from db
        Parameters:
            user = User object to delete
        '''
        # Checks parameter
        if user is None: return False
        # Checks that a user with same values exists in db
        if (not self.get_user_by_uid(user.uid) is None) or (not self.get_user_by_address(user.address) is None):
            del self._users_by_uid[user.uid]
            del self._users_by_addr[user.address]
            return True
        else:
            return False        
    
    def get_user_by_uid(self, uid):
        '''
        Gets a user associated to a given user id
        Parameters:
            uid = user id
        '''
        return self._users_by_uid.get(uid, None) if uid else None        
    
    def get_user_by_address(self, addr):
        '''
        Gets a user associated to a given bitcoin address
        Parameters:
            addr = bitcoin address
        '''
        return self._users_by_addr.get(addr, None) if addr else None                
    
    def _check_user(self, user):
        if (user is None) or (not user.uid) or (not user.address):
            return False
        else:
            return True        
    
        