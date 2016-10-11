#! /usr/bin/env python3

import requests
import configparser
import click

import json
import time

class IssueBot:
   
    def __init__ (self):
        self.init_config_vals()
        
        self.session = requests.Session()
        self.session.headers = {'Authorization': 'token ' + self.token, 'User-Agent': 'Python'}
        
    def init_config_vals (self):
        auth = configparser.ConfigParser()
        auth.read('auth.cfg')

        self.repo = auth['github']['repo']
        self.token = auth['github']['token']

        config = configparser.ConfigParser()
        config.read('settings.cfg')

        if 'sleep' in config['general']:
            self.wait = int(config['general']['sleep'])
        else:
            self.wait = 60 # Default value if not set either in config or at runtime

    def request (self, req):
        print("Trying request: ", req)
        r = self.session.get(req)

        print("JSON response: ", json.dumps(r.json(), sort_keys=True, indent=4)) # pretty print
        print("Response status code: ", r.status_code)

        return r.json()

#   @click.command()
#   @click.option('--repo', help='GitHub repository to check (in format username/reponame)')
#   @click.option('--sleep', help='Number of second before another check (Default: 60)')
    def run (self, sleep=5):
        try:
            # simple parameter validation
            # There are three sources - command line switch, config file and default value
            # If program is invoked without any argument, use config values
            # arguments from command line overrides config
            
            # prepare session
            req_url = "https://api.github.com/repos/%s/issues" % self.repo
            
            while (1):
                reply = self.request(req_url)
                print("Next check in %d seconds" % self.wait)
                time.sleep(self.wait)

        except KeyboardInterrupt:
            print('\n\nKeyboard exception received. Exiting.')

        finally:
            self.session.close()

if __name__ == '__main__':
    robot = IssueBot()
    robot.run()
