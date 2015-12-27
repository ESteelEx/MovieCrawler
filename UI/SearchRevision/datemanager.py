
def convertToSeconds(dateLastRefresh):
    import time
    import datetime

    return time.mktime(datetime.datetime.strptime(dateLastRefresh, "%Y-%m-%d").timetuple())

# ----------------------------------------------------------------------------------------------------------------------
def extractDateFromDFName(listValue):
    """
    :param listValue:
    :return:
    """
    stat = 1
    #dailyDate.date = []

    i = 0
    while 1:
        pos = listValue.find('_')
        if pos == -1:
            stat = -1
            break
        try:
            dateString = str(int(listValue[pos+1:pos+14]))
            break
        except:
            pass
        i += 1
        listValue = listValue[pos+1:]

    if stat != -1:
        year = dateString[0:4]
        month = dateString[4:6]
        day = dateString[6:8]

        dailyDate = str(year) + '-' + str(month) + '-' + str(day)
    else:
        dailyDate = None

    return dailyDate