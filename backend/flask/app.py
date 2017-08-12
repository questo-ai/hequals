from flask import Flask, request, g, render_template, session, redirect, url_for
from github import Github
import github
import test

app = Flask(__name__)

repo_name = ""

@app.route('/repo')
def repo():
    repo_dict = github.get('repos/cenkalti/github-flask')
    return str(repo_dict)

g = None
user_inst = None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        global g
        g = Github(username, password)
        global user_inst
        user_inst = g.get_user()
        return redirect("/repos")
    return render_template('index.html')

@app.route('/repos', methods=['GET', 'POST'])
def select():
    if request.method == 'POST':
        repo = request.form['repo']
        colls = test.retrieve_collaborators(repo)
        comm_mess = test.retrieve_commit_messages(user_inst)
        comm_files = test.retrieve_commit_files(user_inst)
        return redirect("/showresults")

    repos = (test.retrieve_repos(user_inst))[0]
    return render_template('repos.html', repos=repos)

@app.route('/staticfile/<path:path>')
def staticfile(path):
    return send_from_directory('static', path)

@app.route('/showresults', methods=['POST'])
def results():
    return render_template('results.html', repo_name=repo_name)

app.run(debug=True, host="0.0.0.0", threaded=True)