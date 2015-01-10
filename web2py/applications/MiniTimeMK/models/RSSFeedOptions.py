
class RSSFeedOptions(object):
    def __init__(self, feed_url, source_id="", content_from_rss=False, content_rss_tag=None, content_css_selector="",
                 image_from_rss=False, image_rss_tag=None, image_css_selector="",
                 item_rss_description=False, category=None, recode=1, clean_regex=[]):
        """
        :param feed_url: A string representation of the url to the feed
        :param source_id: An id of the source in the database
        :param content_from_rss: A boolean flag which specifies whether the content should be taken
            from the RSS or from the HTML of the page. Default: False
        :param content_rss_tag: A string that specifies the RSS item tag for the content.
            Used if content_from_rss is True.
        :param content_css_selector: A string that specifies the CSS selector (jQuery style) for the content.
            Used if content_from_rss is False.
        :param image_from_rss: A boolean flag which specifies whether the image should be taken
            from the RSS or from the HTML of the page. Default: False
        :param image_rss_tag: A string that specifies the RSS item tag for the image.
            Used if image_from_rss is True.
        :param image_css_selector: A string that specifies the CSS selector (jQuery style) for the image.
            Used if image_from_rss is False.
        :param item_rss_description: A boolean flag specifying whether an item's description should be taken
            from the RSS "description" tag
        :param category: An integer specifying the feed's category
        :param recode: A flag specifying whether the content text should be recoded in utf-8
        :param clean_regex: A list of regular expressions as raw strings that should be performed
            on the extracted content.
            Each item should be a tuple with format: (regex_expr, output_fmt)
            where regex_expr is the raw regex expression and
            output_fmt is the output format into which the matched content should be formatted
        """
        self.feed_url = feed_url
        self.source_id = source_id
        self.content_from_rss = content_from_rss
        self.content_rss_tag = content_rss_tag
        self.content_css_selector = content_css_selector
        self.image_from_rss = image_from_rss
        self.image_rss_tag = image_rss_tag
        self.image_css_selector = image_css_selector
        self.item_rss_description = item_rss_description
        self.category = category
        self.clean_regex = clean_regex
        self.recode = True if recode == 1 else False