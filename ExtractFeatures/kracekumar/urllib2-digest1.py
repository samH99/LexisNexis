import urllib2

URL = 'http://localhost/allowed.html' 

ah = urllib2.HTTPDigestAuthHandler()
ah.add_password('Realm','http://localhost/','senthil','kumaran')
urllib2.install_opener(urllib2.build_opener(ah))
r = urllib2.Request(URL)
obj = urllib2.urlopen(r)
print obj.read()
