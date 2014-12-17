__author__ = 'martin'
#aaaa
class Post(object):
    def __init__(self, link, category, source, title, text, description, image_url, pubdate):
        self.id = None
        self.link = link
        self.category = category
        self.source = source
        self.title = title
        self.text = text
        self.image_url = image_url
        self.pubdate = pubdate
        self.description = description

    def insertDatabase(self):
        rows = db(db.posts.link == self.link).select(db.posts.id)
        if len(rows) == 0:
            # print(self.link)
            db.posts.insert(link=self.link, cluster=None, category=self.category, source=self.source,
                            title=self.title, text=self.text, description=self.description, imageurl=self.image_url,
                            pubdate=self.pubdate)
            return True
        return False

    @staticmethod
    def getPost(id):
        rows = db(db.posts.id == id).select(db.posts.ALL)
        post = Post(rows[0].link, rows[0].category, rows[0].source, rows[0].title, rows[0].text, rows[0].imageurl, rows[0].pubdate)
        post.id = rows[0].id
        return post