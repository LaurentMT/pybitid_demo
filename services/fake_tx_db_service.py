'''
A class simulating a wrapper to access a database storing bitcoin transactions "received" by the website.
For an e-retailer it could be a db storing bitcoin transactions sent by customers buying products.
For others use cases it could be a db storing bitcoin micro-transactions sent to a given address by people who want to register.

This database (or service) should allow to check if a given address has sent a transaction to my site.
The goal is to prevent abuses flooding the users database by checking a proof of goodwill (payment, purchase, burn...)
'''

class FakeTxDbService(object):
    
    def __init__(self):
        pass
    
    def check_proof_of_goodwill(self, address):
        '''
        Checks a proof of goodwill for a given address
        '''
        # The test world is wonderful, welcome everybody ! ;)
        return True