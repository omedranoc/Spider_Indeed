from scrapy import Spider
from scrapy.selector import Selector
from pandas import Series, DataFrame
from stack.items import StackItem
import re

class StackSpider(Spider):
    name = "stack"
    allowed_domains = ["indeed.com"]
    start_urls = [
        "http://www.indeed.com/jobs?q=junior&l=United+States&sort=date"
    ]
    pagination=[10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200]
    for x in pagination:
      x="http://www.indeed.com/jobs?q=junior&l=United+States&sort=date&start="+str(x)

      start_urls.append(x)

    def parse(self, response):
        questions = Selector(response).css('#resultsCol')
       
        #print questions
        table = [[1 , 2], [3, 4]]
        jobTitle=questions.css('a[data-tn-element="jobTitle"]::attr(title)').extract()
        summary= questions.css('.summary').extract()
        date =questions.css('div.result-link-bar-container > div > span.date::text').extract()
        place= questions.css('.location::text,span[itemprop="addressLocality"]::text').extract()
        
        easytoapply= questions.css('.result table').extract()

        easytoaplyvec=[]
        
        for e in easytoapply:
                
               if "iaP" in e:
                  easytoaplyvec.append(1)
               else:
                  easytoaplyvec.append(0)
              
        summary1=[]
        
        for jobn in summary:
            nourls = re.sub("(\S[A-Za-z0-9]+@\S+)|(#\S+)|(w{3}\S+)|(\w+:\/\/\S+)|([^0-9A-Za-z \t])|(\S+(\.com))", " ", jobn)
            summary1.append(nourls)
      
        print "place",len(place),len(jobTitle),len(summary1),len(date),len(easytoaplyvec) 
        frame = DataFrame({'title':jobTitle, 'summary':summary1,'date':date , 'easy':easytoaplyvec, 'place':place},columns=['title', 'summary','date', 'easy','place'])
        
        
        for question in questions:
            item = StackItem()
            
            
            item['title'] = question.css('a[data-tn-element="jobTitle"]::text').extract()
            
        
        with open(r'out14.csv', 'a') as f:
                   frame.to_csv(f, encoding='utf-8',header=False)
        
        yield item