from webScraper import edmundWebScraper
from replaceModelWBrand import replaceModelWBrand
from MDS import MDS
from calculateLift import calculateLift

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
import pandas as pd

url = 'https://forums.edmunds.com/discussion/3941/general/x/i-spotted-a-new-insert-make-model-today'
pages = 336
comments = edmundWebScraper(url, pages)
comments.to_csv("results.csv")