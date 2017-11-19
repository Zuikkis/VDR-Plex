# VDR Recording Scanner
#
# Source:
# https://forums.plexapp.com/index.php/topic/86990-scanner-for-vdr-recordings/
#
# Copyright: Friedhelm Buescher 2013
#            Teemu Suikki 2017

import re, os, os.path, sys, datetime
import Media, VideoFiles, unicodedata, Stack

import logging

def Scan(path, files, mediaList, subdirs):

  #logging.basicConfig(filename='/tmp/vdrscanner.log',level=logging.DEBUG)

  if len(files) >= 1:

    # Iterate through all the files
    for file in files:
      if (file.endswith("/info")):
        dir = os.path.dirname(file)
        infoFile = open(file).read()

        title = re.search('^T (.*)$', infoFile,re.M)

        # accepted formats for Episode 3 of season 1, episode name "epname"
        # (3:22) epname
        # (3:22/s1) epname
        # (Ep 3:22) epname
        # (Ep 3:22/s1) epname
        # (Ep. 3:22) epname
        # (Ep. 3:22/s1) epname
        #      
        # Both S and D lines are scanned.
        episode = re.search('^(?:S|D) \((?:Ep\.|Ep)?\s*(\d+)(?:\:\d+)?(?:\/s(\d+))?\)\.\s+(.*)$', infoFile, re.M)

        if episode and title:
            tvshow = True
        else:
            tvshow = False

        # some shows that lack episode info for some reason
        forceshow = re.search('^T (Ren and Stimpy|Die Ren & Stimpy Show|Simpsonit)', infoFile, re.M)
        if forceshow and title:
            tvshow = True
 
        if not tvshow:
	    if title:
                title = title.groups(1)[0]
            else:
                title = "Unknown"

            #logging.debug('Title : %s' %title)

	    movie = Media.Movie(title)

            for ts_filename in sorted(os.listdir(dir)):
                if (ts_filename.endswith(".ts")):
                    if (ts_filename.endswith("00001.ts")):
                        movie.source = VideoFiles.RetrieveSource(dir+"/"+ts_filename)
                    movie.parts.append(dir+"/"+ts_filename)

	    if len(movie.parts)>0:
    	        mediaList.append(movie)

