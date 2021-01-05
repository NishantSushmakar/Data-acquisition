# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 13:36:02 2021

@author: nishant
"""
import scrapy
import json
import os 
import requests

class PepperSpider(scrapy.Spider):
    
    name = "pepper_spider"
    BASE_DIR = './pepper_fry_data/'
    MAX_CNT = 10
    
    
    def start_requests(self):
        
        BASE_URL = "https://www.pepperfry.com/site_product/search?q="
    
        products = ["arm chairs","bean bags","bench","book cases","chest drawers","coffee table",
                    "dinning set","garden seating","king beds","queen beds","two seater sofa"]
        
        urls = []
        dir_names = []
        
        for product in products :
            
            s = '+'.join(product.split())
            dir_name = '-'.join(product.split())
            dir_names.append(dir_name)
            urls.append(BASE_URL+s)
            
        for i in range(len(urls)):
            d = {
                'dir_name':dir_names[i]
                
                }
            resp = scrapy.Request(url=urls[i],callback=self.parse,dont_filter=True)
            resp.meta['dir_name']=dir_names[i]
             
            yield resp
            
    
    def parse(self, response,**meta):
        
        count = 0 
        
        q = response.css("a.clip-prd-dtl")
        product_list = q.css("a::attr(href)").getall()
        
        for link in product_list:
            resp = scrapy.Request(url=link,callback=self.product_parse,dont_filter=True)
            resp.meta['dir_name'] = response.meta['dir_name']
            
            
            
            if count == self.MAX_CNT:
                break
            
            if not resp == None:
                count += 1
            
            yield resp
            
            
    def product_parse(self,response,**meta):
        
        product_name = response.css("h1::text").get()
        product_price = response.css("span.v-price-mrp-amt::text").get()
        q = response.css("div.v-prod-comp-dtls-list")
        product_detail = " ".join(q.css('span::text').getall())
      #  product_detail = json.load(product_detail)
        
        img_url = response.css("a::attr(data-hoverimg)").getall()
        
        if (len(img_url)>3):
            d = {
                'Product Name':product_name,
                'Product Price':product_price,
                'Product Detail':product_detail,
                }
        
            CATEGORY_NAME = response.meta['dir_name']
            ITEM_DIR_URL = os.path.join(self.BASE_DIR,os.path.join(CATEGORY_NAME,product_name))
            if not os.path.exists(ITEM_DIR_URL):
                os.makedirs(ITEM_DIR_URL)
                
            with open(os.path.join(ITEM_DIR_URL,'metadata.txt'),'w') as f:
                json.dump(d,f)
            
            for i,url in enumerate(img_url):
                r = requests.get(url)
                
                with open(os.path.join(ITEM_DIR_URL,'image_{}.jpg'.format(i)),'wb') as f:
                    f.write(r.content)
                    
            print("-->Done"+product_name+"data at:"+ITEM_DIR_URL)
            
            yield d
            
            
        yield None
        
        
        
        