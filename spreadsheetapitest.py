#!/usr/bin/python

#### Example used as starting point : http://gdata-python-client.googlecode.com/hg/samples/spreadsheets/spreadsheetExample.py

import gdata.spreadsheet.service
import gdata.service
import atom.service
import gdata.spreadsheet

gd_client = gdata.spreadsheet.service.SpreadsheetsService()
gd_client.email = 'pingini1@gmail.com'
gd_client.password = 'xxxx'
gd_client.ProgrammaticLogin()

# Utility function to print some feed information:

def _PrintFeed(feed):
  for i, entry in enumerate(feed.entry):
    if isinstance(feed, gdata.spreadsheet.SpreadsheetsCellsFeed):
      print '%s %s\n' % (entry.title.text, entry.content.text)
    elif isinstance(feed, gdata.spreadsheet.SpreadsheetsListFeed):
      print '%s %s %s' % (i, entry.title.text, entry.content.text)
      # Print this row's value for each column (the custom dictionary is
      # built using the gsx: elements in the entry.)
      print 'Contents:'
      for key in entry.custom:  
        print '  %s: %s' % (key, entry.custom[key].text) 
      print '\n',
    else:
      print '%s %s\n' % (i, entry.title.text)

# Utility to get the last part of a URL, usually useful as some sort of id:

def GetLastIdPart(entryWithId):
   id_parts = entryWithId.id.text.split('/')
   return id_parts[len(id_parts) - 1]


# Finds the first spreadsheets in the list of all spreadsheets:

sfeed = gd_client.GetSpreadsheetsFeed()
#_PrintFeed(sfeed)
curr_key = GetLastIdPart(sfeed.entry[0])

# Finds the first spreadsheet tab in the list of all tabs of the spreadsheet:

wsfeed = gd_client.GetWorksheetsFeed(curr_key)
ws_key = GetLastIdPart(wsfeed.entry[0])

# Returns a list feed of all non-title rows in the spreadsheet and prints out the count of the entries:
listfeed = gd_client.GetListFeed(curr_key, ws_key)
print len(listfeed.entry)

