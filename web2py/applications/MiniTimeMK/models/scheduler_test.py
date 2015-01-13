# -*- coding: utf-8 -*-
import time
from datetime import datetime
import threading

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


def hours_ago(mins):
    """
    Converts minutes to hours

    :param mins: The number of minutes to convert
    :return: A string representing the converted hours or minutes
    """

    if mins >= 60:
        hours = int(mins/60)
        if hours == 1:
            return "1 час"
        else:
            return str(hours) + " часа"
    else:
        return str(mins) + " мин"


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

    import os
    print 'Generating static page: ', page_name

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
    .time{
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
    <script src="http://code.jquery.com/jquery-1.11.2.min.js"></script>
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
                    if i%3 == 0:
                        f.write('<div class="first_in_row">')
                    else:
                        f.write('<div>')
                    for (postId, title, image, description, link, published, website) in posts:
                        if first:
                            f.write('<article>')
                            f.write('<a href="' + link + '" target="_blank"><img src="' + image + '" /></a>')
                            f.write('<a href="' + link + '" target="_blank"><h4>' + title + ' <span class="time"> ' + website + ' - ' + published + '</span></h4></a>')
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
    print 'Generating static pages: %d ms' % (t2 - t1)


def testf():
    t = time.ctime()
    open('/tmp/sch_testing', 'a').write('Testing 1 2 3' + t + '\n')
    print("HELLO NIGGERS")
    print(t)
    return t

from gluon.scheduler import Scheduler
Scheduler(db, dict(testtask=testf))
