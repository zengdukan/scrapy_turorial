#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from tutorial.spiders.quotes_spider import QuotesSpider

if __name__ == '__main__':
    setting = get_project_settings()
    configure_logging(setting)

    runner = CrawlerRunner(setting)
    d = runner.crawl(QuotesSpider)
    d.addBoth(lambda _: reactor.stop())

    logging.info('start run')
    reactor.run()
    logging.info('all finished')