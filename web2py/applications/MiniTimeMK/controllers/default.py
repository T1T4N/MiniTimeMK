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
    page_file = urllib.urlopen(url)
    entry_html = page_file.read()
    page_file.close()
    return BeautifulSoup("".join(entry_html))


def rss_extract_items(feeds_list):
    """
    Extracts the text from each RSS entry in each RSS feed in feeds_array
    and performs cleaning of interpunction signs and other HTML tags
    Feeds array should consists of RSSFeedOptions items.

    :param feeds_list: A list of RSSFeedOptions items
    :return: A list of RSSItem items.
    """
    ret = []
    for feed_options_item in feeds_list:
        d = feedparser.parse(feed_options_item.feed_url)

        # Take only the first 2 elements for speed...debug purposes :)
        for entry in d.entries[:2]:
            soup = get_html_soup(entry.link)
            # print(soup.prettify(encoding="utf-8"))

            if feed_options_item.item_rss_description:
                item_description = entry.description
            else:
                item_description = ""

            if feed_options_item.content_from_rss:
                item_text = entry[feed_options_item.content_rss_tag]
            else:
                content_entries = soup.select(feed_options_item.content_css_selector)
                # if len(content_entries) > 0:
                item_text = content_entries[0].get_text()

            if feed_options_item.image_from_rss:
                image_url = entry[feed_options_item.image_rss_tag]
            else:
                image_entries = soup.select(feed_options_item.image_css_selector)
                if len(image_entries) > 0:  # May not contain image
                    image_url = image_entries[0]["src"]

            # TODO: Implement regex cleaning here

            rss_item = RSSItem(entry.link, feed_options_item.category,
                               entry.title, item_text, item_description, image_url)
            ret.append(rss_item)

    return ret


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    #testf()

    # feeds: A list of RSSFeedOptions items
    feeds = [RSSFeedOptions("http://kanal5.com.mk/rss/vestixml-makedonija.asp",
                            content_css_selector="div.entry div:nth-of-type(4)",
                            image_css_selector="div.entry div.frame_box img",
                            category="makedonija"),
             RSSFeedOptions("http://www.plusinfo.mk/rss/zdravje",
                            content_css_selector="div.glavna_text",
                            image_css_selector="#MainContent_imgVest",
                            category="zdravje")]
    # (, "", [])]

    ret = rss_extract_items(feeds)

    response.flash = T("Welcome to miniTimeMK")
    return dict(message=T('Hello WORLD'),
                entries=ret
                )


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
