# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
import re
from News_cust_spider.items import NewsCustSpiderItem


class CustNewsSpider(scrapy.Spider):
    name = 'reference_news_spider'
    allowed_domains = ['cust.eud.cn']
    start_urls = ['http://cust.edu.cn/']
    get_name = ''
    count = 0

    def parse(self, response):
        get_index_url = response.css('.list01 .more ::attr(href)').extract_first("")
        index_url = parse.urljoin(response.url, get_index_url)
        print(index_url)
        yield Request(url=index_url, dont_filter=True, callback=self.parse_index)

    def parse_index(self, response):

        post_nodes = response.css('#warp .list15 li')
        for post_node in post_nodes:
            post_url = post_node.css('::attr(href)').extract_first("")
            url_get = parse.urljoin(response.url, post_url)

            yield Request(url=url_get, dont_filter=True, callback=self.parse_detail)
            print(parse.urljoin(response.url, post_url))

        next_urls = response.css('#warp  .list15 .list_sort > a:nth-child(3) ::attr(href)').extract_first("")
        if next_urls:
            next_url = parse.urljoin(response.url, next_urls)

            last_second_url = response.css('#warp  .list15 .list_sort > a:nth-child(2) ::attr(href)').extract_first("")

            if last_second_url != 'index248.htm':
                yield Request(url=next_url, dont_filter=True, callback=self.parse_index)

    def parse_detail(self, response):
        content = response.css('#work span::text').extract()
        reg = "^(http|https|ftp)://.*(.com|.cn|.html|.htm|.asp|.jsp)"
        url = response.url
        reg_url_name = ".*?(\d+)"
        get_url = re.match(reg_url_name, url)
        if get_url:
            self.get_name = get_url.group(1)
        reference_url_list = []
        for each_line in content:
            get_reference_url = re.match(reg, each_line)
            if get_reference_url:
                reference_url_list.append(get_reference_url.group(0))
        self.count = 0
        if reference_url_list:
            for each_url in reference_url_list:
                yield Request(url=each_url, dont_filter=True, callback=self.parse_reference)
                self.count += 1
        else:
            pass

    def parse_reference(self, response):
        reference_item = NewsCustSpiderItem()
        get_content = response.css('html ::text').extract()

        if get_content:
            reference_item["name"] = self.get_name + 'reference'+str(self.count)+'.htm'
            reference_item["reference_urls"] = response.url
            reference_item["reference_url_content"] = get_content

        else:
            reference_item["reference_urls"] = []
            reference_item["reference_url_content"] = []
        yield reference_item
