#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from tutorial.spiders.quotes_spider import QuotesSpider


def start_spider(arg, setting):
    runner = CrawlerRunner(setting)
    d = runner.crawl(QuotesSpider)
    # twisted deferred callback 必须有arg参数,否则不会回调
    d.addBoth(start_spider, setting)
    # d.addBoth(lambda _ : reactor.stop())
    return arg

if __name__ == '__main__':
    setting = get_project_settings()
    configure_logging(setting)

    start_spider(0, setting)

    logging.info('start run')
    reactor.run()
    logging.info('all finished')