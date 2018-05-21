#coding:utf-8
import urllib
import urllib2
import re

# data = {}
# number = '12345'
#
# for i in range(400):
#     data['nothing'] = number
#     url_values = urllib.urlencode(data)
#     url = 'http://www.pythonchallenge.com/pc/def/linkedlist.php'
#     full_url = url+'?'+url_values
#
#     foo=urllib2.urlopen(full_url)
#     foo = foo.read()
#     print foo
#     foo= foo.split(" ")
#
#     number = [i for i in foo if i.isdigit()][0]

url='http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing='

nothing ='82682'

search = re.compile(" (\d*)$")

search_html = re.compile("\.html$")

for i in xrange(400):
    #range和xrange有什么区别
    print("%s: "%nothing)

    line = urllib.urlopen("%s%s"%(url,nothing)).read()

    print(line)

    if search_html.findall(line):
        break

    match = search.findall(line)
    if match:
        nothing=match[0]
    else:
        nothing=str(int(nothing)/2)