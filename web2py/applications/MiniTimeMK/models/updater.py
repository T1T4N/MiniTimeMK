# -*- coding: utf-8 -*-
from datetime import datetime
from time import strftime
from Queue import Queue
from pyquery import PyQuery as pq
from lxml import etree
import os
import time
import speedparser
import re
import urllib3
import urllib
import threading
import logging
logger = logging.getLogger("MiniTimeMK")
logger.setLevel(logging.DEBUG)


def days_between(days):
    """
    Converts days to weeks/months/years

    :param days: The number of days to convert
    :return: A string representing the difference
    """

    if days >= 365:
        return str(int(days/365)) + " год"
    if days >= 30:
        return str(int(days/30)) + " мес"
    if days >= 7:
        return str(int(days/7)) + " нед"
    if days == 1:
        return str(days) + " ден"
    return str(days) + " дена"


def hours_ago(minutes):
    """
    Converts minutes to hours

    :param minutes: The number of minutes to convert
    :return: A string representing the converted hours or minutes
    """

    if minutes >= 60:
        hours = int(minutes/60)
        if hours == 1:
            return "1 час"
        else:
            return str(hours) + " часа"
    else:
        return str(minutes) + " мин"


def time_between(d1, d2):
    """
    Calculates difference between two dates

    :param d1: First date, must be > d2
    :param d2: Second date, must be < d1
    :return: A string representing the time difference
    """

    d1 = datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
    d2 = datetime.strptime(d2, "%Y-%m-%d %H:%M:%S")
    days = (d1 - d2).days
    if days > 0:
        return str(days_between(days))
    else:
        minutes = int((d1-d2).total_seconds()/60)
        return hours_ago(minutes)


def create_static_page(page_name, pages_url, categories, cluster_entries, post_entries):
    """
    Creates the static html pages from the clusters.

    :param page_name: The file name of the html page
    :param pages_url: The URL pointing to the category static pages
    :param categories: The id and names of the categories
    :param cluster_entries: The clusters for the specified categories
    :param post_entries: The posts for the specified clusters
    """

    logger.info('Generating static page: %s' % page_name)

    f = open(os.path.dirname(__file__) + os.sep +
             ".." + os.sep +
             "static" + os.sep + page_name + ".html", 'w')
    f.write(
        """<!DOCTYPE html>
<html>
<head>
    <title>Информирај се</title>
    <meta charset="utf-8" />
    <style>
    *{
        font-family: Tahoma, sans-serif;
    }
    a{
        text-decoration: none;
        color: inherit;
    }
    #main{
        width: 980px;
        margin: 0 auto;
        min-height: 300px;
    }
    h3{
        width: 100%;
        background: #f0f0f0;
        border-radius: 5px;
    }
    .category{
        overflow: auto;
    }
    .category > div{
        padding: 0.3%;
        border: 1px solid #CCC;
        width: 29%;
        margin-top: 10px;
        background: #f0f0f0;
        float: left;
        margin-right: 2.6%;
        font-size: 0.85em;
        text-align: right;
    }
    article h4, article p{
        margin: 0.3em 0;
        text-align: left;
    }
    article p{
        font-size: 0.8em;
        text-align: justify;
    }
    .category div:nth-of-type(2){
        margin-left: -3px;
    }
    .category div:nth-of-type(3){
        margin-right: 0;
        margin-left: -3px;
    }
    .category h5{
        text-align: left;
    }
    article img{
        width: 100%;
        height: 200px;
    }
    div.first_in_row {
        clear: left;
    }
    .related{
        display: none;
    }
    .time, .count{
        font-size: 0.6em;
        color: #666;
    }
    .more{
        cursor: pointer;
        font-size: 0.8em;
        font-weight: bold;
        color: #0088ff;
    }
    #f1_container {
      position: relative;
      margin: 10px auto;
      width: 450px;
      height: 503px;
      z-index: 1;
    }
    #f1_container {
      perspective: 1000;
    }
    #f1_card {
      width: 100%;
      /*height: 100%;*/
      transform-style: preserve-3d;
      transition: all 1.0s linear;
    }
    #f1_container:hover #f1_card {
      transform: rotateY(180deg);
    }
    .front{
        overflow: inherit;
    }
    .back{
        height: inherit;
    }
    .face {
      position: absolute;
      width: 100%;
      backface-visibility: hidden;
    }
    .face.back {
      display: block;
      transform: rotateY(180deg);
      box-sizing: border-box;
      padding: 10px;
      color: white;
      text-align: center;
      background-color: #aaa;
    }
    </style>
    <script src=""" + URL('static', 'js/jquery.js') + """"></script>
    <script>
        $(document).ready(function(){
            $('.more').click(function () {
                if($.trim($(this).text()) === "Повеќе поврзани статии»"){
                    $(this).text("Врати се назад");
                    $(this).parent().find("article").hide();
                    $(this).parent().find(".related").show();
                }else{
                    $(this).parent().find(".related").hide();
                    $(this).parent().find("article").show();
                    $(this).text("Повеќе поврзани статии»");
                }
            });
        });
    </script>
</head>
<body>
<header>
</header>
<div id="main">"""
    )

    for (k, (id, category)) in enumerate(categories):
        f.write('<div class="category">')
        f.write('<h3><a href="' + pages_url[k] + '">' + category + '</a></h3>')

        arr = cluster_entries.get(id)

        if arr is not None:
            for i, cl in enumerate(arr):
                posts = post_entries.get(cl)
                if posts is not None:
                    first = True
                    if i % 3 == 0:
                        f.write('<div class="first_in_row">')
                    else:
                        f.write('<div>')
                    for (postId, title, image, description, link, published, website) in posts:
                        if first:
                            f.write('<article>')
                            f.write('<a href="' + link + '" target="_blank"><img src="' + image + '" /></a>')
                            f.write('<a href="' + link + '" target="_blank"><h4><span class="title">' + title +
                                    '</span></br><span class="time"> ' + website + ' - ' + published + '</span> ' +
                                    '<span class="count">' + str(len(posts)) + ' поврзани вести</span>'
                                    '</h4></a>')
                            f.write('<p>' + description + '</p>')
                            f.write('</article>')
                            if len(posts) > 1:
                                f.write('<span class="more"> Повеќе поврзани статии» </span>')
                            f.write('<div class="related">')
                        else:
                            f.write('<a href="' + link + '" target="_blank"><h5>' + title + '</h5></a>')
                        first = False
                    if len(posts) > 1:
                        f.write('</div>')
                    f.write('</div>')
        f.write('</div>')
    f.write(
        """</div>
    <footer>
    </footer>
</body>
</html>"""
    )
    f.close()


def generate_categories(req_category=None):
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
        clusters = db(category.id == db.cluster.category).select(db.cluster.ALL, orderby=~db.cluster.score)
        cluster_len = 3 if req_category is None else len(clusters)

        for cluster in clusters[:cluster_len]:
            temp_cluster = cluster_entries.get(category.id, [])
            temp_cluster.append(cluster.id)
            cluster_entries[category.id] = temp_cluster
            posts = db((cluster.id == db.posts.cluster) &
                       (db.posts.source == db.sources.id)).select(db.posts.ALL, db.sources.website, orderby=db.posts.id)

            for post in posts:
                temp_posts = post_entries.get(cluster.id, [])
                time_ago = "пред " + time_between(str(time.strftime("%Y-%m-%d %H:%M:%S")), str(post.posts.pubdate))
                temp_posts.append([post.posts.id, post.posts.title, post.posts.imageurl,
                                  post.posts.description, post.posts.link, time_ago, post.sources.website])
                post_entries[cluster.id] = temp_posts
    return category_entries, cluster_entries, post_entries


def generate_static():
    t1 = millis()
    categories = db().select(db.categories.ALL)
    category_urls = [URL('static', cat.static_name + '.html') for cat in categories]

    category_entries, cluster_entries, post_entries = generate_categories()
    create_static_page("index", category_urls, category_entries, cluster_entries, post_entries)

    threads = []
    for i, category in enumerate(categories):
        category_entries, cluster_entries, post_entries = generate_categories(int(category.id))
        threads.append(threading.Thread(target=create_static_page,
                                        args=(category.static_name, category_urls,
                                              category_entries, cluster_entries, post_entries)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    t2 = millis()
    logger.info('Generating static pages: %d ms' % (t2 - t1))


def get_html3(pool_manager, entry, feed_options_item, queue):
    """
    Extracts the html of the page specified with url and puts it in a queue.
    Intended for parallelized usage.

    :param entry: The RSS Feed entry
    :param queue: The queue where to store the result
    """

    try:
        l = entry.link.encode("utf-8")
        # Bug fix: HTTPConnectionPool uses urls relative to the host
        m = l[l.find('/', 8):]  # Find first occurrence of / after http:// part
        r = pool_manager.request('GET', m, retries=False)

        queue.put((entry, "".join(r.data), feed_options_item))
    except urllib3.exceptions.MaxRetryError as e:
        logger.error("MaxRetryError: %s" % e)
    except IOError as e:
        logger.error("IOError: %s" % e)
    except RuntimeError as e:
        logger.error("RuntimeError:" % e)


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
    try:
        soup = pq(etree.HTML(html))

        default_date = strftime("%Y-%m-%d %H:%M:%S")
        default_encoding = "utf-8"

        item_description = ""
        item_text = ""
        image_url = ""

        item_link = entry.link
        if 'feedproxy.google' in item_link:     # FeedProxy workaround
            item_link = entry.get("id", item_link)      # SpeedParser specific
            # item_link = entry.get("feedburner_origlink", item_link)

        # SpeedParser changes: uses "updated" instead of "published"
        item_pub_date = entry.get("updated", default_date)   # default
        if item_pub_date != default_date:
            if entry.updated_parsed is None or entry.updated_parsed == "":
                item_pub_date = default_date
            else:
                # TODO: timezone adjustment
                item_pub_date = strftime("%Y-%m-%d %H:%M:%S", entry.updated_parsed)

        # Bug fix: Workaround for Kanal5 missing publish date
        if feed_options_item.source_id == 1:
            pattern = re.compile(
                u'(\d+)\s+([A-Za-zАБВГДЃЕЖЗЅИЈКЛЉМНЊОПРСТЌУФХЦЧЏШабвгдѓежзѕијклљмнњопрстќуфхцчџш]+)\s+(\d+)\s+во (\d+):(\d+)'
            )
            html_date = soup("div.author-description div.author-text p")
            if len(html_date) > 0:
                # k5_date = html_date[0].get_text()
                k5_date = pq(html_date[0]).text()
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
                content_entries = soup(selector)
                if len(content_entries) > 0:
                    for part in content_entries:
                        part_text = pq(part).text()
                        if part_text is not None:
                            item_text += part_text + " "

            if item_text.strip() == "":
                return None     # If no text, don't insert in db

            if feed_options_item.recode:
                # Bug fix: Original encoding might not be present
                if soup.encoding is not None:
                    # Workaround for non utf-8 encoding found in Kurir
                    # Search for cyrillic letter 'a' and if text is junk it won't be found
                    if feed_options_item.source_id == 5 and item_text.find(u'\u0430') == -1:
                        item_text = item_text.encode('iso-8859-1', errors='ignore')
                    else:
                        item_text = item_text.encode(soup.encoding, errors='ignore')
                else:
                    item_text = item_text.encode(default_encoding, errors='ignore')

                item_text = item_text.decode(default_encoding, errors='ignore')

        if feed_options_item.image_from_rss:
            image_url = entry[feed_options_item.image_rss_tag]
        else:
            image_entries = soup(feed_options_item.image_css_selector)
            if len(image_entries) > 0:  # May not contain image
                image_url = pq(image_entries[0]).attr("src")

        """
        Regex cleaning here
        """
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
    except etree.XMLSyntaxError as e:
        logger.error("HTML parse error %s %s" % (entry.link, e))
        return None


def parse_feed_parallel(num, feed_options_item, all_links, queue, t_limit=None):
    """
    Parallel creation of a RSSItem for each post in the feed.

    :param num: The feed's number in the list. For DEBUG purposes
    :param feed_options_item: The RSS Feed options
    :param all_links: A set of all the links in the database
    :param queue: A Queue to store the resulting RSSPost objects
    :param t_limit: An integer used to limit the number of running threads
    """
    t1 = millis()

    # Read the feed XML and store it as a string
    a = urllib.urlopen(feed_options_item.feed_url).read()
    d = speedparser.parse(a, clean_html=False)  # SpeedParser is ~10 times faster than FeedParser
    # d = feedparser.parse(feed_options_item.feed_url)

    t2 = millis()
    logger.debug("%d %s with %d posts, speedparser done in: %d ms" % (num, feed_options_item.feed_url, len(d.entries), (t2-t1)))

    # Create a thread for each entry in the feed which is not present in the database
    threads = []

    http = None
    if 'feedburner' in feed_options_item.feed_url:
        # Got maxsize=40 experimentally as best value
        # PoolManager automatically handles different hosts
        # There is a bug with a1on that reports incorrect host
        http = urllib3.connection_from_url(d.entries[0].get("id", d.entries[0].link), maxsize=40, block=True)
    else:
        http = urllib3.connection_from_url(feed_options_item.feed_url, maxsize=40, block=True)

    # Filling thread list
    for entry in d.entries:
        if 'feedproxy.google' in entry.link:    # FeedProxy workaround
            # if entry.get("feedburner_origlink", entry.link) not in all_links:
            if entry.get("id", entry.link) not in all_links:    # SpeedParser changes
                threads.append(threading.Thread(target=get_html3, args=(http, entry, feed_options_item, queue)))
        else:
            if entry.link not in all_links:
                threads.append(threading.Thread(target=get_html3, args=(http, entry, feed_options_item, queue)))

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

    logger.info('Parallel fetch started on %d feeds' % len(feeds_list))
    items = Queue()

    t1 = millis()
    f_limit = 5     # Number of feeds to process in parallel
    t_limit = 10    # Number of posts to process in parallel in each feed

    logger.info("%d feed threads with %d post threads" % (f_limit, t_limit))
    threads = [threading.Thread(target=parse_feed_parallel,
                                args=(i, feed_options_item, raw_links, items, t_limit))
               for i, feed_options_item in enumerate(feeds_list)]

    for i in range(0, len(threads), f_limit):
        for j in range(min(f_limit, len(threads) - i)):
            threads[i+j].start()
        for j in range(min(f_limit, len(threads) - i)):
            threads[i+j].join()
    t2 = millis()
    logger.info("Feeds processed in %d ms" % (t2-t1))

    # All the posts from all the feeds are put in the items queue
    # After all threads have stopped, we start to parse each post
    num_items = items.qsize()
    t1 = millis()
    posts = []
    while not items.empty():
        (entry, html, feed_options_item) = items.get_nowait()
        # post_threads.append(threading.Thread(
        #     target=parse_rss_post, args=(entry, html, feed_options_item)
        # ))
        rss_post = parse_rss_post(entry, html, feed_options_item)
        if rss_post is not None:
            posts.append(rss_post)
    t2 = millis()
    logger.info("%d posts processed in %d ms" % (num_items, (t2 - t1)))

    t1 = millis()
    for rss_post in posts:
        rss_post.db_insert()
    t2 = millis()
    logger.info("Posts inserted in %d ms" % (t2 - t1))


def update_site():
    t1 = millis()

    # TODO: This should go in scheduler_test
    # Selects zero or more occurrences of any interpunction sign in the set
    interpunction_regex = u'(?:\s|[,."\'`:;!@#$%^&*()_<>/=+„“”–\-\\\|\[\]])' + u'*'

    # Selects every sequence of one or more latin or cyrillic, lowercase or uppercase letter and any number
    word_regex = u'([A-Za-z0-9АБВГДЃЕЖЗЅИЈКЛЉМНЊОПРСТЌУФХЦЧЏШабвгдѓежзѕијклљмнњопрстќуфхцчџш]+)'

    words_extraction_regex = [(interpunction_regex + word_regex + interpunction_regex, r'\1 ')]

    feeds = []
    rows = db(db.sources.id == db.rssfeeds.source).select(db.rssfeeds.ALL, db.sources.ALL, orderby='<random>')
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
    logger.info('Total update time: %d ms' % (t2 - t1))

from gluon.scheduler import Scheduler
Scheduler(db, dict(update_task=update_site))
