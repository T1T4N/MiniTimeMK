import re


class RSSItem(object):
    def __init__(self, page_url, category, pub_date, item_title, item_content, item_filtered_content, item_description="", item_image_url=""):
        """
        :param page_url: A string containing the page URL
        :param category: A string containing the page category
        :param pub_date: A string containing the published date
        :param item_title: A string containing the page title
        :param item_content: A string containing the clean page content
        :param item_description: A string containing the item description.
            If not specified, the first 200 characters of the content are used.
        :param item_image_url: A string containing the image url
        """

        self.page_url = page_url
        self.category = category
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
        # TODO: (special case) Resolve real URL from Feedburner proxy
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
        return self.item_content[0:min(len(self.item_content), 251)] + '...'