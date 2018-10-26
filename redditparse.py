import urllib2
import logging

from lxml import html

username = 'creamdreammeme'
print('pulling https://old.reddit.com/user/'+str(username))

headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
page = urllib2.urlopen(urllib2.Request('https://old.reddit.com/user/'+str(username),None,headers))
stuff = str(page.read())
tree = html.fromstring(stuff)
print("got the tree ")
#print(stuff)

karma1 = iter(tree.xpath('//*[@id="container"]/div/div/div/div[3]/div[2]/div[2]/div[1]/div[3]/span/div/text()[2]')).next().split(' ')[0]
print("BOOOOM1: "+str(karma1))

karma2 = iter(tree.xpath('//*[@id="container"]/div/div/div/div[3]/div[2]/div[2]/div[1]/div[3]/span/div/text()[1]')).next().split(' ')[0]
print("BOOOOM2: "+str(karma2))

ckarma = int(karma1.replace(',', ''))
pkarma = int(karma2.replace(',', ''))

print("cleaned the karma "+str(ckarma))
print("cleaned the karma "+str(pkarma))
