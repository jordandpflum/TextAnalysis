from webScraper import edmundWebScraper
from replaceModelWBrand import replaceModelWBrand
from MDS import MDS
from calculateLift import calculateLift

url = 'https://forums.edmunds.com/discussion/3941/general/x/i-spotted-a-new-insert-make-model-today'
pages = 200
comments = edmundWebScraper(url, pages)
comments.to_csv("results.csv")