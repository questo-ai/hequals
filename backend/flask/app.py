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
results = None
coll_arr = None

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

        global results
        # results = task.score
        # print("printing score: ", task.score)

        url_to_redirct = "/showresults?repo_name=" + repos[repo_index].full_name + '?colls=' + str(colls)
        return redirect(url_to_redirct)
    return render_template('repos.html', repos=repos)

@app.route('/staticfile/<path:path>')
def staticfile(path):
    return send_from_directory('static', path)
class Task(object):
    def __init__(self, name, keywords, score):
        self.keywords = keywords
        self.name = name
        self.score = score
@app.route('/showresults', methods=['GET', 'POST'])
def results():
    global results
    tasks = []
    colls = request.args.getlist("colls")
    for user in colls:
        for u in results.keys():
            if user.name == u:
                tasks.append(Task('Using Keras built-in model', user.hypo_keywords, results))
                tasks.append(Task('Broken download links of the Windows GPU', ['.net', 'networking', 'nvidia-CUDA'], {'tkato0909': 0.974, 'aryavohra04': 0.823, 'superspy.827': 0.214}))
                return render_template('results.html', repo_name='aryavohra04/questo-backend', tasks=tasks, selected_task=tasks[0])
    if request.args.get('index'):
        users = []
        tasks.append(Task('Using Keras built-in model', ['Python3', 'Keras', 'machine-learning'], {'karinawalker': 0.744, 'aryavohra04': 0.323, 'superspy.827': 0.214}))
        tasks.append(Task('Redesign the iOS page for question answering.', ['Swift', 'Object-C', 'iOS'], {'tkato0909': 0.974, 'superspy.827': 0.823, 'aryavohra04': 0.741}))
        userkeywords=[[['Python', 'PHP', 'machine-learning', 'tensorflow'],
                        ['C++', 'Java', 'Keras', 'iOS'],
                        ['Python', 'javascript', 'node.js', 'JSON']
                        ], [['Swift', 'iOS', 'Keras', 'CUDA'],
                        ['Python', 'Swift', 'node.js', 'JSON'],
                        ['C++', 'Java', 'Keras', 'iOS'],
                        ]]
        prof=[['https://avatars.githubusercontent.com/u/23270560?size=120','https://avatars.githubusercontent.com/u/8716483?size=100','https://avatars1.githubusercontent.com/u/6974757?v=4&s=400'], ['https://avatars2.githubusercontent.com/u/8716434?v=4&s=460', 'https://avatars1.githubusercontent.com/u/6974757?v=4&s=400', 'https://avatars.githubusercontent.com/u/8716483?size=100']]
        return render_template('results.html', repo_name='aryavohra04/questo-backend', tasks=tasks, selected_task=tasks[int(request.args.get('index'))], userkeywords=userkeywords[int(request.args.get('index'))], prof=prof[int(request.args.get('index'))])
        # return render_template('results.html', repo_name=request.args.get("repo_name"), tasks=tasks, selected_task=tasks[int(request.args.get('index'))])
    tasks.append(Task('Using Keras built-in model', ['Python3', 'Keras', 'machine-learning', 'tensorflow'], {'karinawalker': 0.744, 'aryavohra04': 0.323, 'superspy.827': 0.214}))
    tasks.append(Task('Redesign the iOS page for question answering.', ['Swift', 'Object-C', 'iOS'], {'tkato0909': 0.974, 'superspy.827': 0.823, 'aryavohra04': 0.741}))
    prof=[['https://avatars.githubusercontent.com/u/23270560?size=120','https://avatars.githubusercontent.com/u/8716483?size=100','https://avatars1.githubusercontent.com/u/6974757?v=4&s=400'], ['https://avatars2.githubusercontent.com/u/8716434?v=4&s=460', 'https://avatars1.githubusercontent.com/u/6974757?v=4&s=400', 'https://avatars.githubusercontent.com/u/8716483?size=100']]
    return render_template('results.html', repo_name='aryavohra04/questo-backend', tasks=tasks, selected_task=tasks[0], userkeywords=[['Python', 'PHP', 'machine-learning', 'tensorflow'],
                                                                                                                                        ['C++', 'Java', 'Keras', 'iOS'],
                                                                                                                                        ['Python', 'javascript', 'node.js', 'JSON']
                                                                                                                                        ], prof=prof[0])


app.run(debug=True, host="0.0.0.0", threaded=True)