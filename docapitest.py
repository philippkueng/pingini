#!/usr/bin/python

import gdata.docs.data
import gdata.docs.client
import md5

client = gdata.docs.client.DocsClient(source='gtugzh-pingini-v1')
client.ClientLogin('pingini1@gmail.com', 'xxx', client.source);


def PrintFeed(feed):
  print '\n'
  if not feed.entry:
    print 'No entries in feed.\n'
  for entry in feed.entry:
    print entry.title.text.encode('UTF-8'), entry.GetDocumentType(), entry.resource_id.text

    # List folders the document is in.
    for folder in entry.InFolders():
      print folder.title

def GetLastIdPart(entryWithId):
   id_parts = entryWithId.id.text.split('/')
   return id_parts[len(id_parts) - 1]

def GetMd5Hash(any_item):
   m = md5.new()
   m.update(any_item)
   return m.hexdigest()

feed = client.GetDocList("https://docs.google.com/feeds/default/private/full?edited-min=2011-08-23T19:00:00-01:00")

revisions_feed = client.GetRevisions(feed.entry[0].resource_id.text)
latest_entry = revisions_feed.entry[0]
latest_revision_id = GetLastIdPart(latest_entry)
last_update = latest_entry.updated.text
last_authorname = latest_entry.author[0].name.text

print(latest_revision_id)
print(last_update)
print(last_authorname)

# Get a list of all revision ids for a document:

def GetListOfRevisions(resource_id):
     revision_list = []
     for entry in client.GetRevisions(resource_id).entry:
       revision_list.append(GetLastIdPart(entry))
     return revision_list
     
print (GetListOfRevisions(feed.entry[0].resource_id.text))

print(revisions_feed.entry[1])

acl_feed = client.GetAclPermissions(feed.entry[0].resource_id.text)
aclentries = []
for acl in acl_feed.entry:
  aclentry = '%s(%s)=%s' % (acl.scope.value, acl.scope.type, acl.role.value)
  aclentries.append(aclentry)

print(aclentries)

print(GetMd5Hash(''.join(aclentries)))

