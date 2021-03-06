from scrapy.crawler import CrawlerProcess
from invana_bot.spiders.feeds import RSSSpider
import uuid

from scrapy.utils.log import configure_logging


class InvanaBotWebCrawlerBase(object):
    """


    """
    settings = {
        'COMPRESSION_ENABLED': False,  # this will save the data in normal text form, otherwise to bytes form.
        'HTTPCACHE_ENABLED': True,
        'TELNETCONSOLE_PORT': None

    }
    runner = None

    def __init__(self,
                 settings=None,
                 **kwargs):

        if settings is None:
            raise Exception("settings should be set")
        self.settings = settings
        self.job_id = self.generate_job_id()
        self.set_logger()

    @staticmethod
    def set_logger():
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

    @staticmethod
    def generate_job_id():
        return uuid.uuid4().hex

    def _validate_urls(self, urls):
        if type(urls) is None:
            raise Exception("urls should be list type.")
        if len(urls) is 0:
            raise Exception("urls length should be atleast one.")

    def get_settings(self):
        return self.settings


"""
class InvanaFeedCrawler(InvanaBotWebCrawlerBase):

    def crawl_feeds(self, feed_urls=None):
        self.setup_crawler_type_settings(crawler_type="feeds")
        self._validate_urls(feed_urls)

        process = CrawlerProcess(self.settings)
        allowed_domains = []
        for feed_url in feed_urls:
            domain = feed_url.split("://")[1].split("/")[0]  # TODO - clean this
            allowed_domains.append(domain)

        process.crawl(RSSSpider,
                      start_urls=feed_urls,
                      )
        process.start()

"""
