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


def get_html(entry, feed_options_item, queue):
    """
    Extracts the html of the page specified with url and puts it in a queue.
    Intended for parallelized usage.

    :param entry: The RSS Feed entry
    :param queue: The queue where to store the result
    """
    try:
        entry_html = urllib.urlopen(entry.link.encode("utf-8")).read()
        queue.put((entry, "".join(entry_html), feed_options_item))
    except IOError as e:
        print "ERROR runtime: ", e, e.strerror
    except RuntimeError as e:
        print "ERROR runtime: ", e.strerror


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


def parse_mk_month(month):
    """
    :param month:
    :return:
    """
    l_month = month.lower()
    if l_month == u'јануари':
        return u'01'
    elif l_month == u'февруари':
        return u'02'
    elif l_month == u'март':
        return u'03'
    elif l_month == u'април':
        return u'04'
    elif l_month == u'мај':
        return u'05'
    elif l_month == u'јуни':
        return u'06'
    elif l_month == u'јули':
        return u'07'
    elif l_month == u'август':
        return u'08'
    elif l_month == u'септември':
        return u'09'
    elif l_month == u'октомври':
        return u'10'
    elif l_month == u'ноември':
        return u'11'
    elif l_month == u'декември':
        return u'12'

    return None


def parse_rss_post(entry, html, feed_options_item):
    soup = BeautifulSoup(html)
    default_date = strftime("%Y-%m-%d %H:%M:%S")
    default_encoding = "utf-8"

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

    # BUGFIX: Workaround for Kanal5 missing publish date
    if feed_options_item.source_id == 1:
        import re
        pattern = re.compile(
            u'(\d+)\s+([A-Za-zАБВГДЃЕЖЗЅИЈКЛЉМНЊОПРСТЌУФХЦЧЏШабвгдѓежзѕијклљмнњопрстќуфхцчџш]+)\s+(\d+)\s+во (\d+):(\d+)'
        )
        html_date = soup.select("div.author-description div.author-text p")
        if len(html_date) > 0:
            k5_date = html_date[0].get_text()
            res = pattern.search(k5_date)
            if res is not None:
                month_num = parse_mk_month(res.group(2))
                if month_num is not None:
                    d_year = res.group(3)
                    d_date = res.group(1)
                    d_hour = res.group(4)
                    d_min = res.group(5)
                    item_pub_date = u"{0}-{1}-{2} {3}:{4}:00".format(
                        d_year,
                        month_num,
                        d_date,
                        d_hour,
                        d_min
                    )
        if item_pub_date is None or item_pub_date == "":
            item_pub_date = default_date

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
            if soup.original_encoding is not None:
                item_text = item_text.encode(soup.original_encoding, errors='ignore')
            else:
                item_text = item_text.encode(default_encoding, errors='ignore')

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
    return rss_post


def parse_feed_parallel(num, feed_options_item, all_links, queue, t_limit=None):
    """
    Parallel creation of a RSSItem for each post in the feed.

    :param num: The feed's number in the list. For DEBUG purposes
    :param feed_options_item: The RSS Feed options
    :param all_links: A set of all the links in the database
    :param queue: A Queue to store the resulting RSSPost objects
    :param t_limit: An integer used to limit the number of running threads
    """
    print 'Extracting feed: ', num, feed_options_item.feed_url
    d = feedparser.parse(feed_options_item.feed_url)

    # Create a thread for each entry in the feed which is not present in the database
    threads = []
    for entry in d.entries:
        if 'feedproxy.google' in entry.link:    # Feedproxy workaround
            if entry.get("feedburner_origlink", entry.link) not in all_links:
                threads.append(threading.Thread(target=get_html, args=(entry, feed_options_item, queue)))
                # Adds link in case there is a duplicate entry in the new ones
                all_links.add(entry.get("feedburner_origlink", entry.link))
        else:
            if entry.link not in all_links:
                threads.append(threading.Thread(target=get_html, args=(entry, feed_options_item, queue)))
                # Adds link in case there is a duplicate entry in the new ones
                all_links.add(entry.link)

    # Run threads depending on thread limit
    if t_limit:
        for i in range(0, len(threads), t_limit):
            for j in range(min(t_limit, len(threads) - i)):
                threads[i+j].start()
            for j in range(min(t_limit, len(threads) - i)):
                threads[i+j].join()

    else:
        # If t_limit is None, run all post threads at once
        for t in threads:
            t.start()
        for t in threads:
            t.join()


def rss_extract_items(feeds_list):
    """
    Extracts the text from each RSS entry in each RSS feed in feeds_array
    and performs cleaning of interpunction signs and other HTML tags
    Feeds array should consists of RSSFeedOptions items.

    :param feeds_list: A list of RSSFeedOptions items
    """
    all_dbrow_links = db().select(db.posts.link)    # List of Row objects containing the links
    raw_links = set([row.link for row in all_dbrow_links])  # Set of strings containing the links

    items = Queue()
    print 'Parallel fetch started', len(feeds_list), 'feeds'
    t1 = millis()

    f_limit = 5     # Number of feeds to process in parallel
    t_limit = 13    # Number of posts to process in parallel in each feed
    print f_limit, "feed threads with", t_limit, "post threads"
    threads = [threading.Thread(target=parse_feed_parallel,
                                args=(i, feed_options_item, raw_links, items, t_limit))
               for i, feed_options_item in enumerate(feeds_list)]

    for i in range(0, len(threads), f_limit):
        for j in range(min(f_limit, len(threads) - i)):
            threads[i+j].start()
        for j in range(min(f_limit, len(threads) - i)):
            threads[i+j].join()

    t2 = millis()
    print "Parallel: feeds processed in %d ms" % (t2-t1)

    print items.qsize(), "posts",
    t1 = millis()
    while not items.empty():
        (entry, html, feed_options_item) = items.get_nowait()
        rss_post = parse_rss_post(entry, html, feed_options_item)
        rss_post.db_insert()
    t2 = millis()
    print "processed and inserted in: %d ms" % (t2 - t1)


def update():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    Fetches new posts, updates the database, performs clustering and generates static pages
    """
    t1 = millis()

    # TODO: This should go in scheduler_test
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

    rss_extract_items(feeds)
    new_clusters = clustering()
    generate_static()

    t2 = millis()
    print 'Total update time: %d ms' % (t2 - t1)

    redirect('index')
    return dict()


def index():
    req_category = request.vars.get('cat_id', None)
    try:
        if req_category is not None:
            req_category = int(req_category)
    except ValueError:
        redirect('index')

    all_categories = db().select(db.categories.ALL)
    if req_category is None or not isinstance(req_category, int) \
            or req_category < 0 or req_category > len(all_categories):
        category_list = all_categories
    else:
        category_list = db(db.categories.id == req_category).select(db.categories.ALL)

    category_entries = []
    cluster_entries = {}
    post_entries = {}

    for category in category_list:
        category_entries.append((category.id, category.category))
        clusters = db(db.cluster.category == category.id).select(db.cluster.ALL, orderby=~db.cluster.score)
        cluster_len = 3 if req_category is None else len(clusters)
        # print "Category: ", category.id, category.category

        for cluster in clusters[:cluster_len]:
            temp_cluster = cluster_entries.get(category.id, [])
            temp_cluster.append(cluster.id)
            cluster_entries[category.id] = temp_cluster
            # print("Cluster: " + str(cluster.id))

            posts = db((cluster.id == db.posts.cluster) &
                       (db.posts.source == db.sources.id)).select(db.posts.ALL, db.sources.website, orderby=db.posts.id)
            for post in posts:
                temp_posts = post_entries.get(cluster.id, [])
                time_ago = "пред " + time_between(str(time.strftime("%Y-%m-%d %H:%M:%S")), str(post.posts.pubdate))
                temp_posts.append([post.posts.id, post.posts.title, post.posts.imageurl,
                                  post.posts.description, post.posts.link, time_ago, post.sources.website])
                post_entries[cluster.id] = temp_posts
                # print ("Post: " + str(post.posts.id))
            # print
        # print

    return dict(categoryentries=category_entries,
                clusterEntries=cluster_entries,
                postEntries=post_entries
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
