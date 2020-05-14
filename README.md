# www_data_collector
This is a piece of python code that aims to facilitate extraxtion of arbitrary data from websites.
It can be used to extract specific data from websites that present search results to users in a form of hyperlinks list (e.g. ecommerce sites, catalogs, web archives)
The tool crawls through the result pages and uses BeautifulSoup's HTML parser to collect pieces of information specified in the JSON config file.
Collected data is stored in a JSON format and saved to file. 
Typically, the data requires cleaning and removing artefacts that are present in HTML before it can be stored in a database. 
This means that another use-case specifi script needs to be prepared to process collected data.
Alternatively, www_data_collector can be extended by adding code to the three handler functions (handlers.py):
* result_url_handler - Run before data collection from each resultpage. It is intended to verify or modify result page URL if needed.
* result_page_processing_handler - Run after each data collection. It is intended extend data collection for more complex cases (potentially adding subsequent requests based on the results from each page).
* stop_condition_handler - Run after each data collection. By default returnes False so the crawler loop does not stop (it stops eventually when there are no more result links available). It is intended to define arbitrary stop condition. Useful when the results are sorted chronologically and we know we only have to crawl new results.