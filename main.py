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
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template

import os

import sys
sys.path.insert(0, 'tweepy.zip')

import twitter_auth
import twitter_methods
import show

class MainHandler(webapp.RequestHandler):
    def get(self):
      try:
        values = {}
        path = os.path.join(os.path.dirname(__file__), 'main.htm')
        self.response.out.write(template.render(path, values))
      except:
        self.response.out.write('Application Error')

def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/show', twitter_methods.Tweet),
                                          ('/twitter', twitter_auth.Authenticate_for_Twitter),
                                          ('/twitter/callback', twitter_auth.Authenticate_for_Twitter_Callback)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
