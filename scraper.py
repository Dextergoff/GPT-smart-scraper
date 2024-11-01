from playwright.sync_api import sync_playwright
from Headers import gen_headers
from Proxy import GetProxy
import time
from gpt import field_finder
get_proxy = GetProxy()

proxy_settings = {"server": "per-context"}
script_to_add = "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"

class Scraper:

    def __init__(self, instructions):
        """
        Initializes the scraper with instructions and starts Playwright.
        """
        self.current_url = None
        self.attempts = 0
        self.instructions = instructions
        with sync_playwright() as p:
            self.p = p
            self.init_browser()
            self.run_scraper()
            
    def init_browser(self):
        """
        Initialize the browser with given settings.
        """
        self.browser = self.p.chromium.launch(
            headless=False, 
            slow_mo=50, 
            proxy=proxy_settings
        )

    def run_scraper(self):
        """
        Run the scraper by setting up the browser context and starting the scrape process.
        """
        self.death_condition()
        self.add_context()
        self.page = self.context.new_page()
        self.attach_url_listener()
        self.scrape()

    def attach_url_listener(self):
        """
        Event listener so everytime the url changes it updates the current_url variable
        """
        self.page.on('framenavigated', lambda frame: self.handle_navigation(frame.url))

    def handle_navigation(self, url):
        self.current_url = url
        # self.handle_blockage()

    def handle_blockage(self):
        if '/www.google.com/sorry/' in self.current_url:
            self.retry_scrape()

    def death_condition(self):
        """
        Check the number of attempts and handle browser restart or termination.
        """
        if self.attempts > 4:
            self.kill()
        elif self.attempts > 0:
            self.browser.close()
            self.init_browser()

    def add_context(self):
        """
        Add a new browser context with proxy settings and custom script.
        """
        self.context = self.browser.new_context(proxy=get_proxy.retrive())
        self.context.add_init_script(script_to_add)
        
    def scrape(self):
        """
        Main scraping function to handle navigation and data extraction.
        """
        try:
            site_title = self.instructions['site_title']
            target_page = self.instructions['target_page']
            base_url = self.instructions['base_url']
            desired_contents = self.instructions['desired_contents']
            self.goto_url(base_url)
            self.enter_query(site_title)
            self.seek_site(site_title, target_page)
            self.seek_content(desired_contents)
        except:
            self.retry_scrape()
        finally:
            self.kill()

    def goto_url(self, url):
        """
        Navigate to the base URL and set extra HTTP headers, and use current url as refferer.
        """
        self.page.set_extra_http_headers(gen_headers(self.current_url))
        self.page.goto(url)

    def enter_query(self, site_title):
        """
        Enter the search query into the search box.
        """
        time.sleep(1)
        search_box = self.page.locator("[name='q']")
        search_box.hover()
        search_box.click()
        search_box.press_sequentially(
            site_title, 
            delay=78
        )
        self.page.keyboard.press('Enter')

    def seek_site(self, site_title ,target_page):
        """
        Locate and click on the site link based on the site title.
        """
        self.page.locator(f'a:has-text("{site_title}")').first.click()
        time.sleep(1)
        self.goto_url(target_page)

    def seek_content(self,desired_contents):
        """
        Use Chatgpt to find desired feild names within html.
        """
        #get html contents
        html=self.get_html()
        fields = field_finder(html, desired_contents)
        print(fields)
    
    def get_html(self):
        return self.page.content()

    def retry_scrape(self):
        """
        Handle exceptions by logging the error and retrying the scrape.
        """
        self.attempts += 1
        self.run_scraper()

    def kill(self):
        """
        Close the browser and stop Playwright.
        """
        self.browser.close()
        self.p.stop()
    