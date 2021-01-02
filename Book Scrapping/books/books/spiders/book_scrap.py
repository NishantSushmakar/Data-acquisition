# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 18:30:29 2021

@author: nishant
"""
import scrapy

class BookSpider(scrapy.Spider):
    name = "book"
    
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'output.csv'
    }
    def start_requests(self):
        urls = [
            "http://books.toscrape.com/catalogue/page-1.html",
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        
        for q in response.css("article.product_pod"):
            
            
            yield {
               'image_url' : q.css("img::attr(src)").get(),
               'book_title' : q.css("h3 a::attr(title)").get(),
               'product_price' : q.css('p.price_color::text').get(),
            
                }
                
        next_page = response.css("li.next a::attr(href)").get()
        
        if next_page is not None :
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page,callback=self.parse)
       