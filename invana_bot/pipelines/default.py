from invana_bot.spiders.default import DefaultParserSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class ParserCrawler(object):
    """

    pipe_data = {  # single pipe

        "parser_id": "blog-list",
        "data_extractors": [
            {
                "data_selectors": [
                    {
                        "id": "items",
                        "selector": ".post-listing .post-item",
                        "selector_attribute": "element",
                        "multiple": True
                    },
                    {
                        "id": "url",
                        "selector": ".post-header h2 a",
                        "selector_type": "css",
                        "selector_attribute": "href",
                        "parent_selector": "items",
                        "multiple": False
                    },
                    {
                        "id": "title",
                        "selector": ".post-header h2 a",
                        "selector_type": "css",
                        "selector_attribute": "text",
                        "parent_selector": "items",
                        "multiple": False
                    },
                    {
                        "id": "content",
                        "selector": ".post-content",
                        "selector_type": "css",
                        "selector_attribute": "html",
                        "parent_selector": "items",
                        "multiple": False
                    }
                ],
            }
        ],
        "traversals": [{
            "traversal_type": "pagination",
            "pagination": {
                "selector": ".next-posts-link",
                "selector_type": "css",
                "max_pages": 2
            },
        }]

    }

    context = {
        "client_id": "something"
    }

    """

    def __init__(self, parser=None, start_urls=None, job_id=None,
                 all_parsers=None, context=None):
        """

        :param parser: single unit of crawling
        :param all_parsers: set of units combined to create a flow
        :param context: any extra information user want to send to the crawled data.
        """
        self.parser = parser
        self.job_id = job_id
        self.all_parsers = all_parsers
        self.start_urls = start_urls
        if context:
            self.context = context
        self.validate_pipe()

    def validate_pipe(self):
        must_have_keys = ["parser_id", "data_extractors"]
        optional_keys = ["traversals"]
        for key in must_have_keys:
            if key not in self.parser.keys():
                raise Exception(
                    "invalid parser data, should have the following keys; {}".format(",".join(must_have_keys)))

    def validate_traversal(self):
        pass  # TODO - implement this

    def validate_extractor(self):
        pass  # TODO - implement this

    def get_traversals(self):
        return self.parser.get("traversals", [])

    def get_extractors(self):
        return self.parser.get("data_extractors", [])

    def generate_pipe_kwargs(self):
        domains = []

        for url in self.start_urls:
            domain = url.split("://")[1].split("/")[0]  # TODO - clean this
            domains.append(domain)

        extractor = LinkExtractor()
        rules = [
            Rule(extractor, follow=True)  # TODO - add regex types of needed.
        ]

        spider_kwargs = {
            "start_urls": self.start_urls,
            "allowed_domains": domains,
            "rules": rules,
            "parser": self.parser,
            "all_parsers": self.all_parsers,
            "context": self.context
        }
        return spider_kwargs

    def run(self):
        spider_cls = DefaultParserSpider
        spider_kwargs = self.generate_pipe_kwargs()
        return {"spider_cls": spider_cls, "spider_kwargs": spider_kwargs}


class CTIRunner(object):
    """



    """

    def __init__(self, cti_config=None, job_id=None, context=None):
        self.cti_config = cti_config
        self.crawler_config = self.cti_config['crawlers']
        self.parsers = self.crawler_config['parsers']
        self.job_id = job_id
        self.context = context

    def run(self):
        initial_parser = self.parsers[0]
        print("initial_parser", initial_parser)
        parser_crawler = ParserCrawler(
            job_id=self.job_id,
            start_urls=self.crawler_config['start_urls'],
            parser=initial_parser,
            all_parsers=self.parsers,
            context=self.context
        )
        cti_job = parser_crawler.run()
        return cti_job
