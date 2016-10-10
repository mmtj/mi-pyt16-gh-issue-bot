#! /usr/bin/env python3

import requests
import configparser
import click

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

    return r.json()

@click.command()
@click.option('--repo', help='GitHub repository to check (in format username/reponame)')
@click.option('--sleep', help='Number of second before another check (Default: 60)')
def run (repo, sleep):
    try:
        # simple parameter validation
        # There are three sources - command line switch, config file and default value
        # If program is invoked without any argument, use config values
        # arguments from command line overrides config
        auth = configparser.ConfigParser()
        auth.read('auth.cfg')

        if not repo:
            repo = auth['github']['repo']

        token = auth['github']['token']

        config = configparser.ConfigParser()
        config.read('settings.cfg')

        if not sleep:
            if 'sleep' in config['general']:
                wait = int(config['general']['sleep'])
            else:
                wait = 60 # Default value if not set either in config or at runtime
        else:
            wait = int(sleep)

        # prepare session

        req_url = "https://api.github.com/repos/%s/issues" % repo

        session = init_session(token)
        
        while (1):
            reply = request(session, req_url)
            print("Next check in %d seconds" % wait)
            time.sleep(wait)
    
    except KeyboardInterrupt:
        print('\n\nKeyboard exception received. Exiting.')
    
    finally:
        session.close()

if __name__ == '__main__':
    run()
