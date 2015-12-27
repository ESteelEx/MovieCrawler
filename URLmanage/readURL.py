import requests, sys, os, urllib2

class URLmanager:
    def __init__(self, command):
        pass

    def authorize(self, url, username, password):
        """
        :param username: str
        :param password: str
        :return:
        """
        import urllib2

        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, username, password)
        urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))

    # -------------------------------------------------------------------------------------------------------------------
    def readURL(self, URL):
        """
        reads the given URL and returns content
        """
        req = urllib2.Request(URL)
        try:
            f = urllib2.urlopen(req)
            URLcontent = f.read()
        except urllib2.HTTPError, err:
            if err.code == 403:
                URLcontent = ''
                print 'We have no access"'
            raise

        return URLcontent

    # -------------------------------------------------------------------------------------------------------------------
    def linkfilter(self, content):
        pos = 0
        contentPos = 0
        searchStr = 'href='
        linkdb = []
        while 1:
            pos = content[contentPos + len(searchStr):].find(searchStr)
            if pos != -1:
                contentPos = contentPos + pos + len(searchStr)
                for i in range(len(content[contentPos:])):
                    if content[contentPos + len(searchStr) + 1 + i] == '"':
                        # print content[contentPos:contentPos + len(searchStr) + 2 + i]
                        linkdb.append([(content[contentPos + 1 + len(searchStr):contentPos + len(searchStr) + 1 + i])])
                        break
            else:
                break
        return linkdb

    # -------------------------------------------------------------------------------------------------------------------
    def killunique(self, linkdb, threshold=0.8):
        from difflib import SequenceMatcher

        killpos = []
        for i in range(len(linkdb)):
            print i
            for ii in range(len(linkdb)):
                ratioMatch = SequenceMatcher(None, str(linkdb[i]), str(linkdb[ii])).ratio()
                if ratioMatch > threshold and not i == ii:
                    linkdb[ii] = ''

        while 1:
            j = 0
            for i in linkdb:
                if not str(i):
                    del linkdb[j]
                    break
                j += 1
            if j == len(linkdb):
                break

        return linkdb

    # -------------------------------------------------------------------------------------------------------------------
    def readsublinks(self, linkdb):
        sublinkdb = []
        u = URLmanager('read')
        for i in linkdb:
            link = str(i)
            posStart = link.find('"')
            posEnd = link[posStart+1].find('"')
            try:
                sublinkdb.append(u.readURL(link[posStart+1:posEnd-1]))
            except:
                print link[posStart+1:posEnd-2]

        return sublinkdb

    # -------------------------------------------------------------------------------------------------------------------
    def linkfixer(self, linkdb):
        from urlparse import urlparse

        j = 0
        for i in linkdb:
            # print urlparse(str(i))
            # check for http:// at beginning
            i = str(i)
            j += 1
            if i.find('http') == -1:
                # check string at start point
                if i.find('/') == 2:
                    linkdb[j] = 'http:/' + i[2:-2]
                    if i.find('/') == 3:
                        linkdb[j] = 'http://' + i[2:-2]
                else:
                    linkdb[j] = 'http://' + i[2:-2]

        return linkdb


# -----------------------------------------------------------------------------------------------------------------------
def main():

    # URL = 'http://www.movie4k.to'
    # URL = 'https://instagram.com/kateupton/'
    # URL = 'https://www.google.de/search?q=Kate+Upton&safe=off&biw=1920&bih=1099&source=lnms&tbm=isch&sa=X&ved=0CAYQ_AUoAWoVChMI9LPNiuKDyQIVgYssCh2DDw-K'
    # URL = 'http://www.google.de/imgres?imgurl=http%3A%2F%2Fwww.returnofkings.com%2Fwp-content%2Fuploads%2F2015%2F06%2FKate-Upton-St.-Joseph-MI-667x1001.jpg&imgrefurl=http%3A%2F%2Fwww.returnofkings.com%2F65318%2Fwhy-dont-feminists-call-kate-upton-a-misogynist&h=1001&w=667&tbnid=GytYRw3v8MC_QM%3A&docid=db2EG6gLY8Q7aM&ei=e8pAVoXHPIahsAH5wZWICg&tbm=isch&iact=rc&uact=3&dur=463&page=1&start=0&ndsp=59&ved=0CEIQrQMwBGoVChMIxfCpjeKDyQIVhhAsCh35YAWh'
    # URL = 'https://de.wikipedia.org/wiki/Kate_Upton'
    # URL = 'http://www.dominikpietsch.de'
    URL = 'http://www.amazon.de'
    # URL = 'http://www.google.de/imgres?imgurl=http%3A%2F%2Fwww.returnofkings.com%2Fwp-content%2Fuploads%2F2015%2F06%2FKate-Upton-St.-Joseph-MI-667x1001.jpg&imgrefurl=http%3A%2F%2Fwww.returnofkings.com%2F65318%2Fwhy-dont-feminists-call-kate-upton-a-misogynist&h=1001&w=667&tbnid=GytYRw3v8MC_QM%3A&docid=db2EG6gLY8Q7aM&ei=e8pAVoXHPIahsAH5wZWICg&tbm=isch&iact=rc&uact=3&dur=463&page=1&start=0&ndsp=59&ved=0CEIQrQMwBGoVChMIxfCpjeKDyQIVhhAsCh35YAWh'

    u = URLmanager('read')
    URLcontent = u.readURL(URL)
    linkdb = u.linkfilter(URLcontent)
    # linkdb = u.killunique(linkdb, 1)

    linkdb = u.linkfixer(linkdb)

    print linkdb

    # sublinkdb = u.readsublinks(linkdb)

    # print sublinkdb

if __name__ == '__main__':
    main()
