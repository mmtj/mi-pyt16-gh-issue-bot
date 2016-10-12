#! /usr/bin/env python3

import requests
import configparser
import click

import json
import time

class IssueBot:
   
    def __init__ (self):
        self.session = None
        self.repo = None
        self.token = None
        self.wait = None

    def init (self, repo, sleep, auth, main, rules):
        self.init_config_vals(repo, sleep, auth, main, rules)
        
        self.session = requests.Session()
        self.session.headers = {'Authorization': 'token ' + self.token, 'User-Agent': 'Python'}
        
    def init_config_vals (self, repo, sleep, authcfg, maincfg, rulescfg):
        auth = configparser.ConfigParser()
        auth.read(authcfg)

        if not repo:
            self.repo = auth['github']['repo']
        else:
            self.repo = repo

        self.token = auth['github']['token']

        config = configparser.ConfigParser()
        config.read(maincfg)

        if not sleep:
            if 'sleep' in config['general']:
                self.wait = int(config['general']['sleep'])
            else:
                self.wait = 60 # Default value if not set either in config or at runtime
        else:
            self.wait = int(sleep)

    def get_issues (self, req):
        print("Trying request: ", req)
        r = self.session.get(req)

        print("JSON response: ", json.dumps(r.json(), sort_keys=True, indent=4)) # pretty print
        print("Response status code: ", r.status_code)

        return r.json()
   
    def start (self, repo, sleep, auth, config, rules):
        try:
            # prepare session
            self.init(repo, sleep, auth, config, rules) 

            req_url = "https://api.github.com/repos/%s/issues" % self.repo
            
            while (1):
                reply = self.get_issues(req_url)
                print("Next check in %d seconds" % self.wait)
                time.sleep(self.wait)

        except KeyboardInterrupt:
            print('\n\nKeyboard exception received. Exiting.')

        finally:
            self.session.close()

@click.command()
@click.option('--repo', help='GitHub repository to check (format username/reponame)')
@click.option('--sleep', help='Number of second before another check')
@click.option('--auth', default='auth.cfg', help='File with github credentials')
@click.option('--config', default='settings.cfg', help='Main config file')
@click.option('--rules', default='rules.cfg', help='Rules definition file')
def run (repo, sleep, auth, config, rules):
        
    robot = IssueBot()
    robot.start(repo, sleep, auth, config, rules)

if __name__ == '__main__':
    run()
