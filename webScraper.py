from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
import pandas as pd

def edmundWebScraper(url, pages):
    """
    Scrape Data from a given forum on Edmund's
    :param url: url of page one of Edmund forum
           pages: number of pages of forum to scrape
    :return: returns a pandas dataframe of comments
    """
    # Initialize Driver
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    driver.get(url)

    # Create Empty Dataframe
    comments = pd.DataFrame(columns=['Date', 'user_id', 'comments'])
    for i in range(pages):
        print(i)
        page_comments = scrapePageComments(driver)
        comments = comments.append(page_comments)
        driver.find_element_by_class_name('Next').click()

    return comments


def scrapePageComments(driver):
    """
    Scrape Data from a given page of a forum on Edmund's
    :param driver: webdriver
    :return: returns a pandas dataframe of comments
    """
    page_comments = pd.DataFrame(columns=['Date', 'user_id', 'comments'])
    ids = driver.find_elements_by_xpath("//*[contains(@id,'Comment_')]")

    comment_ids = []
    for i in ids:
        comment_ids.append(i.get_attribute('id'))

    for x in comment_ids:
        # Extract dates from for each user on a page
        user_date = driver.find_elements_by_xpath('//*[@id="' + x + '"]/div/div[2]/div[2]/span[1]/a/time')[0]
        date = user_date.get_attribute('title')

        # Extract user ids from each user on a page
        userid_element = driver.find_elements_by_xpath('//*[@id="' + x + '"]/div/div[2]/div[1]/span[1]/a[2]')[0]
        userid = userid_element.text

        # Extract Message for each user on a page
        user_message = driver.find_elements_by_xpath('//*[@id="' + x + '"]/div/div[3]/div/div[1]')[0]
        comment = user_message.text

        # Adding date, userid and comment for each user in a dataframe
        page_comments.loc[len(page_comments)] = [date, userid, comment]

    return page_comments






