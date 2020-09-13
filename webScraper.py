from selenium import webdriver, common
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
import pandas as pd
import sys

def edmundWebScraper(url, pages):
    """
    Scrape Data from a given forum on Edmund's
    :param url: url of page one of Edmund forum
           pages: number of pages of forum to scrape
    :return: returns a pandas dataframe of comments
    """
    # Initialize Driver
    driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
    driver.set_page_load_timeout(60)
    driver.get(url)

    # Create Empty Dataframe
    comments = pd.DataFrame()
    for i in range(1, pages+1):
        sys.stdout.write('\r')
        sys.stdout.write('Percent Complete:  ' + str(round((i / (pages + 1)) * 100, 2)) + '%' + ', Page: ' + str(i))
        sys.stdout.flush()
        url = f'{url}/p{i}'
        try:
            page_comments = scrapePageComments(driver, url)
            comments = comments.append(page_comments)
        except common.exceptions.TimeoutException:
            continue

        driver.find_element_by_class_name('Next').click()

    return comments


def scrapePageComments(driver, url):
    """
    Scrape Data from a given page of a forum on Edmund's
    :param driver: webdriver
    :return: returns a pandas dataframe of comments
    """
    # Create Empty containers for Values
    c_dates = []
    c_texts = []
    c_authors = []

    # Update Driver
    driver.get(url)
    # Retrieve Comments
    ul_comments = driver.find_elements_by_xpath('//*[@id="Content"]/div[4]/div[1]/ul')[0]
    comments = ul_comments.find_elements_by_tag_name('li')
    for comment in comments:
        try:
            comment_id = comment.get_attribute('id')[8:]
            # If Block Quote
            if comment.find_elements_by_xpath(f'//*[@id="Comment_{comment_id}"]/div/div[3]/div/div[1]/blockquote'):
                element = driver.find_element_by_tag_name('blockquote')
                driver.execute_script("""
                  var element = arguments[0];
                  element.parentNode.removeChild(element);
                  """, element)
                text = comment.find_element_by_xpath(f'//*[@id="Comment_{comment_id}"]/div/div[3]/div/div[1]').text
            # If not block quote
            else:
                text = comment.find_elements_by_xpath(f'//*[@id="Comment_{comment_id}"]/div/div[3]/div/div[1]')[0].text
            date = comment.find_element_by_xpath(f'//*[@id="Comment_{comment_id}"]/div/div[2]/div[2]/span/a/time').get_attribute('datetime')
            author = comment.find_element_by_xpath(f'//*[@id="Comment_{comment_id}"]/div/div[2]/div[1]/span[1]/a[2]').text
            c_dates.append(date)
            c_authors.append(author)
            c_texts.append(text)
        except IndexError:
            continue
        except common.exceptions.StaleElementReferenceException:
            continue
    return {'date': c_dates, 'author': c_authors, 'text': c_texts}






