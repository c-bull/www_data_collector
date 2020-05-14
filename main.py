import json
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from tld import get_tld
import time
import uuid
from common import Common
import handlers


#number of result pages processed
counter = 0

#datetime of the crawler initiation
crawl_start_time = datetime.today()

output = {}

#loads config file
def load_config(config_file_path):
    with open(config_file_path) as config_file:
        config_file_json = json.load(config_file)

    global base_url, page_parameter_name, first_page, last_page, interval, result_url_tag, result_url_class, items_to_extract, visit_results_with_different_domain, output_file, verbose
    if "base_url" in config_file_json:
        base_url = config_file_json["base_url"]
    else:
        print("Base URL not present in the config file. Quitting.")
        quit()
    if "page_parameter_name" in config_file_json:
        page_parameter_name = config_file_json["page_parameter_name"]
    else:
        print("Page parameter name not present in the config file. Quitting.")
        quit()  
    if "first_page" in config_file_json:
        first_page = config_file_json["first_page"]
    else:
        first_page = 1
    #if last_page is 0 and there is no stop condition the crawler will run until there are no results on current page
    if "last_page" in config_file_json:
        last_page = config_file_json["last_page"]
    else:
        last_page = 0
    if "interval" in config_file_json:
        interval = config_file_json["interval"]
    else:
        print("Warning: default interval of 0 seconds is used.")
        interval = 0
    if "result_url_tag" in config_file_json:
        result_url_tag = config_file_json["result_url_tag"]
    else:
        result_url_tag = "a"
    if "result_url_class" in config_file_json:
        result_url_class = config_file_json["result_url_class"]
    else:
        print("Result URL class not specified in the config file. Quitting.")
    #there might be no items to extract specified
    #still the crawler will run and handlers might be used to extract relevant data
    if "items_to_extract" in config_file_json:
        items_to_extract = config_file_json["items_to_extract"]
    else:
        items_to_extract = []
    #by default we only visit result pages on the crawled domain
    if "visit_results_with_different_domain" in config_file_json:
        visit_results_with_different_domain = config_file_json["visit_results_with_different_domain"]
    else:
        visit_results_with_different_domain = False
    if "verbose" in config_file_json:
        verbose = config_file_json["verbose"]
    else:
        verbose = False
    if "output_file" in config_file_json:
        output_file = config_file_json["output_file"]
    else:
        print("No output file specified. Everything will be preinted to the screen.")
        output_file = ""
        verbose = True

def crawl():
    global last_page, counter, output
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
        #stop if there are no more results
        if result_urls == []:
            break
        for result_url in result_urls:
            #result url handler checks if the result url is valid
            #it can modify the url or set it to empty string to skip the result
            #by default it just returnes the ["href"] of the result_url
            result_url_href = handlers.result_url_handler(result_url)
            #now check if the results page is on domain other thatn the one we are crawling
            if visit_results_with_different_domain == False:
                if get_tld(result_url_href, as_object=True).domain != get_tld(base_url, as_object=True).domain:
                    continue
            if verbose:
                print(result_url_href)
            #adding result to output
            current_uuid = uuid.uuid4().__str__()
            output[current_uuid] = {"url":result_url_href}
            if result_url_href != "":
                result_response = requests.get(result_url_href, headers = {"User-Agent" : Common.get_user_agent()})
                result_response_text = result_response.text
                result_response_text = " ".join(result_response_text.split())
                result_soup = BeautifulSoup(result_response_text, features="html.parser")
                extract_data(result_soup, current_uuid)
                if verbose:
                    print()
                #result page processing can be extended by adding code to the result_page_processing_handler function
                #by default is does not do anything
                handlers.result_page_processing_handler(result_soup)
                counter += 1
                stop_condition_reached = handlers.stop_condition_handler(result_soup)
            #if the stop condition is reached then end crawling
            if stop_condition_reached == True:
                break
        if verbose:
            print("Page " + str(current_page) + " crawled.")
        current_page += 1

def extract_data(result_soup, current_uuid):
    global output
    for item in items_to_extract:
        #three types of filters are supported: tag, regex, sieve
        #first: tag name with specific attributes.
        if item["filter_type"] == "tag":
            #check if the value to be collected is a tag attribute
            #this requires specifing attr_to_extract in the config file
            if "attr_to_extract" in item:
                try:
                    value = result_soup.find(item["html_tag_name"], {item["html_tag_attr_name"] : item["html_tag_attr_value"]})[item["attr_to_extract"]]
                    if verbose:
                        print(value)
                    output[current_uuid][item["name"]] = value
                    continue
                except:
                    pass
            #by default we are trying to collect .text inside a tag
            try:
                value = result_soup.find(item["html_tag_name"], {item["html_tag_attr_name"] : item["html_tag_attr_value"]}).text
                if verbose:
                    print(value)
                output[current_uuid][item["name"]] = value
                continue
            except:
                pass
            if verbose:
                print("Item '" + item["name"] + "' not found")
        #second: tag name with regex. regex is applied to string inside a tag.
        if item["filter_type"] == "regex":
            #check if the value to be collected is a tag attribute
            #this requires specifing attr_to_extract in the config file
            if "attr_to_extract" in item:
                try:
                    value = result_soup.find(item["html_tag_name"], string=re.compile(item["regex_string"]))[item["attr_to_extract"]]
                    if verbose:
                        print(value)
                    output[current_uuid][item["name"]] = value
                    continue
                except:
                    pass
            #by default we are trying to collect .text inside a tag
            try:
                value = result_soup.find(item["html_tag_name"], string=re.compile(item["regex_string"])).text
                if verbose:
                    print(value)
                output[current_uuid][item["name"]] = value
                continue
            except:
                pass
            if verbose:
                print("Item '" + item["name"] + "' not found")
        #third: sieve selector consisting series of tags used to traverse the document.
        if item["filter_type"] == "sieve":
            #check if the value to be collected is a tag attribute
            #this requires specifing attr_to_extract in the config file
            if "attr_to_extract" in item:
                try:
                    for i, found_item in enumerate(result_soup.select(item["sieve_selector"])):
                        if verbose:
                            print(found_item[item["attr_to_extract"]])
                        output[current_uuid][item["name"] + str(i)] = found_item[item["attr_to_extract"]]
                    continue
                except:
                    pass
            #by default we are trying to collect .text inside a tag
            try:
                for i, found_item in enumerate(result_soup.select(item["sieve_selector"])):
                    if verbose:
                        print(found_item.text)
                    output[current_uuid][item["name"] + str(i)] = found_item.text
                continue
            except:
                pass
            if verbose:
                print("Item '" + item["name"] + "' not found")

def main(config_file_path):
    load_config(config_file_path)
    output["base_url"] = base_url
    output["page_parameter_name"] = page_parameter_name
    output["firs_page"] = first_page
    output["last_page"] = last_page
    output["start_time"] = crawl_start_time.__str__()
    crawl()
    with open(output_file, 'w') as f:
        json.dump(output, f)
    if verbose:
        print("Finished. Crawled " + str(counter) + " result pages.")


if __name__ == '__main__':
    config_file_path = "config.json"

main(config_file_path)