from flask import Flask, request, render_template
from issuebot import IssueBot

webapp = Flask(__name__)
robot = IssueBot()
 
@webapp.route('/')
def index():
    return render_template('index.html', title='Yet Another GitHub Issue Bot', description='github issue bot')

@webapp.route('/hook', methods=['POST'])
def hook ():
    data = request.get_json()
    print("Json_data recieved: ", data)

    repo = data['repository']['full_name']
    
    robot.set_repo(repo)
    robot.init_token()
    robot.init_rules()
    robot.open_session()
    robot.label_issue(data['issue'])
    robot.close_session()
    
    return ''
