import scrapy
from quotes_js_scraper.items import QuoteItem
from scrapy_playwright.page import PageMethod


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    # allowed_domains = ['quotes.toscrape.com']
    # start_urls = ['http://quotes.toscrape.com/']

    def start_requests(self):
        # url = "https://quotes.toscrape.com/js/"
        url = "https://quotes.toscrape.com/scroll"
        # yield scrapy.Request(url, meta={'playwright': True})
        # playwright waits for page to load and scrapy crawl quotes -O result.json
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_methods=[
                PageMethod('wait_for_selector', 'div.quote'),
                # for long pages
                # PageMethod('evaluate', "window.scrollBy(0, document.body.scrollHeight)"),
                # PageMethod("wait_for_selector", "div.quote:nth-child(11)"),  # 10 per page
            ],
            errback=self.errback
        ))

    async def parse(self, response):
        page = response.meta['playwright_page']
        
        screenshot = await page.screenshot(path="screenshot.png", full_page = True)
        await page.close()

# ***************************************************************************
# # Not needed for taking screen shots
#         for quote in response.css('div.quote'):
#             quote_item = QuoteItem()
#             quote_item['text'] = quote.css('span.text::text').get()
#             quote_item['author'] = quote.css('small.author::text').get()
#             quote_item['tags'] = quote.css('div.tags a.tag::text').get()
#             yield quote_item
# ****************************************************************************

        # To scrape next pages
        # next_page = response.css('.next>a ::attr(href)').get()
        # if next_page is not None:
        #     next_page_url = 'http://quotes.toscrape.com' + next_page
        #     yield scrapy.Request(next_page_url, meta=dict(
        #         playwright=True,
        #         playwright_include_page=True,
        #         playwright_page_methods=[
        #             PageMethod('wait_for_selector', 'div.quote')
        #         ],
        #         errback=self.errback
        #     ))

    async def errback(self, failure):
        page = failure.request.meta("playwright_page")
        await page.close()
