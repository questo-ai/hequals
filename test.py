from github import Github
import github
from nltk.corpus import stopwords
from googleapiclient import discovery
from os.path import splitext
from oauth2client.client import GoogleCredentials
import base64

# ARYAS OAUTH TOKEN
g = Github("46658ee63b136199658e3a201ccbddec743bda00")

user = g.get_user()
#print(user.name)
#print(user.email)
#print(user.login)

credentials = GoogleCredentials.get_application_default()

def retrieve_repos(user_object_arg):
	repo_array = []

	all_repos_objects = user_object_arg.get_repos()

	for repo in all_repos_objects:
		#print(type(repo))
		repo_array.append(repo.name)
		#print(repo.name)

	return all_repos_objects, repo_array

def retrieve_commit_messages(repo_object_arg):
	commit_message_array = []
	for x in repo_object_arg.get_commits(author=user):
		commit_message_array.append(str(x.commit.message).replace('\n', ' '))
	return commit_message_array

def retrieve_commit_files(repo_object_arg):
	commit_filename_array = []
	commit_filename_dict = {}
	counter = 0
	for x in repo_object_arg.get_commits(author=user):
		#print(type(x))
		#return False
		#commit_filename_array.append(x.files.filename)
		for file in x.files:
			print("counter: ", counter)
			if counter > 9:
				return commit_filename_dict
			# print(
			# 	base64.b64decode(
			# 		repo_object_arg.get_file_contents(file.filename).content
			# 	)
			# )
			commit_filename_dict[file.filename] = base64.b64decode(
					repo_object_arg.get_file_contents(file.filename).content
				)
			#print(x.files.contents_url)
			counter += 1
	return commit_filename_dict

repo_obj, array = retrieve_repos(user)
files = retrieve_commit_files(repo_obj[3])

print(repo_obj[3].name)

#print(array)

string = ""
# ASSUMES THEY'VE CHOSEN A REPO AND WE KNOW WHAT INDEX IT IS
for x in retrieve_commit_messages(repo_obj[3]):
	#print(x)
	string += x

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
    # logger.debug('TAG CALLED')
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

bant = "Fix some missing requires, globals, whitespace Change some http scripts to use host table instead of IP in requests Ensure resolveall only affects hostname-derived NetBlocks Document the tls.servername script-arg. See #949 Regen man page to include latest doc updates Expand CIDR documentation to cover IPv6 as well. Document the '*all' host discovery syntax."

# print(tag(bant))

# PSEUDO CODE FOR THE IMPORT PARSING
# LIBRARIES ARE KEYWORDS

def get_library(codefile, codevalue):
	keywords = []

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

	_, ext = splitext(codefile)
	if ext in imports.keys():
		#print(ext)
		search_statement = imports[ext]
		counter = 0
		for line in codevalue.split('\\n'):
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
					if line not in keywords:
						keywords.append(line)
					#keywords.append(next(line, None))


	# with open(codefile) as code:
	# 	_, ext = splitext(codefile)
	# 	if ext in imports.keys():
	# 		search_statement = imports[ext]
	# 		counter = 0
	# 		for line in code:
	# 			if counter < 3:
	# 				if search_statement in line:
	# 					if ext == '.py':
	# 						line = line.strip('\n')
	# 						line = line.replace(search_statement, '')
	# 						if 'from' in line:
	# 							line = line.split()[1]
	# 					keywords.append(line)
	# 				else:
	# 					counter += 1
	# 			else:
	# 				pass

	return keywords

#print(get_library('/Users/aryavohra/questo-backend/app.py'))

#print(files)

for x in files:
	print(get_library(str(x), str(files[x])))



#retrieve_commit_messages(repo_obj)
# for repo in user.get_repos():
#     #for x in repo.get_branches():
#     #	print(repo.get_branch(x.name).commit)
#     #	print(x.name)
#     	#print(repo.get_branch(x))
#     print(repo.name)
#     # for x in repo.get_commits(author=user):
#     # 	print(x.commit.message)
#     	# for y in x.get_comments():
#     	# 	print(y)
#      	# print(x)

#    # repo.edit(has_wiki=False)