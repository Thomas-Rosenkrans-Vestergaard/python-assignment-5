from string import ascii_letters
from multiprocessing import Pool, Value
import os
import requests
import time

def find_combinations():
    for a in ascii_letters:
        for b in ascii_letters:    
            yield a + b

def check_password(password):
    data = {"password": password}
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://127.0.0.1:5000/auth', json=data, headers=headers)
    return response.status_code == 200

def sequential_hack(on_complete):
    for password in find_combinations():
        if check_password(password):
            on_complete(password)
            return
    
    on_complete(password)
    
