from flask import Flask, request, g, session, redirect, url_for
from flask_github import GitHub

app = Flask(__name__)
app.config['GITHUB_CLIENT_ID'] = '24e70a9e5b30650ce068'
app.config['GITHUB_CLIENT_SECRET'] = 'a797a49f99771bf1e4dda9d63f2360a46ac1a9f1'

@app.route('/login')
@app.route('/')
def login():
    return github.authorize()

github = GitHub(app)

@app.route('/callback', methods=['GET'])
def authorized():
    return request.args.get('code')

'''
    next_url = request.args.get('next') or url_for('index')
    if oauth_token is None:
        flash("Authorization failed.")
        return redirect(next_url)

    user = User.query.filter_by(github_access_token=oauth_token).first()
    if user is None:
        user = User(oauth_token)
        db_session.add(user)

    user.github_access_token = oauth_token
    db_session.commit()
    return redirect(next_url)

def authorized():
    print(token)
    next_url = 'localhost:5000/index'
    return ''''''
'''

@app.route('/repo')
def repo():
    repo_dict = github.get('repos/cenkalti/github-flask')
    return str(repo_dict)
app.run(debug=True, host="0.0.0.0", threaded=True)