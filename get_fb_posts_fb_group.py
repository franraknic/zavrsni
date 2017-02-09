import urllib2
import json
import datetime
import time
import sqlite3

#facebook group ids
itjobs = "1470658223200432"
sistemci = "765704940137092"
devhr = "153381991366459"


app_id = "552403108264856"
app_secret = "2f6b44a768bc209cac2c492fc180a7b8" # DO NOT SHARE WITH ANYONE!
group_id = itjobs

access_token = app_id + "|" + app_secret

def request_until_succeed(url):
    req = urllib2.Request(url)
    success = False
    while success is False:
        try: 
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception:
            print(Exception)
            time.sleep(5)

            print( "Error for URL %s: %s" % (url, datetime.datetime.now()))
            print("Retrying.")

    return response.read()


def getFacebookPageFeedData(group_id, access_token, num_statuses):

    # Construct the URL string; see 
    # http://stackoverflow.com/a/37239851 for Reactions parameters
    base = "https://graph.facebook.com/v2.6"
    node = "/%s/feed" % group_id 
    fields = "/?fields=message,link,created_time,type,name,id," + \
            "comments.limit(0).summary(true),shares,reactions." + \
            "limit(0).summary(true),from"
    parameters = "&limit=%s&access_token=%s" % (num_statuses, access_token)
    url = base + node + fields + parameters

    # retrieve data
    data = json.loads(request_until_succeed(url))

    return data

def getReactionsForStatus(status_id, access_token):

    # See http://stackoverflow.com/a/37239851 for Reactions parameters
        # Reactions are only accessable at a single-post endpoint

    base = "https://graph.facebook.com/v2.6"
    node = "/%s" % status_id
    reactions = "/?fields=" \
            "reactions.type(LIKE).limit(0).summary(total_count).as(like)" \
            ",reactions.type(LOVE).limit(0).summary(total_count).as(love)" \
            ",reactions.type(WOW).limit(0).summary(total_count).as(wow)" \
            ",reactions.type(HAHA).limit(0).summary(total_count).as(haha)" \
            ",reactions.type(SAD).limit(0).summary(total_count).as(sad)" \
            ",reactions.type(ANGRY).limit(0).summary(total_count).as(angry)"
    parameters = "&access_token=%s" % access_token
    url = base + node + reactions + parameters

    # retrieve data
    data = json.loads(request_until_succeed(url))

    return data


def processFacebookPageFeedStatus(status, access_token):

    # The status is now a Python dictionary, so for top-level items,
    # we can simply call the key.

    # Additionally, some items may not always exist,
    # so must check for existence first

    status_id = status['id']
    status_message = '' if 'message' not in status.keys() else \
            (status['message'])
    link_name = '' if 'name' not in status.keys() else \
            (status['name'])
    status_type = status['type']
    status_link = '' if 'link' not in status.keys() else \
            (status['link'])
    status_author = (status['from']['name'])

    # Time needs special care since a) it's in UTC and
    # b) it's not easy to use in statistical programs.

    status_published = datetime.datetime.strptime(\
            status['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
    status_published = status_published + datetime.timedelta(hours=-5) # EST
    # best time format for spreadsheet programs:
    status_published = status_published.strftime('%Y-%m-%d %H:%M:%S')

    # Nested items require chaining dictionary keys.

    num_reactions = 0 if 'reactions' not in status else \
            status['reactions']['summary']['total_count']
    num_comments = 0 if 'comments' not in status else \
            status['comments']['summary']['total_count']
    num_shares = 0 if 'shares' not in status else \
            status['shares']['count']

    # Counts of each reaction separately; good for sentiment
    # Only check for reactions if past date of implementation:
    # http://newsroom.fb.com/news/2016/02/reactions-now-available-globally/

    reactions = getReactionsForStatus(status_id, access_token) \
            if status_published > '2016-02-24 00:00:00' else {}

    num_likes = 0 if 'like' not in reactions else \
            reactions['like']['summary']['total_count']

    # Special case: Set number of Likes to Number of reactions for pre-reaction
    # statuses

    num_likes = num_reactions if status_published < '2016-02-24 00:00:00' else \
            num_likes

    def get_num_total_reactions(reaction_type, reactions):
        if reaction_type not in reactions:
            return 0
        else:
            return reactions[reaction_type]['summary']['total_count']

    num_loves = get_num_total_reactions('love', reactions)
    num_wows = get_num_total_reactions('wow', reactions)
    num_hahas = get_num_total_reactions('haha', reactions)
    num_sads = get_num_total_reactions('sad', reactions)
    num_angrys = get_num_total_reactions('angry', reactions)

    # return a tuple of all processed data
    '''
    return (status_id, status_message, status_author, link_name, status_type, 
            status_link, status_published, num_reactions, num_comments, 
            num_shares,  num_likes, num_loves, num_wows, num_hahas, num_sads, 
            num_angrys)
    '''
    return (None, status_message, status_id, status_published, 'IT Jobs FB')

def scrapeFacebookPageFeedStatus(group_id, access_token):

    con = sqlite3.connect('data.db')
    c = con.cursor()

    has_next_page = True
    num_processed = 0   # keep a count on how many we've processed
    num_stored = 1
    scrape_starttime = datetime.datetime.now()

    print("Scraping %s Facebook Page: %s\n" % \
            (group_id, scrape_starttime))

    statuses = getFacebookPageFeedData(group_id, access_token, 100)

    while has_next_page:
        for status in statuses['data']:

            # Ensure it is a status with the expected metadata
            if 'reactions' in status:
                fb_post = processFacebookPageFeedStatus(status, access_token)
                c.execute("SELECT count(mydata.post_link) FROM mydata WHERE mydata.post_link = '" + fb_post[2] + "'")
                exists = c.fetchone()
                if not exists:

                    fb_post = [(fb_post[0], fb_post[1], fb_post[2], fb_post[3], fb_post[4])]

                    c.executemany('INSERT INTO mydata VALUES (?,?,?,?,?)', fb_post)
                    num_stored += 1
                    con.commit()

            # output progress occasionally to make sure code is not
            num_processed += 1
            if num_processed % 100 == 0:
                print("%s Statuses Processed: %s" % (num_processed,
                        datetime.datetime.now()))
            if num_stored % 100 == 0:
                print( "Statuses Stored: %s" % num_stored)

        # if there is no next page, we're done.
        if 'paging' in statuses.keys():
            statuses = json.loads(request_until_succeed(\
                    statuses['paging']['next']))
        else:
            has_next_page = False


    print ("\nDone!\n%s Statuses Processed in %s" % \
            (num_processed, datetime.datetime.now() - scrape_starttime))


if __name__ == '__main__':
    scrapeFacebookPageFeedStatus(group_id, access_token)


# The CSV can be opened in all major statistical programs. Have fun! :)
