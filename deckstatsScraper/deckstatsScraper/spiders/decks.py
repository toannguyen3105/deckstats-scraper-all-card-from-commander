import scrapy
from scrapy.loader import ItemLoader
from deckstatsScraper.items import DeckstatsscraperItem


class DecksSpider(scrapy.Spider):
    name = 'decks'
    allowed_domains = ['deckstats.net']
    start_urls = ['https://deckstats.net/decks/search/?search_tags=Commander&lng=en&page=1']

    def parse(self, response):
        cardLinks = response.xpath('//table[@class="decks_list"]//td[contains(@class, "deck_row")]//a')
        for link in cardLinks:
            loader = ItemLoader(item=DeckstatsscraperItem(), selector=link)
            relative_url = link.xpath("./@href").extract_first()
            absolute_url = "{}?include_comments=1&do_not_include_printings=0&export_txt=1&share_key=".format(
                relative_url)
            file_name = link.xpath("./text()").extract_first().strip()
            s1 = file_name.replace("/", "").replace("//", "")

            loader.add_value("file_urls", absolute_url)
            loader.add_value("file_name", s1)
            yield loader.load_item()

        next_page_url = response.xpath(
            '//div[contains(@class, "page_button_buttonset")]//a[contains(text(),">")]/@href').extract_first()

        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
