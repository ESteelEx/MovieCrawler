#!/usr/bin/python

import wx, os
from wx.lib.agw import ultimatelistctrl as ULC
import UI.SearchRevision.searchUI as UIP

#-----------------------------------------------------------------------------------------------------------------------
def getConfigData(configfile, boolCrypt=True):
    import xml.etree.ElementTree as ET
    from vardef import serverdata
    from Crypt.mrcrypto import AESCipher

    tree = ET.parse(configfile)
    root = tree.getroot()

    for server in root.findall('server'):
        serverdata.name = server.get('name')
        serverdata.url = server.find('url').text
        if boolCrypt:
            serverdata.user = server.find('user').text
            serverdata.passw = server.find('pass').text

    if boolCrypt:
        #decrypt information
        Cipher = AESCipher()
        try:
            serverdata.user = Cipher.decrypt(serverdata.user)
            serverdata.passw = Cipher.decrypt(serverdata.passw)
            serverDataDC = serverdata #save decrypted information in a global var to bypass decryption routine (time saving)
        except:
            raise
            #wx.MessageDialog(None, 'Failed to receive settings information. Proof settings', 'Crypt Error', wx.OK | wx.ICON_INFORMATION).ShowModal()

    for storage in root.findall('storage'):
        storage.name = storage.get('name')
        storage.extracted = storage.find('extracted').text
        storage.zipfiles = storage.find('zipfiles').text

    if storage.extracted == None:
        storage.extracted = ''
        storage.zipfiles = ''

    return serverdata, storage


# ----------------------------------------------------------------------------------------------------------------------
def httpReader(serverdata):
    import urllib2

    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, serverdata.url, serverdata.user, serverdata.passw)
    urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))

    req = urllib2.Request(serverdata.url)

    try:
        f = urllib2.urlopen(req)
        data = f.read()
    except:
        raise

    return data

# ----------------------------------------------------------------------------------------------------------------------
def eraseifnot(linkdb, command='num'):

    if command == 'num':

        # proof if we read valid date format
        while 1:
            for i in range(len(linkdb)):
                try:
                    link = str(linkdb[i])
                    int(link[2:6])   # if conversion fails str isn't a number in char
                except:
                    del linkdb[i]  # kill entry
                    break
            if i == len(linkdb):
                break

    else:
        # proof if we read valid date format
        while 1:
            for i in range(len(linkdb)):
                link = str(linkdb[i])
                if link.find(command) == -1:
                    del linkdb[i] # kill entry
                    break

            if i == len(linkdb)-1:
                break

    return linkdb

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
class searchdialog(wx.Dialog):
    def __init__(self, parent, configfile):
        global exitStat
        import UI.SearchRevision.realtimesearch

        exitStat = False

        wx.Dialog.__init__(self, parent, title=UIP.WMAIN['title'], size=(UIP.WMAIN['size'][0], 100),
                           style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
                                 | wx.TAB_TRAVERSAL | wx.STAY_ON_TOP)

        self.userData = getConfigData(configfile)

        self.SetBackgroundColour(wx.Colour(UIP.WCOLOR['BG'][0], UIP.WCOLOR['BG'][1], UIP.WCOLOR['BG'][2]))
        self.Centre()

        atable = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_ESCAPE, wx.ID_EXIT)])
        self.SetAcceleratorTable(atable)
        wx.EVT_MENU(self, wx.ID_EXIT, self.OnExit)

        # read from file
        # fname = '../../dat/sublinksdb.dat'
        fname = 'dat/sublinksdb.dat'
        with open(fname) as ff:
            sublinksdb = ff.readlines()

        self.sublinksdb = sublinksdb
        self.RTS = UI.SearchRevision.realtimesearch.onlinesearch()

        ficon = UIP.ICON['path'] + UIP.ICON['file']
        self.icon = wx.Icon(ficon, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

        text1 = wx.StaticText(self, label=UIP.THEADER['label'], pos=UIP.THEADER['pos'])

        text1.SetForegroundColour(UIP.TCOLOR['FG']) # set text color
        text1.SetFont(font)

        self.searchf = wx.TextCtrl(self, value='', pos=UIP.ESEARCH['pos'], size=UIP.ESEARCH['size'],
                                   style=wx.TE_PROCESS_ENTER)

        self.searchf.SetForegroundColour(UIP.ECOLOR['FG']) # set color

        self.searchf.Bind(wx.EVT_TEXT, self.EvtText)

        self.listCtrl = wx.ListCtrl(self, pos=UIP.LRESULT['pos'], size=UIP.LRESULT['size'], style=wx.LC_REPORT |
                                                                                                  wx.LC_SINGLE_SEL |
                                                                                                  wx.NO_BORDER) # | wx.BORDER_SUNKEN)
        self.listCtrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.EvtList)
        self.listCtrl.SetForegroundColour(UIP.TCOLOR['FG']) # set text color
        self.listCtrl.SetBackgroundColour(UIP.WCOLOR['BG']) # set text color

        sw = wx.ScrolledWindow(self.listCtrl)
        for child in sw.GetChildren():
            if isinstance(child, wx.ScrollBar):
                print child
                # child.SetBackgroundColour(...)

    # ------------------------------------------------------------------------------------------------------------------
    def EvtText(self, event):
        try:
            self.listCtrl.DeleteAllItems()
            if len(event.GetString()) != 0:
                # revisionNumber = int(event.GetString())
                searchString = event.GetString()
                # searchResult = self.RTS.getByRevisionNumber(self.sublinksdb, revisionNumber)
                self.searchResult = self.RTS.getByString(self.sublinksdb, searchString)
                try:
                    self.listCtrl.DeleteColumn(0)
                except:
                    pass

                self.SetSizeWH(UIP.WMAIN['size'][0], UIP.WMAIN['size'][1])
                self.listCtrl.InsertColumn(0, "Result(s): " + str(len(self.searchResult)), width=630)
                # self.listCtrl.SetAlternateRowColour((90, 90, 90))

                # insert search Results in list
                storagePath = self.userData[1].zipfiles#.replace('\\', '/')
                for i in reversed(range(len(self.searchResult))):
                    self.listCtrl.InsertStringItem(0, self.searchResult[i])
                    if os.path.isfile(storagePath + "\\download\\" + self.searchResult[i][:-1]):
                        self.listCtrl.SetItemTextColour(0, (140, 140, 140))

            else:
                try:
                    self.SetSizeWH(UIP.WMAIN['size'][0], 100)
                    self.listCtrl.DeleteColumn(0)
                except:
                    pass

        except:
            editStr = event.GetString()
            self.searchf.SetValue(editStr[:-1])
            self.searchf.SetInsertionPoint(len(self.searchf.GetValue()))

    # ------------------------------------------------------------------------------------------------------------------
    def EvtList(self, event):
        global listValue
        global dailyDate
        global exitStat
        import UI.SearchRevision.datemanager as DM
        listValue = self.searchResult[self.listCtrl.GetFocusedItem()]
        listValue = listValue[:-1] # kill the next line /n
        dailyDate = DM.extractDateFromDFName(listValue)
        # self.sublinksdb[self.listCtrl.GetFocusedItem()]
        self.Destroy()

    # ------------------------------------------------------------------------------------------------------------------
    def OnExit(self, event):
        global listValue
        global dailyDate
        global exitStat
        listValue = None
        dailyDate = None
        exitStat = True
        self.Destroy()

# ----------------------------------------------------------------------------------------------------------------------
def openSD(configfile):
    sdialog = searchdialog(None, configfile)
    sdialog.ShowModal()
    return exitStat, listValue, dailyDate

# ----------------------------------------------------------------------------------------------------------------------
def main(configfile='../../dat/config.ini'):
    app = wx.App(False)
    openSD(configfile)
    print listValue

if __name__ == '__main__':
    main()