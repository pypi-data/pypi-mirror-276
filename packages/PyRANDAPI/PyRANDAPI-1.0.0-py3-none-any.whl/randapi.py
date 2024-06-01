# RANDAPI 1.0 BETA
import requests, json, random

url = 'https://api.jsonbin.io/v3/b/6659b0abad19ca34f8721d28/latest'

class randapi:
    def __init__(self):
        self.requested = 0
    
    def get(self, id):
        global url
        self.requested += 1
        headers = {
            'X-Master-Key': '$2a$10$4MXwBVXcD3vz9s0aPyEKP.EeEBt3qkAL9lLo57Rr..WieGP2NEIEm',
            'X-Bin-Meta': 'false'
        }

        req = requests.get(url, json=None, headers=headers)
        info = random.choice(json.loads(req.text)[id])
        
        return info
    
    def change_list(self, add, to, id):
        url = 'https://api.jsonbin.io/v3/b/6659b0abad19ca34f8721d28/latest'
        headers = {
            'X-Master-Key': '$2a$10$4MXwBVXcD3vz9s0aPyEKP.EeEBt3qkAL9lLo57Rr..WieGP2NEIEm',
            'X-Bin-Meta': 'false'
        }

        req = requests.get(url, json=None, headers=headers)
        info = json.loads(req.text)
        if add:
            info[id].append(str(to))
        elif add == False:
            info[id] = to
        
        url = 'https://api.jsonbin.io/v3/b/6659b0abad19ca34f8721d28'
        headers = {
            'Content-Type': 'application/json',
            'X-Master-Key': '$2a$10$4MXwBVXcD3vz9s0aPyEKP.EeEBt3qkAL9lLo57Rr..WieGP2NEIEm'
        }

        req = requests.put(url, json=info, headers=headers)
