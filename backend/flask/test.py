from github import Github
import github
from nltk.corpus import stopwords
from googleapiclient import discovery
from os.path import splitext
from oauth2client.client import GoogleCredentials
import base64

credentials = GoogleCredentials.get_application_default()

def retrieve_repos(user_object_arg):
	repo_array = []

	all_repos_objects = user_object_arg.get_repos()

	for repo in all_repos_objects:
		repo_array.append(repo.name)

	return all_repos_objects, repo_array

def retrieve_collaborators(repo_object_arg):
	collaborators_array = []
	for coll in repo_object_arg.get_collaborators():
		collaborators_array.append(coll)
	return collaborators_array

def retrieve_commit_messages(repo_object_arg, user_object_arg):
	commit_message_array = []
	user_object_arg.keyactivity = {}
	for x in repo_object_arg.get_commits(author=user_object_arg):
		commit_message_array.append(str(x.commit.message).replace('\n', ' '))
		# print("hypo_keywords: ", user_object_arg.hypo_keywords)
		det_keys = [k for k in user_object_arg.hypo_keywords if k in x.commit.message]
		# print("det_keys:", det_keys)
		for k in det_keys:
			user_object_arg.keyactivity[k] = int(x.stats.total)
	return commit_message_array

def retrieve_commit_files(repo_object_arg, user_object_arg):
	commit_filename_array = []
	commit_filename_dict = {}
	counter = 0
	for x in repo_object_arg.get_commits(author=user_object_arg):
		for file in x.files:
			if counter > 9:
				return commit_filename_dict
			try:
				commit_filename_dict[file.filename] = base64.b64decode(
						repo_object_arg.get_file_contents(file.filename).content
					)
				counter += 1
			except:
				pass
	return commit_filename_dict

def retrieve_issues(repo_object_arg):
	issues_dict = {}
	for x in repo_object_arg.get_issues():
		issues_dict[x.title] = x.body
	return issues_dict

service = discovery.build('language', 'v1beta1', credentials=credentials)

def createRequest(rawText):
        body = {
            'document': {
                'type': 'PLAIN_TEXT',
                'content': rawText,
            },
            'features': {
                'extract_syntax': True,
            },

        }

        request = service.documents().annotateText(body=body)
        return request

def tag(rawText):
    request = createRequest(rawText)
    response = request.execute()
    tokens = response["tokens"]
    posDict = {}

    for item in tokens:
        if item['text']['content'] not in stopwords.words('english'):
            if item['partOfSpeech']['tag'] in posDict:
                posDict[item['partOfSpeech']['tag']].append(item['text']['content']) 
            else:
                posDict[item['partOfSpeech']['tag']] = [item['text']['content']]

    return posDict

def get_library(user, codefile, codevalue):
	user.hypo_keywords = []

	imports = {
		'.py':'import',
		'.pyx':'cimport',
		'.swift':'import',
		'.c':'include',
		'.cpp':'include',
		'.m':'include',
		'.mm':'include',
		'.java':'import',
		'.js':'require'
	}

	ext = '.' + codefile.split('.')[-1]

	if ext in imports.keys():
		search_statement = imports[ext]
		counter = 0
		for line in codevalue.split(b'\n'):
			line = line.decode()
			if counter < 10:
				counter += 1
				line = line.replace('\n', '')
				if search_statement in line:
					if ext == '.py' or '.pyx':
						if len(line.split(' ')) > 2:
							line = line.replace(search_statement, '')	
							if 'from' in line:
								# from x import y
								line = line.split(' ')[1]
							elif 'as' in line:
								# import x as y
								line = line.split(' ')[1]
						elif len(line.split(' ')) == 2:
							# import x	
							line = line.replace(search_statement, '')
							line = line.strip(' ')

					if '.' in line:
						line = line.split('.')[0]
					elif line not in user.hypo_keywords:
						user.hypo_keywords.append(line)
			else:
				return user.hypo_keywords
	return user.hypo_keywords


class task(object):
	def __init__(self, keywords):
		self.keywords = keywords
		self.score = {}

# score users for a hypothetical task
def scoreUser(userKeywords, taskKeywords):
	sharedElementCount = len(set(taskKeywords).intersection(userKeywords))
	return sharedElementCount

def scoreUsers(users, task):
	max = 0
	for user in users:
		print("keyactivity: ", user.keyactivity)
		mean = (sum(user.keyactivity.values())/len(user.keyactivity.values()))
		std_dev = sum([(x-mean)**2 for x in user.keyactivity.values()])/len(user.keyactivity.values())
		user.keywords = []
		for i, comm in enumerate(user.keyactivity.values()):
			if comm > mean + std_dev:
				user.keywords.extend(user.keyactivity.keys()[i])
		score_calculated = scoreUser(user.keywords, task.keywords)
		if score_calculated > max:
			max = score_calculated
		task.score[user.name] = score_calculated
	for user in users:
		task.score[user.name] = task.score[user.name] / max
