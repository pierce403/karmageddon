import webapp2
import time
from google.appengine.ext import ndb
from django.utils.html import escape

import urllib2
import logging

from lxml import html

def getkarma(username):

  page = urllib2.urlopen('https://www.reddit.com/user/'+str(username))
  tree = html.fromstring(str(page.read()))

  karma2 = iter(tree.xpath('/html/body/div[3]/div[1]/div/span[1]/text()')).next()
  karma1 = iter(tree.xpath('/html/body/div[3]/div[1]/div/span[2]/text()')).next()

  ckarma = int(karma1.replace(',', ''))
  pkarma = int(karma2.replace(',', ''))
  return ckarma, pkarma, ckarma+pkarma

class Person(ndb.Model):
  username = ndb.StringProperty()
  commkarma = ndb.IntegerProperty()
  postkarma = ndb.IntegerProperty()
  fullkarma = ndb.IntegerProperty()
  ctime = ndb.DateTimeProperty(auto_now_add=True,indexed=True)
  mtime = ndb.DateTimeProperty(auto_now=True,indexed=True)

class MainPage(webapp2.RequestHandler):

  def post(self):
    username=self.request.get('username')

    karma=0
    try:
      karma = getkarma(username)
    except:
      self.response.out.write("no ..")
      return

    if karma[2]>2:
      self.response.out.write("you already have too much karma")
      return

    if karma[2]<-2:
      self.response.out.write("you're a terrible person :-p")
      return

    person = Person(username=username,commkarma=karma[0],postkarma=karma[1],fullkarma=karma[2])
    person.put()

    self.response.out.write("welcome to the party")

  def get(self):

    table="\n\n<table><tr><th>[username]</th><th>[comment karma]</th><th>[post karma]</th><th>[total karma]</th></tr>\n"
    q = Person.query().order(-Person.fullkarma)
    for person in q.fetch(1000):
      table+="<tr><td>"
      table+="<a href='https://www.reddit.com/user/"+escape(person.username)+"'>"+escape(person.username)+"</a>"
      table+="</td><td>"
      table+=str(person.commkarma)
      table+="</td><td>"
      table+=str(person.postkarma)
      table+="</td><td>"
      table+=str(person.fullkarma)
      table+="</td></tr>\n"
    table+="</table>"

    self.response.out.write('''
<html><head><title>karmageddon.net</title></head>
<body><center><br>
<b>Hello BSidesPDX 2016 attendees.</b><br>
Your goal is to create and register a reddit account with very low karma.<br>
The winner is whoever can get the most karma by closing ceremonies.<br>
There will be a special prize!  Good luck!<br><br>

<form action="/" method= "post">
  reddit username: <input type="text" name="username">
  <input type="submit" value="add user">
</form><br>
'''+table+'''
<br><br>send hate tweets to <a href='https://twitter.com/deanpierce'>@deanpierce</a>
<br>source : <a href="https://github.com/pierce403/karmageddon">https://github.com/pierce403/karmageddon</a>
''')

class Cron(webapp2.RequestHandler): # update the balances per address
  def get(self):
    self.response.out.write("wut\n")

    q = Person.query().order(-Person.mtime)
    for person in q.fetch(10000):
      try:
        self.response.out.write("updating "+str(person.username)+"\n")
        karma = getkarma(person.username)
        person.commkarma=karma[0]
        person.postkarma=karma[1]
        person.fullkarma=karma[2]
        person.put()
        time.sleep(1)
      except:
        self.response.out.write("whoops\n")

app = webapp2.WSGIApplication([('/',MainPage),('/update',Cron)])
