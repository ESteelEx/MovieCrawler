#!/usr/bin/python

# ----------------------------------------------------------------------------------------------------------------------
def refresh(configfile, dbStorage, dailylinklist):
    import os, time
    from datemanager import extractDateFromDFName
    from datemanager import convertToSeconds

    import UI.SearchRevision.datemanager as DM

    stat = 1

    if os.path.exists(dbStorage):
        sublinksdb = []
        with open(dbStorage) as f:
            sublinksdbStorage = f.readlines()

        # in a first stage we proof how much time has passed till last update.
        dateLastRefresh = extractDateFromDFName(str(sublinksdbStorage[0]))
        dateInSeconds = convertToSeconds(dateLastRefresh)
        deltatime = time.time() - dateInSeconds
        if deltatime/3600 >= 48: # are we later then a day?
            remainingDays = (deltatime/3600) / 24 # how many days we are overdated
            dateIntervall = []
            for i in range(1, int(remainingDays)+1):
                nextDayFloat = dateInSeconds + i*(24*60*60)
                dateIntervall.append(time.strftime('%Y-%m-%d', time.gmtime(nextDayFloat)))

            sublinksdb = rebuildIntervall(configfile, dbStorage, dateIntervall)

        for i in range(len(sublinksdbStorage)):
            sublinksdb.append([[sublinksdbStorage[i][:-1]]]) # this is confusing and wrong. please correct

        for j in reversed(range(len(dailylinklist))):
            searchResult = [s for s in sublinksdb if dailylinklist[j] in str(s)]
            if not searchResult:
                sublinksdb.insert(0, [[dailylinklist[j]]]) # insert at the beginning of db.

        # write data base
        stat = writeDB(sublinksdb, dbStorage, strRange=(2, -2))
        # stat = writeDB(sublinksdb, 'dat/testDB.dat', strRange=(2, -2)) # for test issues

    else:
        # build up complete data base
        stat = rebuild(configfile, dbStorage)

    return stat

# ----------------------------------------------------------------------------------------------------------------------
def rebuildIntervall(configfile, dbStorage, dateIntervall):
    """
    :param configfile:
    :param dbStorage:
    :param dateIntervall:
    :return:
    """
    import wx
    from httpmanager import readURL
    from searchrevdialog import getConfigData
    from searchrevdialog import httpReader
    from searchrevdialog import eraseifnot

    pulse_dlg = wx.ProgressDialog(title="Completing data base",
                                  message="Receiving missing time intervall ... ",
                                  maximum=int(101),
                                  style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)

    ficon = 'dat/images/search.ico'
    icon = wx.Icon(ficon, wx.BITMAP_TYPE_ICO)
    # icon = wx.IconFromBitmap('dat/images/search.ico')
    pulse_dlg.SetIcon(icon)

    userData = getConfigData(configfile)
    serverdata = userData[0]

    # get list from daily server
    URL = readURL.URLmanager('read')
    URL.authorize(serverdata.url, serverdata.user, serverdata.passw)

    # get all daily names and file versions
    sublinks = []
    sublinksdb = []
    canceledProcess = -1
    ii = 0
    for i in reversed(range(len(dateIntervall))):
        # process progress bar
        updmessage = "Receiving missing time intervall ... " + " - " + str(round((float(ii) / float(len(dateIntervall))) * 100)) + ' %' # + str(i) + " of " + str(len(linkdb)) +
        (keepGoin, skip) = pulse_dlg.Update(round((float(ii) / float(len(dateIntervall)-1)) * 100), updmessage)
        if not keepGoin:
            canceledProcess = 1
            break

        # get information from daily date
        linkstr = str(dateIntervall[i])
        sublinks.append(serverdata.url + linkstr)
        subcontent = URL.readURL(sublinks[ii])
        sublinksdbtmp = URL.linkfilter(subcontent)
        sublinksdb.append(eraseifnot(sublinksdbtmp, '.zip'))
        ii += 1

    pulse_dlg.Destroy()

    return sublinksdb


# ----------------------------------------------------------------------------------------------------------------------
def rebuild(configfile, dbStorage):
    """
    :param configfile:
    :param dbStorage:
    :return:
    """
    import wx
    from httpmanager import readURL
    from searchrevdialog import getConfigData
    from searchrevdialog import httpReader
    from searchrevdialog import eraseifnot

    pulse_dlg = wx.ProgressDialog(title="Building up data base",
                                  message="Receiving daily information ... ",
                                  maximum=int(101),
                                  style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)

    userData = getConfigData(configfile)
    serverdata = userData[0]

    # get list from daily server
    dailycontent = httpReader(serverdata)
    URL = readURL.URLmanager('read')
    linkdb = URL.linkfilter(dailycontent)
    linkdb = eraseifnot(linkdb, 'num')

    # get all daily names and file version to extract revision number in the end
    sublinks = []
    sublinksdb = []
    canceledProcess = -1
    for i in range(len(linkdb)):

        updmessage = "Receiving information ... " + " - " + str(round((float(i) / float(len(linkdb))) * 100)) + ' %' # + str(i) + " of " + str(len(linkdb)) +
        (keepGoin, skip) = pulse_dlg.Update(round((float(i) / float(len(linkdb))) * 100), updmessage)
        if not keepGoin:
            canceledProcess = 1
            break

        linkstr = str(linkdb[i])
        sublinks.append(serverdata.url + linkstr[2:-2])
        subcontent = URL.readURL(sublinks[i])
        sublinksdbtmp = URL.linkfilter(subcontent)
        sublinksdb.append(eraseifnot(sublinksdbtmp, '.zip'))

    if canceledProcess != 1:
        stat = writeDB(sublinksdb, dbStorage, strRange=(2, -2))
    else:
        stat = -1

    pulse_dlg.Destroy()

    return stat

# ----------------------------------------------------------------------------------------------------------------------
def writeDB(sublinksdb, dbStorage, strRange=(0, 0)):
    """
    All sublinks that were found under main link were stored in a list and are written to a specified file here.

    :param sublinksdb: list, bundle of str
    :param dbStorage: str, where to store link list
    :param strRange: tuple, default (0,0), str being and str end
    :return: int, status of written file. Was it successful?
    """
    stat = 1
    try:
        f = open(dbStorage, 'w')
        for i in range(len(sublinksdb)):
            for ii in range(len(sublinksdb[i])):
                sublline = str(sublinksdb[i][ii])
                if strRange[1] == 0: # default ... complete string
                    if sublline[-1] == '\n':
                        f.write(sublline[strRange[0]:])
                    else:
                        f.write(sublline[strRange[0]:] + '\n')
                else:
                    f.write(sublline[strRange[0]:strRange[1]] + '\n')
    except:
        raise
        stat = -1

    return stat
