#!/usr/bin/python

import gdata.docs.data
import gdata.docs.client
import md5

# First get a client connection - using simple ClientLogin - should be OAuth in final version running in AppEngine

client = gdata.docs.client.DocsClient(source='gtugzh-pingini-v1')
client.ClientLogin('pingini1@gmail.com', 'xxxx', client.source);

# Print utility function

def PrintFeed(feed):
  print '\n'
  if not feed.entry:
    print 'No entries in feed.\n'
  for entry in feed.entry:
    print entry.title.text.encode('UTF-8'), entry.GetDocumentType(), entry.resource_id.text

    # List folders the document is in.
    for folder in entry.InFolders():
      print folder.title

# Utility to get the last part of a URL, usually useful as some sort of id:

def GetLastIdPart(entryWithId):
   id_parts = entryWithId.id.text.split('/')
   return id_parts[len(id_parts) - 1]

# Utility function to calculate a hex hash 

def GetMd5Hash(any_item):
   m = md5.new()
   m.update(any_item)
   return m.hexdigest()

# Utility to get an MD5 hash for a specific doc:

def GetHashOfCurrentPermissions(doc_resource_id):
    acl_feed = client.GetAclPermissions(doc_resource_id)
    aclentries = []
    for acl in acl_feed.entry:
      aclentry = '%s(%s)=%s' % (acl.scope.value, acl.scope.type, acl.role.value)
      aclentries.append(aclentry)
    return GetMd5Hash(''.join(aclentries))

# Utility to print out information on the latest revision based on document resource id

def PrintLastRevisionInfo(doc_resource_id):
   revisions_feed = client.GetRevisions(doc_resource_id)
   latest_entry = revisions_feed.entry[0]
   latest_revision_id = GetLastIdPart(latest_entry)
   last_update = latest_entry.updated.text
   last_authorname = latest_entry.author[0].name.text

   print (latest_revision_id)
   print (last_update)
   print (last_authorname)

# Utility function get a list of all revision ids for a document:

def GetListOfRevisions(doc_resource_id):
     revision_list = []
     for entry in client.GetRevisions(doc_resource_id).entry:
       revision_list.append(GetLastIdPart(entry))
     return revision_list

##### 

# Get a list of documents for the current user based on a last edited time:

feed = client.GetDocList("https://docs.google.com/feeds/default/private/full?edited-min=2011-08-23T19:00:00-01:00")

# For all documents just use GetDocList()
# feed = client.GetDocList()

PrintLastRevisionInfo(feed.entry[0].resource_id.text)

print (GetListOfRevisions(feed.entry[0].resource_id.text))

print(GetHashOfCurrentPermissions(feed.entry[0].resource_id.text))

