from flask import Flask, request, g, render_template, session, redirect, url_for

app = Flask(__name__)
class Task(object):
	def __init__(self, name, keywords, score):
		self.keywords = keywords
		self.name = name
		self.score = score
repo_name = "questo-backend"
@app.route('/showresults', methods=['GET', 'POST'])
def results():
	tasks = []
	tasks.append(Task('Using Keras built-in model', ['OpenCV', 'C++', 'Swift'], {'aryavohra04': 0.8, 'tkato0909': 0.8}))
	tasks.append(Task('Using Keras built-in model', ['OpenCV', 'C++', 'Swift'], {'tkato0909': 0.9, 'aryavohra04': 0.8, 'malayguy.123': 0.2}))
	if request.args.get('index'):
		users = []
		return render_template('results.html', repo_name=repo_name, tasks=tasks, selected_task=tasks[int(request.args.get('index'))])
	return render_template('results.html', repo_name=repo_name, tasks=tasks, selected_task=tasks[0])
app.run(debug=True, host="0.0.0.0", threaded=True)