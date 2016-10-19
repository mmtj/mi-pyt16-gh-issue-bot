#! /usr/bin/env python3

from flask import Flask, request, render_template

import requests
import configparser
import click

import json
import time
import re

class IssueBot:
    DEFAULT_WAIT = 60
    DEFAULT_AUTH = 'auth.cfg'
    DEFAULT_RULES = 'rules'

    def __init__ (self):
        self.session = None
        self.repo = None
        self.token = None
        self.wait = None

        self.authcfg = self.DEFAULT_AUTH
        self.rulescfg = self.DEFAULT_RULES

    def init_basic (self, authcfg, rulescfg):
        self.authcfg = authcfg
        self.rulescfg = rulescfg

    def init (self, repo, sleep, main):
        self.init_config_vals(repo, sleep, main)
        
        self.session = requests.Session()
        self.session.headers = {'Authorization': 'token ' + self.token, 'User-Agent': 'Python'}
        
    def init_config_vals (self, repo, sleep, maincfg):
        auth = configparser.ConfigParser()
        auth.read(self.authcfg)

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
                self.wait = self.DEFAULT_WAIT # Default value if not set either in config or at runtime
        else:
            self.wait = int(sleep)

        rules_conf = configparser.ConfigParser()
        rules_conf.read(self.rulescfg)

        self.rr = {} # rewrite rules
        for key, value in rules_conf['labels'].items():
            self.rr[key] = re.compile(value)

    def get_issues (self, req):
        print("Trying request: ", req)
        r = self.session.get(req)

        #print("JSON response: ", json.dumps(r.json(), sort_keys=True, indent=4)) # pretty print
        print("Response status code: ", r.status_code)

        return r.json()
  
    def apply_rules (self, title):
        for label, regex in self.rr.items():
            if regex.search(title):
                return [label]
            
        return None

    def label_issue (self, json_data):
        number = json_data['number']
        url = "https://api.github.com/repos/%s/issues/%s/labels" % (self.repo, number)

        if not json_data['labels']:
            title = json_data['title']
            
            payload = self.apply_rules(title)
            if not payload:
                payload = [self.rules_conf['default']['label']]
            
            print("Trying request: ", url)
            r = self.session.post(url, json=payload)
            print("Response status code: ", r.status_code)

    def process_issues (self, json_data):
        for row in json_data:
            data = self.label_issue(row)

    def start (self, repo, sleep, config):
        try:
            # prepare session
            self.init(repo, sleep, config) 

            req_url = "https://api.github.com/repos/%s/issues" % self.repo
            
            while (1):
                reply = self.get_issues(req_url)
                self.process_issues(reply)

                print("Next check in %d seconds" % self.wait)
                time.sleep(self.wait)

        except KeyboardInterrupt:
            print('\n\nKeyboard exception received. Exiting.')

        finally:
            self.session.close()
            
    def one_pass_check ():
        pass

# Flask webapp part
webapp = Flask(__name__)
robot = IssueBot()
 
@webapp.route('/')
def index():
    return render_template('index.html', title='Yet Another GitHub Issue Bot', description='github issue bot')

@webapp.route('/hook', methods=['POST'])
def hook ():
    data = request.get_json()
    print("Json_data recieved: ", data)

    return ''

@click.group()
def cli():
    pass

@cli.command()
@click.option('--auth', default='auth.cfg', help='File with github credentials')
@click.option('--rules', default='rules', help='Rules definition file')
def web(auth, rules):
    """Run bot as web app"""
    robot.init_basic(auth, rules)
    
    webapp.run(debug=True)

@cli.command()
@click.option('--repo', help='GitHub repository to check (format username/reponame)')
@click.option('--sleep', help='Number of second before another check')
@click.option('--auth', default='auth.cfg', help='File with github credentials')
@click.option('--config', default='settings.cfg', help='Main config file')
@click.option('--rules', default='rules', help='Rules definition file')
def console (repo, sleep, auth, config, rules):
    """Run bot localy from command line """
    robot = IssueBot()
    robot.init_basic(auth, rules)
    robot.start(repo, sleep, config)

if __name__ == '__main__':
    cli()
