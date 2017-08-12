import requests

base = 'https://api.github.com/'

# get OAuth token from Flask

class Github(object):

	def __init__(self):
		self.session = requests.Session()
		
		if hasattr(self, 'oauth_token'):
			self.session.headers['Authorization'] = 'token %s' % self.api_token
		elif hasattr(self, 'username') and hasattr(self, 'password'):
        	self.session.auth = (self.username, self.password)

	resp = requests.get(base+'/user/repos')

	print(resp.text)

