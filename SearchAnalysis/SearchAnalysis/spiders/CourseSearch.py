import scrapy,csv
import pip._vendor.requests as request
from scrapy.http import TextResponse
from scrapy.linkextractors import LinkExtractor
from ..items import CourseItem

inp2 = input("Enter Course Name: ")
#inp1 = " ".join(inp1.split())+" course"

class CourseSearchSpider(scrapy.Spider):
    name = 'CourseSearch'
    #url1 = "https://search.aol.com/aol/search?q={}".format(inp1)
    courseInp = "https://www.classcentral.com/search?q={}&sort=rating-up&lang=english".format(inp2)
    #udemyInp = "https://www.udemy.com/topic/{}/".format(inp2)
    #udacityinp = "https://www.udacity.com/courses/all?search={}&sort=highest'%20'rated".format(inp2)
    start_urls = [courseInp]
    def parse(self, response):
        items = CourseItem()
        self.course_Title = response.css('.line-tight.margin-bottom-xxsmall::text').extract()
        self.course_Ratings = response.css("span::attr(aria-label)").extract()[1::]
        self.course_TotalReviews = response.css(".color-gray::text").extract()
        self.course_Provide = response.css('.color-charcoal.margin-left-small::text').extract()
        self.course_University = response.css(".block::attr(title)").extract()
        self.course_Description = response.css(".block.hover-no-underline::text").extract()[-21:-6]
        #self.course_Link = response.css(".rottenTomatoes a").xpath("@href").extract()[0]
        self.course_Links = response.css("a").xpath("@href").extract()
        self.course_Provider=[]
        for i in self.course_Provide:
            self.course_Provider.append(i.strip())
       
        items['course_Title']=self.course_Title
        items['course_Ratings']= self.course_Ratings
        items['course_TotalReviews']= self.course_TotalReviews
        items['course_Provider']= self.course_Provider
        items['course_University'] = self.course_University
        items['course_Description']= self.course_Description
     
        yield items

        fieldnames1 = ['Course Description','Course Provider','course_University','Course Ratings','Course Name','Total Reviews']
        with open('courseData','w') as f:
            writer = csv.DictWriter(f,fieldnames=fieldnames1)
            writer.writeheader()
            w=csv.writer(f)
            data = zip(items['course_Description'],items['course_Provider'],items['course_University'],items['course_Ratings'],items['course_Title'],items['course_TotalReviews'])
            w.writerows(data)
            
        print("Search Result Is Completed And Data Has Been Stored")
    #def display(self):
       # print("IMDB Rating:",self.imdbRate)
        #print("Rotten Rating:",self.rottRate)

        
        