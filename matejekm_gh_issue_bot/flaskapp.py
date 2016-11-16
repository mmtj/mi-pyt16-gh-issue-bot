from flask import Flask, request, render_template
from configparser import ConfigParser

from .issuebot import IssueBot

import os
import jinja2
from markdown import markdown
import textwrap

webapp = Flask(__name__)
robot = IssueBot()

base_path = os.path.dirname(os.path.abspath(__file__))
config_base_path = base_path + '/config'

config = ConfigParser()
config.read(config_base_path + '/flask.cfg')

global_config = ConfigParser()
global_config.read(config_base_path + '/settings.cfg')

md_content = None

with open(base_path + '/content/about.md', 'r') as readme:
    md_content = readme.read()

@webapp.route('/')
def index():
    hook_base_url = config['hook']['base_url']
    md_content_final = md_content.replace('<sample.domain>', hook_base_url) 
    return render_template('index.html', title='Yet Another GitHub Issue Bot', description='github issue bot', md_content = md_content_final)

@webapp.route('/hook', methods=['POST'])
def hook ():
    data = request.get_json()
    
    if global_config['general']['debug']:
        print("Json_data recieved: ", data)

    repo = data['repository']['full_name']
    
    robot.set_repo(repo)
    robot.init_token()
    robot.init_rules()
    robot.open_session()
    robot.label_issue(data['issue'])
    robot.close_session()
    
    return ''

# credits: fedora-python/fedoralovespython.org
@webapp.template_filter('markdown')
def convert_markdown(text):
    text = textwrap.dedent(text)
    result = jinja2.Markup(markdown(text))
    return result
