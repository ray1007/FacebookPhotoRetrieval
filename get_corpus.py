#!/usr/bin/env python
from login import *
from fb_util  import *

def execute():
    token = login()

    graph = facebook.GraphAPI(token)
    profile = graph.get_object("me")
    permissions = graph.get_connections("me", "permissions")
    permission_list = [p['permission'] for p in permissions['data']]
   
    # Get friends (in util.py)
    #dumpFriendlist(graph, "friends.txt") 

    # Get groups (in util.py)
    #dumpGrouplist(graph, "groups.txt")

	# Get uploaded photos	
    dumpPhotos(graph, "my_photo_corpus_uploaded",5000)

if __name__=="__main__":
   execute()
