# -*- coding: utf-8 -*-
import scrapy


class LoginSpider(scrapy.Spider):
    name = 'login'
    login_url = 'http://quotes.toscrape.com/login'
    start_urls = [login_url]

    def parse(self, response):
        token = response.css('input[name="csrf_token"]::attr(value)').extract_first()

        data = {
            'csrf_token': token,
            'username': 'abc',
            'password': 'abc',
        }

        yield scrapy.FormRequest(url=self.login_url, formdata=data, callback=self.parse_quotes)

    def parse_quotes(self, response):
        for quote in response.css('div.quote'):
            item = {
                'author_name': quote.css('small.author::text').extract_first(),
                'text': quote.css('span.text::text').extract_first(),
                'tags': quote.css('a.tag::text').extract(),
            }
            yield item

