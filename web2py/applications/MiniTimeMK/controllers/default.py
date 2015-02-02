# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################


def update():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    Fetches new posts, updates the database, performs clustering and generates static pages
    """
    update_site()

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
            # print("Cluster: " + str(cluster.id))

            posts = db((cluster.id == db.posts.cluster) &
                       (db.posts.source == db.sources.id)).select(db.posts.ALL, db.sources.website, orderby=db.posts.id)
            if len(posts) > 0:
                cluster_entries[category.id] = temp_cluster
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
