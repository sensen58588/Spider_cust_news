# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
import re
from News_cust_spider.items import NewsCustSpiderItem


class CustNewsSpider(scrapy.Spider):
    name = 'cust_news'
    allowed_domains = ['cust.eud.cn']
    start_urls = ['http://cust.edu.cn/']

    def parse(self, response):
        get_index_url = response.css('.list01 .more ::attr(href)').extract_first("")
        index_url = parse.urljoin(response.url, get_index_url)
        print(index_url)
        yield Request(url=index_url, dont_filter=True, callback=self.parse_index)

    def parse_index(self, response):
        """
                1.获取当前页的文章url并交给scrapy下载后，进行具体解析
                2.获取下一页的url并交给scrapy进行下载
                :param response: 
                :return: 
        """
        # 1
        post_nodes = response.css('#warp .list15 li')
        for post_node in post_nodes:
            post_url = post_node.css('::attr(href)').extract_first("")
            url_get = parse.urljoin(response.url, post_url)

            yield Request(url=url_get, dont_filter=True, callback=self.parse_detail)
            print(parse.urljoin(response.url, post_url))

        # 2.获取下一页的url并交给scrapy进行下载

        next_urls = response.css('#warp  .list15 .list_sort > a:nth-child(3) ::attr(href)').extract_first("")
        if next_urls:
            next_url = parse.urljoin(response.url, next_urls)
            # 获取最后一页的“上一页”url,加判断
            last_second_url = response.css('#warp  .list15 .list_sort > a:nth-child(2) ::attr(href)').extract_first("")
            # last_second_url = parse.urljoin(response.url, last_second_url)
            if last_second_url != 'index248.htm':
                yield Request(url=next_url, dont_filter=True, callback=self.parse_index)

    def parse_detail(self, response):
        news_spider_item = NewsCustSpiderItem()

        # news_spider_item = NewsCustSpiderItem()
        title = response.css('#main3 h3::text').extract()[0]
        # print(title)
        date = response.css('#author ::text').extract()[0]
        reg_data = ".*(\d+)"
        get_data = re.match(reg_data, date)
        if get_data:
            date = get_data.group(0)

        img_urls = response.css('#work img::attr(src)').extract()
        if img_urls:
            for img_url in img_urls:
                try:
                    get_img_url = parse.urljoin(response.url, img_url)
                    print(get_img_url)
                    news_spider_item["image_urls"] = [get_img_url]

                except Exception as e:
                    print(e)

        else:
            news_spider_item["image_urls"] = []

        url = response.url
        reg_url_name = ".*?(\d+)"
        get_url = re.match(reg_url_name, url)
        if get_url:
            get_name = get_url.group(1) + '.htm'

        print(get_name)
        content = response.css('#work span::text').extract()
        reg = "^(http|https|ftp)://.*(.com|.cn|.html|.htm|.asp|.jsp)"

        news_spider_item["url"] = response.url
        news_spider_item["title"] = title
        news_spider_item["date"] = date
        news_spider_item["name"] = get_name
        news_spider_item["content"] = content

        reference_url_list = []
        for each_line in content:
            get_reference_url = re.match(reg, each_line)
            if get_reference_url:
                # print('**********************************************')
                # print(get_reference_url.group(0))
                # get_reference_url = get_reference_url.group(0)
                reference_url_list.append(get_reference_url.group(0))
                # news_spider_item["reference_urls"] = get_reference_url.group(0)
        else:
            news_spider_item["reference_urls"] = reference_url_list
            news_spider_item["reference_url_content"] = []
            yield news_spider_item

    def parse_reference(self, response):
        news_spider_item = NewsCustSpiderItem()
        get_content = response.css('html ::text').extract()

        if get_content:
            news_spider_item["reference_urls"] = response.url
            news_spider_item["reference_url_content"] = get_content

        else:
            news_spider_item["reference_urls"] = []
            news_spider_item["reference_url_content"] = []
        yield news_spider_item
