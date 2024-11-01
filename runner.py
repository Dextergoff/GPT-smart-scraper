from scraper import Scraper
scraper = Scraper(instructions={
            "base_url":"https://www.google.com/",
            "site_title":"Scrape This Site",
            "target_page":"https://www.scrapethissite.com/pages/simple/",
            "desired_contents":['country', 'capital', 'population', 'area']
        }) 