# www_data_collector
This is a piece of python code that aims to facilitate extraction of arbitrary data from websites.
It can be used to extract specific data from websites that present search results to users in a form of hyperlinks list (e.g. ecommerce sites, catalogs, web archives).
The tool crawls through the result pages and uses BeautifulSoup's HTML parser to collect pieces of information specified in the JSON config file.
Collected data is stored in a JSON format and saved to file. 
Typically, the data requires cleaning and removing artefacts that are present in HTML before it can be stored in a database. 
This means that another use-case specific script needs to be prepared to process collected data.
Alternatively, www_data_collector can be extended by adding code to the three handler functions (handlers.py):
* result_url_handler - Run each time before data is collected from a result page. It is intended to verify or modify result page URL if needed.
* result_page_processing_handler - Run after each data collection. It is intended extend data collection for more complex cases (potentially adding subsequent requests based on the collected data).
* stop_condition_handler - Run after each data collection. By default it returnes False, so the crawler loop does not stop (it stops eventually when there are no more result links available). It is intended to define arbitrary stop condition. Useful when the results are sorted chronologically and we know we only have to crawl new results.

# Usage example
Let's say we want to collect data of bimmers that pop up on ebay. We first have to find the URL, so we search BMWs on ebay and sort by "newly listed".

![Alt text](/readme_img/img1.png)

Next, we have to go to the next page of the results to find out the page_parameter_name. In this case it is "_pgn".

![Alt text](/readme_img/img2.png)

So far, our config file looks like this:
```
{
    "base_url": "https://www.ebay.com/b/BMW-Cars-and-Trucks/6001/bn_24017016?rt=nc&_sop=10",
    "page_parameter_name": "_pgn"
}
```
Now, let's inspect the result hyperlink and see what is the CSS class name of the "a" tag. In this case it is "s-item__link".

![Alt text](/readme_img/img3.png)

Config file:
```
{
    "base_url": "https://www.ebay.com/b/BMW-Cars-and-Trucks/6001/bn_24017016?rt=nc&_sop=10",
    "page_parameter_name": "_pgn",
    "result_url_tag": "a",
    "result_url_class": "s-item__link"
}
```
We now visit a sample page from the result list. We will start collecting data with the title of the offer and link to image. This info is usually present in meta tags. BTW meta tags often have "content" attribute defined. To extract value of this attribute we can use "attr_to_extract" option in the config file.

![Alt text](/readme_img/img4.png)

We are adding two "items_to_extract" with filter type "tag" to our config:
```
"items_to_extract": [
    {
        "filter_type" : "tag",
        "name": "title",
        "html_tag_name": "meta",
        "html_tag_attr_name": "property",
        "html_tag_attr_value": "og:title",
        "attr_to_extract" : "content"
    },
    {
        "filter_type" : "tag",
        "name": "image",
        "html_tag_name": "meta",
        "html_tag_attr_name": "property",
        "html_tag_attr_value": "og:image",
        "attr_to_extract" : "content"
    },
]
```
Let's collect the price as well. It is rendered as a "span" tag with id "prcIsum", which should be unique in the scope of this page.

![Alt text](/readme_img/img5.png)

Adding price item:
```
"items_to_extract": [
    {
        "filter_type" : "tag",
        "name": "price",
        "html_tag_name": "span",
        "html_tag_attr_name": "id",
        "html_tag_attr_value": "prcIsum"
    }
]
```
We are also interested in the vehicle specification. It is presented in a table. 

![Alt text](/readme_img/img6.png)

Since the parameters listed in the table do not have unique tags which we can reference, we will use a Soup Sieve. It basically tells the program how to traverse the document to access the elements we are interested in. At the bottom of the developers tools there is a path to the tag we are currently inspecting. Our job is to convert it to a sieve_selector.

![Alt text](/readme_img/img7.png)

Adding sieve item to config:
```
"items_to_extract": [
    {
        "filter_type" : "sieve",
        "name": "vehicle_parameter",
        "sieve_selector": "html body div.tabbable div.tab-content-m div.vi-VR-tabCnt div.section table tr td span"
    }
]
```
Finished config file:
```
{
    "base_url": "https://www.ebay.com/b/BMW-Cars-and-Trucks/6001/bn_24017016?rt=nc&_sop=10",
    "page_parameter_name": "_pgn",
    "first_page": 1,
    "last_page": 3,
    "interval": 0,
    "result_url_tag": "a",
    "result_url_class": "s-item__link",
    "visit_results_with_different_domain" : false,
    "output_file" : "output.json",
    "verbose" : true,
    "items_to_extract": [
        {
            "filter_type" : "tag",
            "name": "title",
            "html_tag_name": "meta",
            "html_tag_attr_name": "property",
            "html_tag_attr_value": "og:title",
            "attr_to_extract" : "content"
        },
        {
            "filter_type" : "tag",
            "name": "image",
            "html_tag_name": "meta",
            "html_tag_attr_name": "property",
            "html_tag_attr_value": "og:image",
            "attr_to_extract" : "content"
        },
        {
            "filter_type" : "tag",
            "name": "price",
            "html_tag_name": "span",
            "html_tag_attr_name": "id",
            "html_tag_attr_value": "prcIsum"
        },
        {
            "filter_type" : "sieve",
            "name": "vehicle_parameter",
            "sieve_selector": "html body div.tabbable div.tab-content-m div.vi-VR-tabCnt div.section table tr td span"
        }
    ]
}
```
Output should look like this:
![Alt text](/readme_img/img8.png)