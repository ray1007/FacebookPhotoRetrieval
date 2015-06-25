import os
import urllib
import shutil

def isChinese(str):
   if(str >= u'\u4e00' and str <= u'\u9fff'):
      return True
   else:
      return False

#

def dumpPhotos(graph, file_prefix, maxNum=-1):
    if maxNum < -1: maxNum=-1
    limitNum = 200
    photos_json = graph.get_connections(
        "me", "photos",
        fields="images,name", type="uploaded",
        offset=0, limit=limitNum)

	#photo_list = []
    count = 0
    # Create the corpus dir.
    if os.path.exists(file_prefix):
        shutil.rmtree(file_prefix)
    os.makedirs(file_prefix)
    photo_fetcher = urllib.URLopener()
    keep = True
    print("Fetching uploaded photos...")
    while(keep):
        nextPage = None
        if('next' in photos_json['paging']):
            nextPage = photos_json['paging']['cursors']['after']
        else:
            keep = False
        # Iterate over photos.
        for photo in photos_json['data'] :
            count += 1
            dir_name = '{0}/{1}'.format(file_prefix,count)
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
            os.mkdir(dir_name)
            if 'name' in photo: # Photo is annotated.
                with open('{0}/anno'.format(dir_name),'w') as f:
                    f.write(photo['name'].encode('utf-8'))
            for img in photo['images']:
                if 'p480x480' in img['source']:
                    photo_fetcher.retrieve(
                        img['source'],
                        "{0}/{1}.jpg".format(dir_name,count))
            if maxNum != -1 and count >= maxNum:
                keep = False
                break
        print("   processed {0} photos".format(count) )
        if(nextPage != None):
            friends_json = graph.get_connections(
			    "me", "photos",
                fields='images,name', type="uploaded",
                after=nextPage, offset=count, limit=200)
    print("Done!")

#

def dumpFriendlist(graph, filename):
   limitNum = 200
   friends_json = graph.get_connections("me", "invitable_friends",
                                        fields='first_name,last_name,name', locale='zh_TW',
                                        offset=0, limit=limitNum)
   friends_list = []
   with open(filename, "w") as f:
      count = 0
      keep = True
      print("Fetching friend names...")
      while(keep):
         nextPage = None
         if('next' in friends_json['paging']):
            nextPage = friends_json['paging']['cursors']['after']
         else:
            keep = False
         for friend in friends_json['data'] :
            if isChinese(friend['name']):
               f.write( "{0}\n".format(friend['name'].encode('utf-8')) )
               #f.write( "{0}\n".format(friend['first_name'].encode('utf-8')) )
         count += len(friends_json['data'])
         print("   processed {0} friends".format(count) )
         if(nextPage != None):
            friends_json = graph.get_connections("me", "invitable_friends",
                                                 fields='first_name,last_name,name', locale='zh_TW',
                                                 after=nextPage, offset=count, limit=200)
      print("Done!")

#

def dumpGrouplist(graph, filename):
   limitNum = 200
   groups_json = graph.get_connections("me", "groups",
                                        fields='name', locale='zh_TW',
                                        offset=0, limit=limitNum)
   groups_list = []
   with open(filename, "w") as f:
      count = 0
      keep = True
      print("Fetching group names...")
      while(keep):
         nextPage = None
         if('next' in groups_json['paging']):
            nextPage = groups_json['paging']['cursors']['after']
         else:
            keep = False
         for group in groups_json['data'] :
            if isChinese(group['name']):
#TODO separate the name with non-chinese character.
               f.write( "{0}\n".format(group['name'].encode('utf-8')) )
         count += len(groups_json['data'])
         print("   processed {0} groups".format(count) )
         if(nextPage != None):
            groups_json = graph.get_connections("me", "groups",
                                                 fields='name', locale='zh_TW',
                                                 after=nextPage, offset=count, limit=200)
      print("Done!")

#

