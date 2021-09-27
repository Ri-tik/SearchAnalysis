import scrapy,csv
import pip._vendor.requests as request
from scrapy.http import TextResponse
from scrapy.linkextractors import LinkExtractor
from ..items import SearchanalysisItem

inp1 = input("Enter Show Name: ")
inp1 = "+".join(inp1.split())+"+imdb"
class GooglesearchSpider(scrapy.Spider):
    name = 'GoogleSearch'
    url1 = "https://search.aol.com/aol/search?q={}".format(inp1)
    start_urls = [url1]
    def parse(self, response):
        items = SearchanalysisItem()
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
        self.im_detailed_reviews = self.im_review_link.css(".show-more__control::text").extract()
        #self.im_detailReview = self.im_rating_link.css("").extract()        
        #self.display()
       
        items['imdbRate']=self.imdbRate
        items['rottRate']= self.rottRate
        items['imdbLink']= self.imdbLink
        items['rottLink']= self.rottLink
        items['imdb_rating_no']= self.im_rating_no
        items['imdb_rating_votes']= self.im_rating_votes
        items['imdb_reviews']= self.im_reviews
        items['im_detailed_reviews']=self.im_detailed_reviews
     
        yield items

        fieldnames1 = ['RatingNo','Votes']
        with open('ShowData','w') as f:
            writer = csv.DictWriter(f,fieldnames=fieldnames1)
            writer.writeheader()
            w=csv.writer(f)
            data = zip(items['imdb_rating_no'],items['imdb_rating_votes'])
            w.writerows(data)

        '''fieldnames2 = ['imdb_reviews']
        with open('ShowReviews','w') as f2:
            writer = csv.DictWriter(f2,fieldnames=fieldnames2)
            writer.writeheader()
            w=csv.writer(f2)
            data = items['imdb_reviews']
            w.writerows(data) '''

        with open("ShowReviews.txt", "w") as f2:
            f2.write("Show Reviews \n")
            f2.writelines(items['imdb_reviews'])
            f2.writelines(items['im_detailed_reviews'])

            
        print("Search Result Is Completed And Data Has Been Stored")
    #def display(self):
       # print("IMDB Rating:",self.imdbRate)
        #print("Rotten Rating:",self.rottRate)


        