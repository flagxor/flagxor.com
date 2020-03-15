import webapp2

class Redirect(webapp2.RequestHandler):
  def get(self):
    self.redirect("https://www.flagxor.com/")

app = webapp2.WSGIApplication([
    ('/.*', Redirect),
], debug=False)
