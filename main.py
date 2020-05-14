import json
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from tld import get_tld
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
visit_results_with_different_domain = False

items_to_extract = ""

#number of result pages processed
counter = 0

#datetime of the crawler initiation
crawl_start_time = datetime.today()

#loads config file
def load_config(config_file_path):
    with open(config_file_path) as config_file:
        config_file_json = json.load(config_file)

    global base_url, page_parameter_name, first_page, last_page, interval, stop_condition, result_url_tag, result_url_class, items_to_extract, visit_results_with_different_domain
    base_url = config_file_json['base_url']
    page_parameter_name = config_file_json['page_parameter_name']
    first_page = config_file_json['first_page']
    #if last_page is 0 and there is no stop condition the crawler will run till there is no results on page
    last_page = config_file_json['last_page']
    interval = config_file_json['interval']
    #if stop condition is set to true the stop_condition_handler function will run at the end of crawl of each page
    stop_condition = config_file_json['stop_condition']
    result_url_tag = config_file_json['result_url_tag']
    result_url_class = config_file_json['result_url_class']
    items_to_extract = config_file_json['items_to_extract']
    visit_results_with_different_domain = config_file_json['visit_results_with_different_domain']

def crawl():
    global last_page, counter
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
            #now check if the results page is on domain other thatn the one we are crawling
            if visit_results_with_different_domain == False:
                if get_tld(result_url_href, as_object=True).domain != get_tld(base_url, as_object=True).domain:
                    continue
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
    for item in items_to_extract:
        #three types of filters are supported: tag, regex, sieve
        #first: tag name with specific attributes.
        if item["filter_type"] == "tag":
            try:
                #some objects created by bs4 have "content"
                print(result_soup.find(item["html_tag_name"], {item["html_tag_attr_name"] : item["html_tag_attr_value"]})["content"])
                continue
            except:
                pass
            try:
                #and some have .text
                print(result_soup.find(item["html_tag_name"], {item["html_tag_attr_name"] : item["html_tag_attr_value"]}).text)
                continue
            except:
                pass
            print("Item '" + item["name"] + "' not found")
        #second: tag name with regex. regex is applied to string inside a tag.
        if item["filter_type"] == "regex":
            try:
                print(result_soup.find(item["html_tag_name"], string=re.compile(item["regex_string"])).text)
                continue
            except:
                pass
            try:
                print(result_soup.find(item["html_tag_name"], string=re.compile(item["regex_string"])).text)
                continue
            except:
                pass
            print("Item '" + item["name"] + "' not found")
        #third: sieve selector consisting series of tags used to traverse the document.
        if item["filter_type"] == "sieve":
            try:
                for found_item in result_soup.select(item["sieve_selector"]):
                    print(found_item["content"])
                continue
            except:
                pass
            try:
                for found_item in result_soup.select(item["sieve_selector"]):
                    print(found_item.text)
                continue
            except:
                pass
            print("Item '" + item["name"] + "' not found")

def main(config_file_path):
    load_config(config_file_path)
    crawl()
    print(counter)


if __name__ == '__main__':
    config_file_path = "config.json"

main(config_file_path)