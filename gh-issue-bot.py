#! /usr/bin/env python3

import requests
import configparser
import json
import time

def init_session (token):
    session = requests.Session()
    session.headers = {'Authorization': 'token ' + token, 'User-Agent': 'Python'}

    return session

def request (session, req):
    print("Trying request: ", req)
    r = session.get(req)

    print("JSON response: ", json.dumps(r.json(), sort_keys=True, indent=4)) # pretty print
    print("Response status code: ", r.status_code)

def run ():
    try:
        config = configparser.ConfigParser()
        config.read('auth.cfg')

        repo = config['github']['repo']
        token = config['github']['token']

        req_url = "https://api.github.com/repos/%s/issues" % repo

        session = init_session(token)
        
        while (1):
            request(session, req_url)
            time.sleep(5)
    
    except KeyboardInterrupt:
        print('\n\nKeyboard exception received. Exiting.')
    
    finally:
        session.close()

if __name__ == '__main__':
    run()
