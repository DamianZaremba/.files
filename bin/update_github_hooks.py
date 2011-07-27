#!/usr/bin/python
import urllib2
import urllib
import cookielib
from BeautifulSoup import BeautifulSoup

try:
	from simplejson import json
except ImportError:
	import json

GITHUB_IGNORE_REPOS = [
	"tweets",
]
GITHUB_USERNAME = "damianzaremba"
GITHUB_COOKIES = '''
'''
TWITTER_TOKEN = ""
TWITTER_SECRET = ""
IRC_SERVER = "delta.cluenet.org"
IRC_PORT = "1337"
IRC_PASS = ""
IRC_ROOM = "#damian" # Only specify one, just so the bot sends something

def update_twitter_settings(user_name, repo_name):
	global GITHUB_COOKIES
	print "Doing: %s/%s" % (user_name, repo_name)

	request = urllib2.Request(
		"https://github.com/%s/%s/admin/hooks" % (
			urllib.quote(user_name),
			urllib.quote(repo_name)
		)
	)
	request.add_header("Cookie", GITHUB_COOKIES.strip())

	try:
		response = urllib2.urlopen(request)
	except urllib2.HTTPError, e:
		print "Server returned error %d" % e.code
	except urllib2.URLError, e:
		print "Could not reach the server: %s" % e.reason
	else:
		soup = BeautifulSoup(response.read())
		minibucket = soup.findAll('div', {'id': 'twitter_minibucket'})[0]

		data = {}
		for x in minibucket.findAll('input'):
			try:
				data[ x['name'] ] = x['value']
			except:
				pass

		data['Twitter[token]'] = TWITTER_TOKEN
		data['Twitter[secret]'] = TWITTER_SECRET
		data['hook[active]'] = '1'
		data['Twitter[digest]'] = ''

		request = urllib2.Request(
			"https://github.com/%s/%s/admin/service" % (
				urllib.quote(user_name),
				urllib.quote(repo_name)
			)
		)

		request.add_header("Content-Type", "application/x-www-form-urlencoded")
		request.add_header("Cookie", GITHUB_COOKIES.strip())
		data = urllib.urlencode(data)

		try:
			response = urllib2.urlopen(request, data)
		except urllib2.HTTPError, e:
			print "Server returned error %d" % e.code
		except urllib2.URLError, e:
			print "Could not reach the server: %s" % e.reason
		else:
			print "%s twitter updated!" % repo_name

def update_irc_settings(user_name, repo_name):
	global GITHUB_COOKIES
	print "Doing: %s/%s" % (user_name, repo_name)

	request = urllib2.Request(
		"https://github.com/%s/%s/admin/hooks" % (
			urllib.quote(user_name),
			urllib.quote(repo_name)
		)
	)
	request.add_header("Cookie", GITHUB_COOKIES.strip())

	try:
		response = urllib2.urlopen(request)
	except urllib2.HTTPError, e:
		print "Server returned error %d" % e.code
	except urllib2.URLError, e:
		print "Could not reach the server: %s" % e.reason
	else:
		soup = BeautifulSoup(response.read())
		minibucket = soup.findAll('div', {'id': 'irc_minibucket'})[0]

		data = {}
		for x in minibucket.findAll('input'):
			try:
				data[ x['name'] ] = x['value']
			except:
				pass

		data['IRC[server]'] = IRC_SERVER
		data['IRC[port]'] = IRC_PORT
		data['IRC[room]'] = IRC_ROOM
		data['IRC[password]'] = IRC_PASS
		data['IRC[ssl]'] = ''
		data['IRC[message_without_join]'] = '1'
		data['IRC[no_colors]'] = ''
		data['IRC[long_url]'] = ''
		data['hook[active]'] = '1'

		request = urllib2.Request(
			"https://github.com/%s/%s/admin/service" % (
				urllib.quote(user_name),
				urllib.quote(repo_name)
			)
		)

		request.add_header("Content-Type", "application/x-www-form-urlencoded")
		request.add_header("Cookie", GITHUB_COOKIES.strip())
		data = urllib.urlencode(data)

		try:
			response = urllib2.urlopen(request, data)
		except urllib2.HTTPError, e:
			print "Server returned error %d" % e.code
		except urllib2.URLError, e:
			print "Could not reach the server: %s" % e.reason
		else:
			print "%s irc updated!" % repo_name

if __name__ == "__main__":
	request = urllib2.Request("https://github.com/api/v2/json/repos/show/%s" % GITHUB_USERNAME)
	#request = urllib2.Request("https://api.github.com/users/%s/repos" % GITHUB_USERNAME)
	request.add_header("Accept", "application/json")

	try:
		response = urllib2.urlopen(request)
	except urllib2.HTTPError, e:
		print "Server returned error %d" % e.code
	except urllib2.URLError, e:
		print "Could not reach the server: %s" % e.reason
	else:
		data = json.loads(response.read())

		for repo in data['repositories']:
		#for repo in data:
			repo_name = repo['name']
			repo_private = repo['private']
			owner_login = repo['owner']
			#owner_login = repo['owner']['login']

			if repo_name not in GITHUB_IGNORE_REPOS:
				if repo_private == True:
					print "Skipping '%s'" % repo_name
					continue

				try:
					update_twitter_settings(owner_login, repo_name)
				except Exception, e:
					print e

				try:
					update_irc_settings(owner_login, repo_name)
				except Exception, e:
					print e
			else:
				print "Skipping %s" % repo_name
