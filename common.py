import random

class Common:

    #define User-Agent header (otomoto responds with 403 when default requests lib agent is used)
    user_agent = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:34.0) Gecko/20100101 Firefox/34.0",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/5.0)",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53 (compatible; bingbot/2.0; http://www.bing.com/bingbot.htm)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Media Center PC",
        "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; Trident/5.0)",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
        "Mozilla/5.0 (iPad; U; CPU OS 5_1 like Mac OS X) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B367 Safari/531.21.10 UCBrowser/3.4.3.532",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.6.01001)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.7.01001)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.5.01003)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0",
        "Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.2.8) Gecko/20100723 Ubuntu/10.04 (lucid) Firefox/3.6.8",
        "Mozilla/5.0 (Windows NT 5.1; rv:13.0) Gecko/20100101 Firefox/13.0.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:11.0) Gecko/20100101 Firefox/11.0",
        "Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.2.8) Gecko/20100723 Ubuntu/10.04 (lucid) Firefox/3.6.8",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.0.3705)",
        "Mozilla/5.0 (Windows NT 5.1; rv:13.0) Gecko/20100101 Firefox/13.0.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0.1",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
        "Opera/9.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.01",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows NT 5.1; rv:5.0.1) Gecko/20100101 Firefox/5.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:5.0) Gecko/20100101 Firefox/5.02",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1",
        "Mozilla/4.0 (compatible; MSIE 6.0; MSIE 5.5; Windows NT 5.0) Opera 7.02 Bork-edition [en]"    
    ]

    @staticmethod
    def get_user_agent():
        return random.choice(Common.user_agent)


    def param_switcher(self, offer_source, caroffer, param_name, param_value):
        if param_name.find(offer_source.category) != -1:
            caroffer.category = param_value
            return
        if param_name.find(offer_source.manufacturer) != -1:
            caroffer.manufacturer = param_value
            return
        if param_name.find(offer_source.model_name) != -1:
            caroffer.model_name = param_value
            return
        if param_name.find(offer_source.model_version) != -1:
            caroffer.model_version = param_value
            return
        if param_name.find(offer_source.year) != -1:
            caroffer.year = int(param_value)
            return
        if param_name.find(offer_source.odometer) != -1:
            #remove "km" and spaces before storing
            caroffer.odometer = int(param_value[:-2].replace(" ", ""))
            return
        if param_name.find(offer_source.juice) != -1:
            caroffer.juice = param_value
            return
        if param_name.find(offer_source.engine) != -1:
            #remove "cm3" and spaces before storing
            #for allegro there are 4 characters to remov coz the 3 is in superscript
            caroffer.engine = param_value[:-3].replace(" ", "")
            if offer_source.source_name != "otomoto":
                caroffer.engine = int(param_value[:-4].replace(" ", ""))
            else:
                caroffer.engine = int(param_value[:-3].replace(" ", ""))
            return
        if param_name.find(offer_source.power) != -1:
            #remove "KM" and spaces before stroring
            caroffer.power = int(param_value[:-2].replace(" ", ""))
            return
        if param_name.find(offer_source.transmission) != -1:
            caroffer.transmission = param_value
            return
        if param_name.find(offer_source.drivetrain_layout) != -1:
            caroffer.drivetrain_layout = param_value
            return
        if param_name.find(offer_source.body_type) != -1:
            caroffer.body_type = param_value
            return
        if param_name.find(offer_source.color) != -1:
            caroffer.color = param_value
            return
        if param_name.find(offer_source.left_hand_drive) != -1:
            if param_value == "Tak" or param_value == "po prawej":
                caroffer.left_hand_drive = True
            else:
                caroffer.left_hand_drive = False
            return

    def english_month(self, date):
        eng_date = date.replace("stycznia", "January")
        if date != eng_date :
            return eng_date
        eng_date = date.replace("lutego", "February")
        if date != eng_date :
            return eng_date
        eng_date = date.replace("marca", "March")
        if date != eng_date :
            return eng_date
        eng_date = date.replace("kwietnia", "April")
        if date != eng_date :
            return eng_date
        eng_date = date.replace("maja", "May")
        if date != eng_date :
            return eng_date
        eng_date = date.replace("czerwca", "June")
        if date != eng_date :
            return eng_date
        eng_date = date.replace("lipca", "July")
        if date != eng_date :
            return eng_date
        eng_date = date.replace("sierpnia", "August")
        if date != eng_date :
            return eng_date
        eng_date = date.replace("września", "September")
        if date != eng_date :
            return eng_date
        eng_date = date.replace("października", "October")
        if date != eng_date :
            return eng_date
        eng_date = date.replace("listopada", "Novermber")
        if date != eng_date :
            return eng_date
        eng_date = date.replace("grudnia", "December")
        if date != eng_date :
            return eng_date
