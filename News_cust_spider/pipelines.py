# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import codecs


class NewsCustSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class NewsImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            try:
                if value["path"]:
                    image_file_path = value["path"]
                    print(image_file_path)
                    item["image_path"] = image_file_path
            except Exception as e:
                print(e)

        return item


class FileWritingPipeline(object):
    # def __init__(self):
    #     self.file = codecs.open('news.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        # lines = json.dumps(item['content'], ensure_ascii=False) + '\n'
        for each in item:

            if each:
                file = codecs.open('get_html/' + item['name'], 'w', encoding="utf8")
                list = item['content']
                file.write('<html>')
                file.write("<meta charset='UTF-8'>")
                file.write('<body>')
                file.write('<h3 style="color:#ff0000;height:80px;text-align:center;line-height:70px;">' +
                           item["title"] + '</h3>')
                file.write('<p style="color:#0000ff;text-align:center">'+item["date"]+'</p>')

                if item["image_urls"]:
                    print(item["image_path"])
                    file.write('<p style="text-align:center; text-indent:24pt;">')
                    file.write('<span>')
                    print('"' + item["image_path"] + '"')
                    file.write('<img alt="" src="../image/' + item["image_path"] + '"  >')
                    file.write('</span>')
                    file.write('</p>')
                for st in list:
                    file.write('<p style="text-indent:24pt;">' + st + '</p>')

                file.write('</body>')
                file.write('</html>')
                file.close()
        # self.file.write(lines)
        return item


class ReferenceWritingPipeline(object):
    def process_item(self, item, spider):
        for each in item:
            if each:
                key = item["reference_url_content"]
                if key:
                    file = codecs.open('reference_html/' + item['name'], 'w', encoding="utf8")
                    file.write('<html>')
                    file.write("<meta charset='UTF-8'>")
                    file.write('<body>')
                    for each_line in key:
                        file.write(each_line)
                    file.write('</body>')
                    file.write('</html>')
                    file.close()
        return item
