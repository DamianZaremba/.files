#!/usr/bin/python
import urllib2
import smtplib
import os
import hashlib
from BeautifulSoup import BeautifulSoup
DUMP_DIR = "/home/damian/.bm_job_shiz/"

if __name__ == "__main__":
	try:
		response = urllib2.urlopen("http://bytemark.co.uk/company/work_for_us")
	except urllib2.HTTPError, e:
		print "Could not grab page, server returned %d" % e.code
	except urllib2.URLError, e:
		print "Could not reach the server to grab page: %s" % e.reason
	else:
		data = response.read()
		soup = BeautifulSoup(data)

		'''
		Pretty sure the we don't have any jobs line is a <p></p>
		so this should work....
		'''
		jobs = []
		for job in soup.findAll('div', {'id': 'content_left'})[0].findAll('h3'):
			jobs.append( job.string )

		if len(jobs) > 0:
			emsg = "From: finnix@nodehost.co.uk\r\n"
			emsg += "To: damian@damianzaremba.co.uk\r\n"
			emsg += "Subject: New BM jobs!\r\n"
			emsg += "Importance: High\r\n\r\n" # OVER 9000!

			if not os.path.isdir(DUMP_DIR):
				print "Creating %s" % DUMP_DIR
				os.makedirs(DUMP_DIR)

			new_jobs = ""
			other_jobs = ""
			for job in jobs:
				jhash = hashlib.md5(job).hexdigest()
				jpath = os.path.join(DUMP_DIR, jhash) + ".job"
				if not os.path.isfile(jpath):
					new_jobs += job + "\n"

					print "Adding %s" % jpath
					open(jpath, 'w').close() # Now we just need os.touch
				else:
					other_jobs += job + "\n"

			msg = "New jobs:\n"
			msg += new_jobs
			msg += "\nOlder jobs:\n"
			msg += other_jobs
			emsg += msg

			# We only mail on new jobs
			if len(new_jobs) > 0:
				try:
					server = smtplib.SMTP('localhost')
					server.set_debuglevel(1)
					server.sendmail("finnix@nodehost.co.uk", "damian@damianzaremba.co.uk", emsg)
					server.quit()
				except:
					print "Could not send mail :("
