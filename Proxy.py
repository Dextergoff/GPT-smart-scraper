import os
from dotenv import load_dotenv 
load_dotenv() 
class GetProxy:
    def __init__(self):
        self.result = None 
    def retrive(self):
        """ return iproyal proxy settings with varibles from .env """
        self.result= {
                'server': os.getenv('PROXY_URL'),
                'username': os.getenv('PROXY_USERNAME'),
                'password': os.getenv('PROXY_PASS')
            }
        return self.result