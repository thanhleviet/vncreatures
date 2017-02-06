import scrapy
from vncreatures.items import VncreaturesItem, PlantItem
from vncreatures.settings import BASE_URL, PROJECT_ROOT, IMAGES
import re
import os
import urllib
from w3lib.html import remove_tags

class PlantSpider(scrapy.Spider):
    name = "plant"

    def start_requests(self):
        page_range = range(1, 90)

        urls = ['http://www.vncreatures.net/hinhanh.php?page={}&loai=2&nhom=0&'.format(i) for i in page_range]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        hxs = scrapy.Selector(response)
        items = hxs.select('//a[contains(@href, "./chitiet")]/@href').extract()

        _items = []

        for item in items:
            vn_item = VncreaturesItem()
            print item
            vn_item['url'] = "{}/{}".format(BASE_URL, item[2:])
            _items.append(vn_item)

        return _items


class PlantDetail(scrapy.Spider):
    name = "plant_detail"

    def start_requests(self):
        with open(os.path.join(PROJECT_ROOT, "result.csv")) as f:
            urls = [url.strip() for url in f.readlines()[1:]]

        for url in urls:
            # print url
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        image_folder = os.path.join(PROJECT_ROOT, IMAGES)
        if not os.path.isdir(image_folder):
            os.mkdir(image_folder)

        hxs = scrapy.Selector(response)

        id = re.search("ID=([0-9]{4})", response.url).group(1)

        imgs = hxs.select('//img[contains(@src, "plant")]/@src').extract()

        latin_species = hxs.select('//*[@id="Bdy"]/table[3]/tr[1]/td[2]/table/tr[2]/td/table/tr[2]/td/table[1]/tr[2]/td[2]/table[1]/tr[2]/td[2]/em/text()').extract_first()

        description = hxs.select('//*[@id="Bdy"]/table[3]/tr[1]/td[2]/table/tr[2]/td/table/tr[2]/td/table[1]/tr[5]/td/table/tr/td[2]').extract()
        description = remove_tags(description[0])
        description = re.sub(r"\r\n", "\n", description)
        description = re.sub(r"\xa0", "", description)
        description = re.sub(r"\s{2,}", " ", description)
        description = re.sub(r"New Page 1", "", description)
        description = re.sub(r"^ ", "", description)

        _imgs = [os.path.basename(img) for img in imgs]

        for img in imgs:

            img = re.sub(r"(_[0-9]{1,2})", r"\1s", img)

            _img_path = "{}/{}".format(BASE_URL, img[2:])
            save_path = os.path.join(PROJECT_ROOT, IMAGES, os.path.basename(img))

            if not os.path.exists(save_path):
                urllib.urlretrieve(_img_path, save_path)

        plant = PlantItem()
        plant["id"] = id
        plant["images"] = _imgs
        plant["species"] = latin_species
        plant["description"] = description

        yield plant
