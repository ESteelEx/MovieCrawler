# # UI configuration file
# # define size and position of main window and all elements
#
########################################################################################################################
#                                               UI SEARCH SECTION
########################################################################################################################
# MAIN WINDOW
# ----------------------------------------------------------------------------------------------------------------------
WMAIN = {'title': 'Online search', 'pos': (500, 500), 'size': (700, 370)}
ICON = {'path': 'dat/images/', 'file': 'search.ico'}

# TEXT FIELDS
# ----------------------------------------------------------------------------------------------------------------------
THEADER = {'pos': (1, 10),  'size': (), 'label': 'Search with multiple strings separated by white space. Please note order. Preceding string decimates to available data base.'}

# EDIT FIELDS
# ----------------------------------------------------------------------------------------------------------------------
ESEARCH = {'pos': (1, 30),  'size': (691, 25)}

# LIST FIELDS
# ----------------------------------------------------------------------------------------------------------------------
LRESULT = {'pos': (2, 60),  'size': (691, 279)}

########################################################################################################################
#                                                   COLOR SECTION
########################################################################################################################
#
# GROUP COLORS
# ----------------------------------------------------------------------------------------------------------------------
WCOLOR = {'FG': (), 'BG': (90, 90, 90)}
TCOLOR = {'FG': (255, 255, 255), 'BG': ()}
ECOLOR = {'FG': (80, 80, 80), 'BG': (220, 220, 220)}
BCOLOR = {'FG': (80, 80, 80), 'BG': (220, 220, 220)}