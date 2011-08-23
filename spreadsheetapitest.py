#!/usr/bin/python

import gdata.spreadsheet.service
import gdata.service
import atom.service
import gdata.spreadsheet

gd_client = gdata.spreadsheet.service.SpreadsheetsService()
gd_client.email = 'pingini1@gmail.com'
gd_client.password = 'xxxx'
gd_client.ProgrammaticLogin()

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

sfeed = gd_client.GetSpreadsheetsFeed()
#_PrintFeed(sfeed)
id_parts = sfeed.entry[0].id.text.split('/')
curr_key = id_parts[len(id_parts) - 1]

wsfeed = gd_client.GetWorksheetsFeed(curr_key)
ws_parts = wsfeed.entry[0].id.text.split('/')
ws_key = ws_parts[len(ws_parts) - 1]

listfeed = gd_client.GetListFeed(curr_key, ws_key)
print len(listfeed.entry)




