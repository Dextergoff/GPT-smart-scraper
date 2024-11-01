from fake_useragent import UserAgent
ua = UserAgent()
user_agent = ua.random

def gen_headers(current_url):

    if current_url == None:
        current_url = 'https://www.google.com/'

    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding":"gzip, deflate, br, zstd",
        "Accept-Language":"en-US,en;q=0.9",
        "Cache-Control":"max-age=0",
        "DNT":"1",
        "Connection":"close",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":user_agent,
        "Referer":current_url
    }
    # change this so when referer changes onjly reffer is changed and nothing else
    return headers
