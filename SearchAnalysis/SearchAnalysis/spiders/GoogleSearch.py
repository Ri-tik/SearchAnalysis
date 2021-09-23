import scrapy
import pip._vendor.requests as request
from scrapy.http import TextResponse
from scrapy.linkextractors import LinkExtractor

inp1 = input("Enter Show Name: ")
inp1 = "+".join(inp1.split())+"+TV"
class GooglesearchSpider(scrapy.Spider):
    name = 'GoogleSearch'
    url1 = "https://search.aol.com/aol/search?q={}".format(inp1)
    start_urls = [url1]
    def parse(self, response):
        self.imdbRate = response.css('.imdb::text').extract()[0]
        self.rottRate = response.css('.rottenTomatoes::text').extract()[0]
        self.imdbLink = response.css(".imdb a").xpath("@href").extract()[0]
        self.rottLink = response.css(".rottenTomatoes a").xpath("@href").extract()[0]
        self.links = response.css(".lh-17::text").extract()
        for i in self.links:
            if i.startswith("/title"):
                self.imdbLink = "https://www.imdb.com"+i
                break
        rateUrl = self.imdbLink+'/ratings/'
        rateResp = request.get(rateUrl)
        reviewUrl = self.imdbLink+'/reviews'
        reviewResp = request.get(reviewUrl)

        self.im_rating_link = TextResponse(body=rateResp.content, url=rateUrl)
        self.im_rating_no = self.im_rating_link.css(".rightAligned::text").extract()
        self.im_rating_votes = self.im_rating_link.css("tr :nth-child(3) .leftAligned::text").extract()

        self.im_review_link = TextResponse(body=reviewResp.content, url=reviewUrl)
        self.im_reviews = self.im_review_link.css(".title::text").extract()
        #self.im_detailReview = self.im_rating_link.css("").extract()        
        #self.display()
        yield {
            'imdbRate':self.imdbRate,
            'rottRate': self.rottRate,
            'imdbLink': self.imdbLink,
            'rottLink': self.rottLink,
            'imdb_rating_no': self.im_rating_no,
            'imdb_rating_votes': self.im_rating_votes,
            'imdb_reviews': self.im_reviews
            }
    #def display(self):
       # print("IMDB Rating:",self.imdbRate)
        #print("Rotten Rating:",self.rottRate)


        