# -*- coding: utf-8 -*-

from facebook import GraphAPI as GraphAPIBase
from facebook import GraphAPIError
import subprocess
import urllib
import re
import sys

token = 'YOUR_ACCESS_TOKEN_HERE'

if __name__ == '__main__':

    if len(sys.argv) == 1:
        print "자동 재생할 페이스북 그룹 주소를 입력해주세요."
        print "ex) python player.py rarelylive [ID]"
        exit(1)

    if len(sys.argv) == 3:
        lastest_feed_id = sys.argv[2]
    else:
        lastest_feed_id = None

    facebookId = sys.argv[1]
    graph = GraphAPIBase(token)

    while True:
        if lastest_feed_id is None:
            feeds = graph.get_connections(facebookId, 'feed',
                                          fields='source,message',
                                          type='video',
                                          limit='1')
        else:
            feeds = graph.get_connections(facebookId, 'feed',
                                          fields='source,message',
                                          type='video',
                                          until=lastest_feed_id,
                                          limit='1')

        lastest_feed_id = None
        for feed in feeds['data']:
            lastest_feed_id = feed['id'].encode('utf-8')

            if 'message' not in feed:
                continue
            if 'source' not in feed:
                continue
            
            print '* Downloading... "' + re.compile('[^\n]+').search(feed['message'].encode('utf-8')).group(0) + '"'
            urllib.urlretrieve(feed['source'], "music.cache")
            print '* Play!'
            subprocess.call(['afplay','music.cache'])
            print ''

        if lastest_feed_id is None:
            break
        else:
            lastest_feed_id = re.compile('until=[0-9]+').search(feeds['paging']['next'].encode('utf-8')).group(0)[6:]
            print '* ID: ' + lastest_feed_id