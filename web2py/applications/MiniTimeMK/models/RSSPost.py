import re


class RSSPost(object):
    def __init__(self, page_url, category, source, pub_date, item_title,
                 item_content, item_filtered_content, item_description="", item_image_url=""):
        """
        :param page_url: A string containing the page URL
        :param category: An integer specifying the category id
        :param source: An integer specifying the source id
        :param pub_date: A string containing the published date
        :param item_title: A string containing the page title
        :param item_content: A string containing the clean page content
        :param item_description: A string containing the item description.
            If not specified, the first 200 characters of the content are used.
        :param item_image_url: A string containing the image url
        """

        self.page_url = page_url
        self.category = category
        self.source = source
        self.pub_date = pub_date
        self.item_title = item_title
        self.item_content = item_content
        self.item_filtered_content = item_filtered_content
        if item_description.strip() == "":
            self.item_description = self._get_item_description()
        else:
            self.item_description = item_description
        self.item_image_url = self._compose_full_url(item_image_url)

    def _compose_full_url(self, url):
        """
        Creates an absolute URL given a relative URL in the post.

        :param url: The relative URL found in the post
        :return: An absolute URL of the relative URL found in the post
        """

        if len(url) == 0:
            return ""

        if url.startswith("http"):
            return url
        else:
            a = re.findall(r"https?://.+?/", self.page_url)
            if len(a) > 0:
                b = re.sub(r"\.?/?(.+)", r"\1", url)
                if url.startswith("."):
                    ret = self.page_url + "/" + b
                else:
                    ret = str(a[0]) + b
                return ret
            else:
                return url

    def _get_item_description(self):
        """
        Creates post description from the content.

        :return: The first 250 characters from the post unfiltered content
        """

        return self.item_content[0:min(len(self.item_content), 251)] + '...'

    def db_insert(self):
        # rows = db(db.posts.link == self.page_url).select(db.posts.id)
        # if len(rows) == 0:
            # print(self.link)
        db.posts.insert(link=self.page_url,
                        cluster=None,
                        category=self.category,
                        source=self.source,
                        title=self.item_title,
                        text=self.item_filtered_content,
                        description=self.item_description,
                        imageurl=self.item_image_url,
                        pubdate=self.pub_date)
        return True
        # return False

    @staticmethod
    def get_post(post_id):
        rows = db(db.posts.id == post_id).select(db.posts.ALL)
        if len(rows) > 0:
            # Post id not necessary ?
            return RSSPost(page_url=rows[0].link,
                           category=rows[0].category,
                           source=rows[0].source,
                           pub_date=rows[0].pubdate,
                           item_title=rows[0].title,
                           item_content=rows[0].text,
                           item_filtered_content=rows[0].text,
                           item_description=rows[0].description,
                           item_image_url=rows[0].imageurl)
        else:
            return None