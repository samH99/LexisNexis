"""
Update feeds for Django community page.  Requires Mark Pilgrim's excellent
Universal Feed Parser (http://feedparser.org)
"""

import os
import sys
import time
import optparse
import datetime
import feedparser

sys.path.insert(0,'/home/mloss/django/')
sys.path.insert(0,'/home/mloss/django/mloss/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'mloss.settings'

def update_feeds():
    from aggregator.models import Feed, FeedItem
    for feed in Feed.objects.filter(is_defunct=False):
        parsed_feed = feedparser.parse(feed.feed_url)
        print 'Reading ' + feed.title + ' with ' + str(len(parsed_feed.entries)) + ' entries.'
        if len(parsed_feed.entries) == 0:
            print 'No feed entries found, error is...'
            print parsed_feed.bozo_exception
        for entry in parsed_feed.entries:
            title = entry.title.encode(parsed_feed.encoding, "xmlcharrefreplace")
            print 'Updating ' + title
            guid = entry.get("id", entry.link).encode(parsed_feed.encoding, "xmlcharrefreplace")
            link = entry.link.encode(parsed_feed.encoding, "xmlcharrefreplace")

            if not guid:
                guid = link

            if hasattr(entry, "summary"):
                content = entry.summary
            elif hasattr(entry, "content"):
                content = entry.content[0].value
            elif hasattr(entry, "description"):
                content = entry.description
            else:
                content = u""
            content = content.encode(parsed_feed.encoding, "xmlcharrefreplace")

            try:
                if entry.has_key('modified_parsed'):
                    date_modified = datetime.datetime.fromtimestamp(time.mktime(entry.modified_parsed))
                elif parsed_feed.feed.has_key('modified_parsed'):
                    date_modified = datetime.datetime.fromtimestamp(time.mktime(parsed_feed.feed.modified_parsed))
                elif parsed_feed.has_key('modified'):
                    date_modified = datetime.datetime.fromtimestamp(time.mktime(parsed_feed.modified))
                else:
                    date_modified = datetime.datetime.now()
            except TypeError:
                date_modified = datetime.datetime.now()

            try:
                feed.feeditem_set.get(guid=guid)
            except FeedItem.DoesNotExist:
                feed.feeditem_set.create(title=title[:200], link=link, summary=content, guid=guid, date_modified=date_modified)

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--settings')
    options, args = parser.parse_args()
    if options.settings:
        os.environ["DJANGO_SETTINGS_MODULE"] = options.settings
    update_feeds()
