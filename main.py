import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
from common import Common
import handlers

base_url = ""
page_parameter_name = ""
first_page = 1
last_page = 0
interval = 0
stop_condition = False

result_url_tag = ""
result_url_class = ""

#number of result pages processed
counter = 0

#datetime of the crawler initiation
crawl_start_time = datetime.today()

#loads config file
def load_config(config_file_path):
    with open(config_file_path) as config_file:
        data = json.load(config_file)

    global base_url, page_parameter_name, first_page, last_page, interval, stop_condition, result_url_tag, result_url_class
    base_url = data['base_url']
    page_parameter_name = data['page_parameter_name']
    first_page = data['first_page']
    #if last_page is 0 and there is no stop condition the crawler will run till there is no results on page
    last_page = data['last_page']
    interval = data['interval']
    #if stop condition is set to true the stop_condition_handler function will run at the end of crawl of each page
    stop_condition = data['stop_condition']
    result_url_tag = data['result_url_tag']
    result_url_class = data['result_url_class']

def crawl():
    global base_url, page_parameter_name, first_page, last_page, interval, stop_condition, result_url_tag, result_url_class, counter
    stop_condition_reached = False
    current_page = first_page
    #if last page was 0 (not defined) we set it to large number so the loop condition makes sense
    if last_page == 0:
        last_page = 100000
    while (stop_condition_reached == False and current_page <= last_page):
        time.sleep(interval)
        #request results page
        current_url = base_url + "&" + page_parameter_name + "=" + str(current_page)
        response = requests.get(current_url, headers = {"User-Agent" : Common.get_user_agent()})
        response_text = response.text
        response_text = " ".join(response_text.split())
        soup = BeautifulSoup(response_text, features="html.parser")
        #extract result urls
        result_urls = soup.find_all(result_url_tag, {"class" : result_url_class})
        for result_url in result_urls:
            #result url handler checks if the result url is valid
            #it can modify the url or set it to empty string to skip the result
            #by default it just returnes the ["href"] of the result_url
            result_url_href = handlers.result_url_handler(result_url)
            if result_url_href != "":
                result_response = requests.get(result_url_href, headers = {"User-Agent" : Common.get_user_agent()})
                result_response_text = result_response.text
                result_response_text = " ".join(result_response_text.split())
                result_soup = BeautifulSoup(result_response_text, features="html.parser")
                extract_data(result_soup)
                #result page processing can be extended by adding code to the result_page_processing_handler function
                #by default is does not do anything
                handlers.result_page_processing_handler(result_soup)
                counter += 1
                #if the stop condition is used run stop_condition_handler
                if stop_condition == True:
                    stop_condition_reached = handlers.stop_condition_handler(result_soup)
            #if the stop condition is reached then end crawling
            if stop_condition_reached == True:
                break
        current_page += 1

def extract_data(result_soup):
    print("shit")

def main(config_file_path):
    load_config(config_file_path)
    crawl()
    print(counter)


if __name__ == '__main__':
    config_file_path = "config.json"

main(config_file_path)