

# ----------------------------------------------------------------------------------------------------------------------
class onlinesearch:
    # ----------------------------------------------------------------------------------------------------------------------
    def getByRevisionNumber(self, sublinksdb, revisionNumber):

        searchResult = []
        for i in sublinksdb:
            if i.find('_r' + str(revisionNumber)) != -1:
                searchResult.append(i)

        return searchResult

    # ----------------------------------------------------------------------------------------------------------------------
    def getByString(self, sublinksdbtmp, searchString):
        """
        search for string snippets separated by white space in daily db
        real time search
        search result is decimated by every search string
        So be sure to use the correct search string order
        e.g. searching for a date in db
        """
        splittedString = searchString.split(" ")
        searchResult = [s for s in sublinksdbtmp if splittedString[0] in s]
        if len(splittedString) > 1:
            for j in range(1, len(splittedString)):
                searchResult = [s for s in searchResult if splittedString[j] in s]

        return searchResult