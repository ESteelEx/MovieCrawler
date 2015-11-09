import requests, sys, os, urllib2, filterMovies

class URLmanager:
    def __init__(self, command):
        pass

    def readURL(self, URL):
        """
        reads the given URL and returns content
        """
        req = urllib2.Request(URL)
        try:
            f = urllib2.urlopen(req)
            URLcontent = f.read()
        except:
            raise
        return URLcontent

    def linkfilter(self, content):
        pos = 0
        contentPos = 0
        searchStr = 'href='
        i = 0
        while 1:
            pos = content[contentPos + len(searchStr):].find(searchStr)
            if pos != -1:
                contentPos = contentPos + pos + len(searchStr)

            contentTrimmed = content[contentPos + len(searchStr):]

            print pos
            print contentPos
            i += 1

def main():

    URL = 'http://www.movie4k.to'

    u = URLmanager('read')
    URLcontent = u.readURL(URL)
    u.linkfilter(URLcontent)

if __name__ == '__main__':
    main()
