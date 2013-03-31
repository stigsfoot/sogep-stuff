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
 
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db
 
class Message(db.Model):
    text = db.StringProperty(multiline=True)
    image = db.BlobProperty()
 
class MainHandler(webapp.RequestHandler):
    def get(self):
        # This code is activated when we go to the page i.e. no post
        # is performed
 
        # Get all messeages
        message_query = Message.all()
        messages = message_query.fetch(10)
 
        template_values = {'messages': messages}
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
 
    def post(self):
        # If a new message has been posted then put it in the DB
        newMessage = Message()
        newMessage.text = self.request.get( "form_text")
        newMessage.image = self.request.get( "form_image")
        newMessage.put()
        # Now I redirect back to the page itself thus calling the
        # get(self) declaration
        self.redirect('/')
 
class GetImage (webapp.RequestHandler):
    def get(self):
        message = db.get(self.request.get("entity_id"))
        if message.image:
            self.response.headers['Content-Type'] = "image/png"
            self.response.out.write(message.image)
 
def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/img', GetImage)
                                         ], debug=True)
    util.run_wsgi_app(application)
 
if __name__ == '__main__':
    main()