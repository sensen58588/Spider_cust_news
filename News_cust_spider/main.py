# -*- coding : utf-8 -*-
__author__ = 'sensen'

from scrapy.cmdline import execute
import os
import sys


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "cust_news"])
# execute(["scrapy", "crawl", "reference_news_spider"])
# 开关