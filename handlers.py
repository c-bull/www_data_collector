from bs4 import BeautifulSoup

def result_url_handler(result_url):
    #default return value is href of the result tag (typically result tag is an <a>)
    #comment and write your own code if needed
    #for example something like this
    #return result_url.find("a")["href"]
    return result_url["href"]


def result_page_processing_handler(result_soup):
    pass

def stop_condition_handler(result_soup):
    return False