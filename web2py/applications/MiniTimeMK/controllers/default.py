# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################
import feedparser
from time import strftime
from bs4 import BeautifulSoup
from Queue import Queue
import urllib
import threading


def get_html(entry, queue):
    """
    Extracts the html of the page specified with url and puts it in a queue.
    Intended for parallelized usage.

    :param entry: The RSS Feed entry
    :param queue: The queue where to store the result
    """

    page_file = urllib.urlopen(entry.link.encode("utf-8"))
    entry_html = page_file.read()
    page_file.close()
    queue.put((entry, "".join(entry_html)))


def get_encoding(soup):
    ret = soup.meta.get('charset')
    if ret is None:
        ret = soup.meta.get('content-type')
        if ret is None:
            content = soup.meta.get('content')
            match = re.search('charset=(.*)', content)
            if match:
                ret = match.group(1)
            else:
                ret = "utf-8"
    return ret


def parse_feed_parallel(feed_options_item, all_links):
    """
    Parallel creation of a RSSItem for each post in the feed.

    :param feed_options_item: The RSS Feed options
    :param all_links: A set of all the links in the database
    :return: A list of RSSItems for each post
    """
    default_date = "2000-01-01 07:58:55"
    default_encoding = "utf-8"
    d = feedparser.parse(feed_options_item.feed_url)

    entries = Queue()   # Queue is thread-safe

    # Create a thread for each entry in the feed which is not present in the database
    # TODO: Limit number of threads to 5-10
    threads = []

    for entry in d.entries:
        if 'feedproxy.google' in entry.link:    # Feedproxy workaround
            if entry.get("feedburner_origlink", entry.link) not in all_links:
                threads.append(threading.Thread(target=get_html, args=(entry, entries)))
        else:
            if entry.link not in all_links:
                threads.append(threading.Thread(target=get_html, args=(entry, entries)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    res = []
    while not entries.empty():
        (entry, html) = entries.get_nowait()
        soup = BeautifulSoup(html)

        item_description = ""
        item_text = ""
        image_url = ""

        item_link = entry.link
        if 'feedproxy.google' in item_link:     # Feedproxy workaround
            item_link = entry.get("feedburner_origlink", item_link)

        item_pub_date = entry.get("published", default_date)   # default
        if item_pub_date != default_date:
            if entry.published_parsed is None or entry.published_parsed == "":
                item_pub_date = default_date
            else:
                # TODO: timezone adjustment
                item_pub_date = strftime("%Y-%m-%d %H:%M:%S", entry.published_parsed)

        # TODO: Workaround for Kanal5 missing publish date
        if feed_options_item.source_id == 1:
            pass

        if feed_options_item.item_rss_description:
            item_description = entry.description

        if feed_options_item.content_from_rss:
            item_text = entry[feed_options_item.content_rss_tag]
        else:
            selectors = feed_options_item.content_css_selector.split(",")
            for selector in selectors:
                content_entries = soup.select(selector)
                if len(content_entries) > 0:
                    for part in content_entries:
                        item_text += part.get_text() + " "

            if feed_options_item.recode:
                item_text = item_text.encode(soup.original_encoding, errors='ignore')
                item_text = item_text.decode(default_encoding, errors='ignore')

        if feed_options_item.image_from_rss:
            image_url = entry[feed_options_item.image_rss_tag]
        else:
            image_entries = soup.select(feed_options_item.image_css_selector)
            if len(image_entries) > 0:  # May not contain image
                image_url = image_entries[0]["src"]

        '''
        Regex cleaning here
        '''
        import re
        item_filtered_text = item_text.lower()
        for (regex_expr, output_fmt) in feed_options_item.clean_regex:
            item_filtered_text = re.sub(regex_expr, output_fmt, item_filtered_text)

        rss_post = RSSPost(page_url=item_link,
                           category=feed_options_item.category,
                           source=feed_options_item.source_id,
                           pub_date=item_pub_date,
                           item_title=entry.title,
                           item_content=item_text,
                           item_filtered_content=item_filtered_text,
                           item_description=item_description,
                           item_image_url=image_url)

        if not rss_post.db_insert():
            break   # If post is already present in database, stop

        res.append(rss_post)
    return res


def rss_extract_items(feeds_list):
    """
    Extracts the text from each RSS entry in each RSS feed in feeds_array
    and performs cleaning of interpunction signs and other HTML tags
    Feeds array should consists of RSSFeedOptions items.

    :param feeds_list: A list of RSSFeedOptions items
    :return: A list of RSSItem items.
    """

    all_dbrow_links = db().select(db.posts.link)    # List of Row objects containing the links
    raw_links = set([row.link for row in all_dbrow_links])  # Set of strings containing the links

    ret = []
    print 'Parallel fetch started', len(feeds_list), 'feeds'
    t1 = millis()
    for i, feed_options_item in enumerate(feeds_list):
        # print 'Extracting feed: ', feed_options_item.feed_url
        ret += (parse_feed_parallel(feed_options_item, raw_links))
    t2 = millis()
    print "Number of posts: %d" % len(ret)
    print "Parallel: feeds processed in %d ms" % (t2-t1)

    """
    ret = []
    print 'Sequential fetch started'
    t1 = millis()
    for feed_options_item in feeds_list:
        ret += (parse_feed_sequential(feed_options_item))
    t2 = millis()
    print(len(ret))
    print "Sequential: feeds processed in %d ms" % (t2-t1)
    """

    return ret


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    # Dynamically create a html page
    # test_create()
    # redirect(URL("index_generated"))

    # Selects zero or more occurrences of any interpunction sign in the set
    interpunction_regex = u'(?:\s|[,."\'`:;!@#$%^&*()_<>/=+„“”–\-\\\|\[\]])' + u'*'

    # Selects every sequence of one or more latin or cyrillic, lowercase or uppercase letter and any number
    word_regex = u'([A-Za-z0-9АБВГДЃЕЖЗЅИЈКЛЉМНЊОПРСТЌУФХЦЧЏШабвгдѓежзѕијклљмнњопрстќуфхцчџш]+)'

    words_extraction_regex = [(interpunction_regex + word_regex + interpunction_regex, r'\1 ')]

    feeds = []
    rows = db(db.sources.id == db.rssfeeds.source).select(db.rssfeeds.ALL, db.sources.ALL)
    for row in rows:
        feeds.append(RSSFeedOptions(feed_url=row.rssfeeds.feed,
                                    source_id=row.sources.id,
                                    content_css_selector=row.sources.contentselector,
                                    image_css_selector=row.sources.imageselector,
                                    category=row.rssfeeds.category,
                                    recode=row.rssfeeds.recode,
                                    clean_regex=words_extraction_regex))

    new_posts = rss_extract_items(feeds)
    new_clusters = clustering()

    response.flash = T("Welcome to miniTimeMK")
    return dict(message=T('Hello WORLD'),
                entries=new_clusters
                )


def index_generated():
    return dict(msg=T('HEY'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())



def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()



def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
