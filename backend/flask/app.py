from flask import Flask, request, g, session, redirect, url_for
from flask_github import GitHub
import requests

app = Flask(__name__)
app.config['GITHUB_CLIENT_ID'] = '24e70a9e5b30650ce068'
app.config['GITHUB_CLIENT_SECRET'] = 'a797a49f99771bf1e4dda9d63f2360a46ac1a9f1'

token = str

@app.route('/login')
@app.route('/')
def login():
    return github.authorize()

github = GitHub(app)

@app.route('/callback', methods=['GET'])
@github.authorized_handler
def authorized(oauth_token):
    token = oauth_token
    return oauth_token

@github.access_token_getter
def token_getter():
    return token

    # next_url = request.args.get('next') or url_for('index')
    # if access_token is None:
    #     return redirect(next_url)

    # user = User.query.filter_by(github_access_token=access_token).first()
    # if user is None:
    # user.github_access_token = access_token

    # session['user_id'] = user.id
    # return redirect(next_url)
# @github.authorized_handler
# def authorized(shit):
#     global token
#     token = request.args.get('code')
#     return token

# @github.access_token_getter
# def token_getter():
#     user = g.user
#     if user is not None:
#         return user.github_access_token

@app.route('/repo')
def repo():
    session = requests.Session()
    session.headers['Authorization'] = 'token %s' % token
    base = 'https://api.github.com/'
    #resp = requests.get(base+'/user/repos')
    resp = session.post('https://api.github.com/user')
    return resp.text

app.run(debug=True, host="0.0.0.0", threaded=True)


