# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SearchanalysisItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    imdbRate=scrapy.Field()
    rottRate=scrapy.Field()
    imdbLink=scrapy.Field()
    rottLink=scrapy.Field()
    imdb_rating_no=scrapy.Field()
    imdb_rating_votes= scrapy.Field()
    imdb_reviews= scrapy.Field()
    im_detailed_reviews=scrapy.Field()

class CourseItem(scrapy.Item):
    course_Title=scrapy.Field()
    course_Ratings=scrapy.Field()
    course_TotalReviews=scrapy.Field()
    course_Provider=scrapy.Field()
    course_University=scrapy.Field()
    course_Description=scrapy.Field()
