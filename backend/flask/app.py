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
    repos = (test.retrieve_repos(user_inst))[0]
    if request.method == 'POST':
        repo_index = int(request.form['repo'])

        colls = test.retrieve_collaborators(repos[repo_index])

        for user in colls:
            comm_files = test.retrieve_commit_files(repos[repo_index], user)
            for name, content in comm_files.items():
                keywords = test.get_library(user, name, content)
                user.hypo_keywords = keywords
            comm_mess = test.retrieve_commit_messages(repos[repo_index], user)

        for t, b in test.retrieve_issues(repos[repo_index]).items():
            task = test.task([k for k in keywords if k in t or b])
            test.scoreUsers(colls, task)

        url_to_redirct = "/showresults?repo_name=" + repos[repo_index].full_name
        return redirect(url_to_redirct)
    return render_template('repos.html', repos=repos)

@app.route('/staticfile/<path:path>')
def staticfile(path):
    return send_from_directory('static', path)

@app.route('/showresults', methods=['GET', 'POST'])
def results():
    # Give this page issues with corresponding people suitable for the task

    if request.args.get("repo_name") != None:
        print("it exists")
    return render_template('results.html', repo_name=request.args.get("repo_name"))

app.run(debug=True, host="0.0.0.0", threaded=True)