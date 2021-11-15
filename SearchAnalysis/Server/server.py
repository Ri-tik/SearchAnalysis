from flask import Flask, render_template

from SearchAnalysis.SearchAnalysis.spiders.CourseSearch import CourseSearchSpider
from SearchAnalysis.SearchAnalysis.spiders.GoogleSearch import GooglesearchSpider
app = Flask(__name__)

import scrapy,csv
import pip._vendor.requests as request
from scrapy.http import TextResponse
from scrapy.linkextractors import LinkExtractor
import SearchAnalysis.SearchAnalysis.items as SI


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/my-link/')
def run(butn):
    if butn == "Course":
        return CourseSearchSpider
    else:
        return GooglesearchSpider