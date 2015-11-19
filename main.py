#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import urllib2
import urllib
import re

import webapp2
import jinja2



JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/view'),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

# [END imports]

class MainHandler(webapp2.RequestHandler):
	def get(self):        
		template = JINJA_ENVIRONMENT.get_template('index.html')
		template_values = {}
		self.response.write(template.render(template_values))

class ScanHandler(webapp2.RequestHandler):
	site = ''

	def get(self):
		self.site = urllib.unquote(self.request.get('site'))

		try :
			result = urllib2.urlopen(self.site)
			data = result.read()
			self.scan(data)
		except urllib2.URLError, e:
			self.response.write('Can not open this url : %S', self.site)

	def scan(self, content):
		# find mp3
		mp3_pattern = re.compile('"[^"]*\.mp3"', re.IGNORECASE)
		mp3_files = mp3_pattern.findall(content)
		mp3_links = []
		for file_path in mp3_files:
			mp3_links.append(self.build_link(file_path))

		# find images		
		# find javascript
		# find css

		template = JINJA_ENVIRONMENT.get_template('site.html')
		template_values = {
			'mp3_files':mp3_files, 
			'mp3_links':mp3_links,
			'site':self.site}
		self.response.write(template.render(template_values))

	def build_link(self, file_path):
		root_url = self.site[:self.site.rfind('/')];

		while file_path.find('..') != -1:
			file_path = file_path[3:]
			root_url = root_url[:root_url.rfind('/')]			
		return root_url + "/" + file_path[1:-1]

app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/scan', ScanHandler)
], debug=True)
