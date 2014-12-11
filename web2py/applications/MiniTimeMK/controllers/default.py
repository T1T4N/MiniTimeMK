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
import urllib


def get_html_soup(url):
    """Extracts the html of the page specified with url
    and returns a BeautifulSoup object"""
    page_file = urllib.urlopen(url.encode("utf-8"))
    entry_html = page_file.read()
    page_file.close()
    return BeautifulSoup("".join(entry_html))


def insert_post(link, category, source, title, item_filtered_text, item_description, image_url):
    db.posts.insert(link=link, category=category, source=source, title=title, text=item_filtered_text, description=item_description, imageurl=image_url)


def parse_item(feed_options_item):
    d = feedparser.parse(feed_options_item.feed_url)

    # Take only the first 2 elements for speed...debug purposes :)
    ret = []
    for entry in d.entries[:3]:

        soup = get_html_soup(entry.link)
        #entry_html = urllib.urlopen(entry.link).read()
        #soup = BeautifulSoup("".join(entry_html))
        # print(soup.prettify(encoding="utf-8"))

        item_description = ""
        item_text = ""
        image_url = ""

        if feed_options_item.item_rss_description:
            item_description = entry.description

        if feed_options_item.content_from_rss:
            item_text = entry[feed_options_item.content_rss_tag]
        else:
            content_entries = soup.select(feed_options_item.content_css_selector)
            if len(content_entries) > 0:
                item_text = content_entries[0].get_text()

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

        rss_item = RSSItem(entry.link, feed_options_item.category,
                           entry.title, item_text, item_filtered_text, item_description, image_url)

        #TODO: inserting into database
        insert_post(entry.link, feed_options_item.category, '1',
                    entry.title, item_filtered_text, item_description, image_url)

        ret.append(rss_item)
    return ret


def millis():
    import time
    return int(round(time.time() * 1000))


def rss_extract_items(feeds_list):
    """
    Extracts the text from each RSS entry in each RSS feed in feeds_array
    and performs cleaning of interpunction signs and other HTML tags
    Feeds array should consists of RSSFeedOptions items.

    :param feeds_list: A list of RSSFeedOptions items
    :return: A list of RSSItem items.
    """
    ret = []
    t1 = millis()
    for feed_options_item in feeds_list:
        ret += (parse_item(feed_options_item))
    t2 = millis()
    print(len(ret))
    print("Sequential took %f millis", t2-t1)
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
    interpunction_regex = r'(?:\s|[,."\':;!@#$%^&*()_<>/=+„“–\-\\\|\[\]])' + '*'

    # Selects every sequence of one or more latin or cyrillic, lowercase or uppercase letter and any number
    word_regex = r'([A-Za-z0-9АБВГДЃЕЖЗЅИЈКЛЉМНЊОПРСТЌУФХЦЧЏШабвгдѓежзѕијклљмнњопрстќуфхцчџш]+)'

    words_extraction_regex = [(interpunction_regex + word_regex + interpunction_regex, r'\1 ')]

    # feeds = []
    # for row in db((db.sources.id==db.rssfeeds.source) & (db.rssfeeds.category == 1) & (db.rssfeeds.source == 1) | (db.rssfeeds.source == 4)).select(db.rssfeeds.ALL, db.sources.ALL):
    #     feeds.append(RSSFeedOptions(row.rssfeeds.feed,
    #                         content_css_selector=row.sources.contentselector,
    #                         image_css_selector=row.sources.imageselector,
    #                         category=row.rssfeeds.category,
    #                         clean_regex=words_extraction_regex))



    feeds = [RSSFeedOptions("http://kanal5.com.mk/rss/vestixml-makedonija.asp",
                            content_css_selector="div.entry div:nth-of-type(4)",
                            image_css_selector="div.entry div.frame_box img",
                            category="1",
                            clean_regex=words_extraction_regex),
             RSSFeedOptions("http://www.plusinfo.mk/rss/svet",
                            content_css_selector="div.glavna_text",
                            image_css_selector="#MainContent_imgVest",
                            category="5",
                            clean_regex=words_extraction_regex)]

    ret = rss_extract_items(feeds)

    # for row in db((db.posts.source==db.rssfeeds.source) & (db.posts.category==db.rssfeeds.category)).select(db.posts.ALL):
    #     print row.title
    response.flash = T("Welcome to miniTimeMK")
    return dict(message=T('Hello WORLD'),
                entries=ret
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


@cache.action()
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


@auth.requires_login() 
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
