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


def insert_post(link, category, source, title, item_filtered_text, item_description, image_url, pubdate):
    post = Post(link, category, source, title, item_filtered_text, item_description, image_url, pubdate)
    return post.db_insert()


def parse_feed_parallel(feed_options_item):
    """
    Parallel creation of a RSSItem for each post in the feed.

    :param feed_options_item: The RSS Feed options
    :return: A list of RSSItems for each post
    """
    d = feedparser.parse(feed_options_item.feed_url)
    print 'Extracting feed: ', feed_options_item.feed_url

    entries = Queue()   # Queue is thread-safe
    # Create a thread for each entry in the feed
    threads = [threading.Thread(target=get_html, args=(entry, entries)) for entry in d.entries]
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
        item_pub_date = entry.get("published", "Sat, 01 Jan 2000 07:58:55 +0000")   # default

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

        if feed_options_item.image_from_rss:
            image_url = entry[feed_options_item.image_rss_tag]
        else:
            image_entries = soup.select(feed_options_item.image_css_selector)
            if len(image_entries) > 0:  # May not contain image
                image_url = image_entries[0]["src"]

        # Regex cleaning here
        import re
        item_filtered_text = item_text.lower().encode("utf-8")  # Encoding a string makes a special string
        for (regex_expr, output_fmt) in feed_options_item.clean_regex:
            item_filtered_text = re.sub(regex_expr, output_fmt, item_filtered_text)

        rss_item = RSSItem(entry.link, feed_options_item.category, item_pub_date,
                           entry.title, item_text, item_filtered_text, item_description, image_url)

        if not insert_post(entry.link, feed_options_item.category,
                           feed_options_item.source_id, entry.title, rss_item.item_filtered_content,
                           rss_item.item_description, rss_item.item_image_url, item_pub_date):
            break   # If post is already present in database, stop iterating the feed

        res.append(rss_item)
    return res


def rss_extract_items(feeds_list):
    """
    Extracts the text from each RSS entry in each RSS feed in feeds_array
    and performs cleaning of interpunction signs and other HTML tags
    Feeds array should consists of RSSFeedOptions items.

    :param feeds_list: A list of RSSFeedOptions items
    :return: A list of RSSItem items.
    """

    ret = []
    print 'Parallel fetch started'
    t1 = millis()
    for feed_options_item in feeds_list:
        ret += (parse_feed_parallel(feed_options_item))
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
    interpunction_regex = r'(?:\s|[,."\'`:;!@#$%^&*()_<>/=+„“–\-\\\|\[\]])' + '*'

    # Selects every sequence of one or more latin or cyrillic, lowercase or uppercase letter and any number
    word_regex = r'([A-Za-z0-9АБВГДЃЕЖЗЅИЈКЛЉМНЊОПРСТЌУФХЦЧЏШабвгдѓежзѕијклљмнњопрстќуфхцчџш]+)'

    words_extraction_regex = [(interpunction_regex + word_regex + interpunction_regex, r'\1 ')]

    feeds = []
    rows = db(db.sources.id == db.rssfeeds.source).select(db.rssfeeds.ALL, db.sources.ALL)
    for row in rows:
        feeds.append(RSSFeedOptions(row.rssfeeds.feed, source_id=row.sources.id,
                                    content_css_selector=row.sources.contentselector,
                                    image_css_selector=row.sources.imageselector,
                                    category=row.rssfeeds.category,
                                    clean_regex=words_extraction_regex))

    # clustering()

    new_posts = rss_extract_items(feeds)
    # post = Post.getPost(39)
    # print(post.id)

    response.flash = T("Welcome to miniTimeMK")
    return dict(message=T('Hello WORLD'),
                entries=db((db.posts.source == db.rssfeeds.source) & (db.posts.category == db.rssfeeds.category)).select(db.posts.ALL)
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
