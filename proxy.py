import aiohttp
import asyncio
import itertools
import random
import re


def generate_user_agent():
    bases = [
        "Mozilla/5.0 ({system}) AppleWebKit/537.36 (KHTML, like Gecko) {browser}/{version} Safari/537.36",
        "Mozilla/5.0 ({system}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{version} Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 ({system}; rv:{version}) Gecko/20100101 Firefox/{version}",
        "Mozilla/5.0 ({system}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36 Edg/{edge_version}",
    ]
    systems = [
        "Windows NT 10.0; Win64; x64",
        "Windows NT 6.1; WOW64",
        "Windows NT 5.1; Win32",
        "Macintosh; Intel Mac OS X 10_15_7",
        "Macintosh; Intel Mac OS X 11_3_1",
        "Linux; Android 11; Pixel 5",
        "Linux; Android 8.0.0; Nexus 5X",
        "iPhone; CPU iPhone OS 16_0 like Mac OS X",
        "iPad; CPU OS 15_0 like Mac OS X",
    ]
    browsers = [
        ("Chrome", list(range(80, 117))),
        ("Safari", [12, 13, 14, 15, 16]),
        ("Firefox", list(range(50, 117))),
        ("Edge", list(range(80, 116))),
    ]
    
    system = random.choice(systems)
    browser, versions = random.choice(browsers)
    version = random.choice(versions)
    base = random.choice(bases)
    edge_version = random.randint(80, 116)  
    
    return base.format(system=system, browser=browser, version=version, edge_version=edge_version)

REGEX = re.compile(r'(\d{1,3}(?:\.\d{1,3}){3}:\d{2,5})')

class ProxyScraper:
    def __init__(self):
        self.proxies = []
        self.proxy_iter = None
        self.proxy_urls = {
          "http": [
                "https://api.proxyscrape.com/?request=displayproxies&proxytype=",
                "https://raw.githubusercontent.com/r00tee/Proxy-List/main/Https.txt",
                "https://github.com/MrMarble/proxy-list/raw/main/all.txt",
                "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
                "https://github.com/gitrecon1455/ProxyScraper/raw/main/proxies.txt",
                "https://github.com/Zaeem20/FREE_PROXIES_LIST/raw/master/http.txt",
                "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
                "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/http.txt",
                "https://github.com/elliottophellia/proxylist/raw/master/results/http/global/http_checked.txt",
                "https://api.proxyscrape.com/?request=displayproxies&proxytype=http",
                "https://www.proxy-list.download/api/v1/get?type=http",
                "http://spys.me/proxy.txt",
                "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
                "https://api.openproxylist.xyz/http.txt",
                "https://www.my-proxy.com/free-proxy-list.html",
                "https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt",
                "https://www.my-proxy.com/free-anonymous-proxy.html",
                "https://www.my-proxy.com/free-transparent-proxy.html",
                "https://www.my-proxy.com/free-proxy-list-2.html",
                "https://www.my-proxy.com/free-proxy-list-3.html",
                "https://www.my-proxy.com/free-proxy-list-4.html",
                "https://proxy50-50.blogspot.com/",
                "https://www.my-proxy.com/free-proxy-list-5.html",
                "http://alexa.lr2b.com/proxylist.txt",
                "http://rootjazz.com/proxies/proxies.txt",
                "https://www.my-proxy.com/free-socks-4-proxy.html",
                "https://www.my-proxy.com/free-proxy-list-6.html",
                "https://www.my-proxy.com/free-proxy-list-7.html",
                "https://www.my-proxy.com/free-proxy-list-8.html",
                "http://proxysearcher.sourceforge.net/Proxy%20List.php?type=http",
                "https://www.my-proxy.com/free-proxy-list-9.html",
                "https://www.my-proxy.com/free-proxy-list-10.html",
                "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
                "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
                "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
                "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
                "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
                "https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/http.txt",
                "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
                "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
                "https://proxy-spider.com/api/proxies.example.txt",
                "http://rootjazz.com/proxies/proxies.txt",
                "https://proxyspace.pro/http.txt",
                "https://proxyspace.pro/https.txt",
            ],
            "socks4": [
                "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4",
                "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks4/data.txt",
                "https://openproxylist.xyz/socks4.txt",
                "https://proxyspace.pro/socks4.txt",
                "https://www.proxy-list.download/api/v1/get?type=socks4",
                "https://proxyhub.me/en/all-socks4-proxy-list.html",
                "https://proxy-tools.com/proxy/socks4"
                "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=socks4",
                "https://spys.me/socks.txt",
                "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4",
                "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4",
                "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
                "https://www.proxy-list.download/api/v1/get?type=socks4",
                "https://api.openproxylist.xyz/socks4.txt",
                "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
                "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
                "https://www.my-proxy.com/free-socks-4-proxy.html",
                "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
                "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
                "http://worm.rip/socks4.txt",
                "https://www.socks-proxy.net/",
                "https://www.my-proxy.com/free-socks-4-proxy.html",
                "https://cdn.jsdelivr.net/gh/B4RC0DE-TM/proxy-list/SOCKS4.txt",
                "https://cdn.jsdelivr.net/gh/jetkai/proxy-list/online-proxies/txt/proxies-socks4.txt",
                "https://cdn.jsdelivr.net/gh/roosterkid/openproxylist/SOCKS4_RAW.txt",
                "https://cdn.jsdelivr.net/gh/saschazesiger/Free-Proxies/proxies/socks4.txt",
                "https://cdn.jsdelivr.net/gh/TheSpeedX/PROXY-List/socks4.txt",
                "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
                "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/socks4/global/socks4_checked.txt",
                "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks4.txt",
                "https://raw.githubusercontent.com/fahimscirex/proxybd/master/proxylist/socks4.txt",
                "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt",
                "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/socks4.txt",
                "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks4.txt",
                "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
                "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/socks4_proxies.txt",
                "https://raw.githubusercontent.com/SevenworksDev/proxy-list/main/proxies/socks4.txt",
                "https://raw.githubusercontent.com/tuanminpay/live-proxy/master/socks4.txt",
                "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt",
                "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/socks4.txt",
                "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
                "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt",
                "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks4.txt",
            ],
            "socks5": [
                "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5",
                "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks5/data.txt",
                "https://openproxylist.xyz/socks5.txt",
                "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5",
                "https://proxyspace.pro/socks5.txt",
                "https://spys.me/socks.txt",
                "https://www.proxy-list.download/api/v1/get?type=socks5",
                "https://proxy-tools.com/proxy/socks5",
                "https://proxyhub.me/en/all-sock5-proxy-list.html",
                "https://www.my-proxy.com/free-socks-5-proxy.html",
                "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=socks5",
                "https://cdn.jsdelivr.net/gh/HyperBeats/proxy-list/socks5.txt",
                "https://cdn.jsdelivr.net/gh/jetkai/proxy-list/online-proxies/txt/proxies-socks5.txt",
                "https://cdn.jsdelivr.net/gh/roosterkid/openproxylist/SOCKS5_RAW.txt",
                "https://cdn.jsdelivr.net/gh/TheSpeedX/PROXY-List/socks5.txt",
                "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
                "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/socks5/global/socks5_checked.txt",
                "https://raw.githubusercontent.com/fahimscirex/proxybd/master/proxylist/socks5.txt",
                "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
                "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/socks5.txt",
                "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
                "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt",
                "https://raw.githubusercontent.com/im-razvan/proxy_list/main/socks5.txt",
                "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
                "https://raw.githubusercontent.com/SevenworksDev/proxy-list/main/proxies/socks5.txt",
                "https://raw.githubusercontent.com/tuanminpay/live-proxy/master/socks5.txt",
                "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt"
                "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/socks5.txt",
                "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
                "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
                "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5",
                "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5",
                "https://www.proxy-list.download/api/v1/get?type=socks5",
                "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
                "https://www.my-proxy.com/free-socks-5-proxy.html",
                "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
                "https://github.com/roosterkid/openproxylist/blob/main/SOCKS5_RAW.txt",
                "https://api.openproxylist.xyz/socks5.txt",
                "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
                "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5",
                "http://www.socks24.org/feeds/posts/default",
                "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt"
                "http://worm.rip/socks5.txt",
                "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
      
            ]
}

    
REGEX = re.compile(r'(\d{1,3}(?:\.\d{1,3}){3}:\d{2,5})')

class ProxyScraper:
    def __init__(self):
        self.proxies = []
        self.proxy_iter = None
        self.proxy_urls = {
                  "http": [
                "https://api.proxyscrape.com/?request=displayproxies&proxytype=",
                "https://raw.githubusercontent.com/r00tee/Proxy-List/main/Https.txt",
                "https://github.com/MrMarble/proxy-list/raw/main/all.txt",
                "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
                "https://github.com/gitrecon1455/ProxyScraper/raw/main/proxies.txt",
                "https://github.com/Zaeem20/FREE_PROXIES_LIST/raw/master/http.txt",
                "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
                "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/http.txt",
                "https://github.com/elliottophellia/proxylist/raw/master/results/http/global/http_checked.txt",
                "https://api.proxyscrape.com/?request=displayproxies&proxytype=http",
                "https://www.proxy-list.download/api/v1/get?type=http",
                "http://spys.me/proxy.txt",
                "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
                "https://api.openproxylist.xyz/http.txt",
                "https://www.my-proxy.com/free-proxy-list.html",
                "https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt",
                "https://www.my-proxy.com/free-anonymous-proxy.html",
                "https://www.my-proxy.com/free-transparent-proxy.html",
                "https://www.my-proxy.com/free-proxy-list-2.html",
                "https://www.my-proxy.com/free-proxy-list-3.html",
                "https://www.my-proxy.com/free-proxy-list-4.html",
                "https://proxy50-50.blogspot.com/",
                "https://www.my-proxy.com/free-proxy-list-5.html",
                "http://alexa.lr2b.com/proxylist.txt",
                "http://rootjazz.com/proxies/proxies.txt",
                "https://www.my-proxy.com/free-socks-4-proxy.html",
                "https://www.my-proxy.com/free-proxy-list-6.html",
                "https://www.my-proxy.com/free-proxy-list-7.html",
                "https://www.my-proxy.com/free-proxy-list-8.html",
                "http://proxysearcher.sourceforge.net/Proxy%20List.php?type=http",
                "https://www.my-proxy.com/free-proxy-list-9.html",
                "https://www.my-proxy.com/free-proxy-list-10.html",
                "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
                "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
                "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
                "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
                "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
                "https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/http.txt",
                "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
                "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
                "https://proxy-spider.com/api/proxies.example.txt",
                "http://rootjazz.com/proxies/proxies.txt",
                "https://proxyspace.pro/http.txt",
                "https://proxyspace.pro/https.txt",
            ],
            "socks4": [
                "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4",
                "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks4/data.txt",
                "https://openproxylist.xyz/socks4.txt",
                "https://proxyspace.pro/socks4.txt",
                "https://www.proxy-list.download/api/v1/get?type=socks4",
                "https://proxyhub.me/en/all-socks4-proxy-list.html",
                "https://proxy-tools.com/proxy/socks4"
                "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=socks4",
                "https://spys.me/socks.txt",
                "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4",
                "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4",
                "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
                "https://www.proxy-list.download/api/v1/get?type=socks4",
                "https://api.openproxylist.xyz/socks4.txt",
                "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
                "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
                "https://www.my-proxy.com/free-socks-4-proxy.html",
                "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
                "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
                "http://worm.rip/socks4.txt",
                "https://www.socks-proxy.net/",
                "https://www.my-proxy.com/free-socks-4-proxy.html",
                "https://cdn.jsdelivr.net/gh/B4RC0DE-TM/proxy-list/SOCKS4.txt",
                "https://cdn.jsdelivr.net/gh/jetkai/proxy-list/online-proxies/txt/proxies-socks4.txt",
                "https://cdn.jsdelivr.net/gh/roosterkid/openproxylist/SOCKS4_RAW.txt",
                "https://cdn.jsdelivr.net/gh/saschazesiger/Free-Proxies/proxies/socks4.txt",
                "https://cdn.jsdelivr.net/gh/TheSpeedX/PROXY-List/socks4.txt",
                "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
                "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/socks4/global/socks4_checked.txt",
                "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks4.txt",
                "https://raw.githubusercontent.com/fahimscirex/proxybd/master/proxylist/socks4.txt",
                "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt",
                "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/socks4.txt",
                "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks4.txt",
                "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
                "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/socks4_proxies.txt",
                "https://raw.githubusercontent.com/SevenworksDev/proxy-list/main/proxies/socks4.txt",
                "https://raw.githubusercontent.com/tuanminpay/live-proxy/master/socks4.txt",
                "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt",
                "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/socks4.txt",
                "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
                "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt",
                "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks4.txt",
            ],
            "socks5": [
                "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5",
                "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks5/data.txt",
                "https://openproxylist.xyz/socks5.txt",
                "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5",
                "https://proxyspace.pro/socks5.txt",
                "https://spys.me/socks.txt",
                "https://www.proxy-list.download/api/v1/get?type=socks5",
                "https://proxy-tools.com/proxy/socks5",
                "https://proxyhub.me/en/all-sock5-proxy-list.html",
                "https://www.my-proxy.com/free-socks-5-proxy.html",
                "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=socks5",
                "https://cdn.jsdelivr.net/gh/HyperBeats/proxy-list/socks5.txt",
                "https://cdn.jsdelivr.net/gh/jetkai/proxy-list/online-proxies/txt/proxies-socks5.txt",
                "https://cdn.jsdelivr.net/gh/roosterkid/openproxylist/SOCKS5_RAW.txt",
                "https://cdn.jsdelivr.net/gh/TheSpeedX/PROXY-List/socks5.txt",
                "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
                "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/socks5/global/socks5_checked.txt",
                "https://raw.githubusercontent.com/fahimscirex/proxybd/master/proxylist/socks5.txt",
                "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
                "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/socks5.txt",
                "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
                "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt",
                "https://raw.githubusercontent.com/im-razvan/proxy_list/main/socks5.txt",
                "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
                "https://raw.githubusercontent.com/SevenworksDev/proxy-list/main/proxies/socks5.txt",
                "https://raw.githubusercontent.com/tuanminpay/live-proxy/master/socks5.txt",
                "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt"
                "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/socks5.txt",
                "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
                "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
                "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5",
                "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5",
                "https://www.proxy-list.download/api/v1/get?type=socks5",
                "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
                "https://www.my-proxy.com/free-socks-5-proxy.html",
                "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
                "https://github.com/roosterkid/openproxylist/blob/main/SOCKS5_RAW.txt",
                "https://api.openproxylist.xyz/socks5.txt",
                "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
                "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5",
                "http://www.socks24.org/feeds/posts/default",
                "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt"
                "http://worm.rip/socks5.txt",
                "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
      
            ]
        }

    async def scrap(self, source_url, proxy_type):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    source_url, 
                    headers={'User-Agent': generate_user_agent()}, 
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    html = await response.text()
                    matches = REGEX.findall(html)
                    for match in matches:
                        self.proxies.append((proxy_type, match))
        except Exception as e:
            with open('error.txt', 'a', encoding='utf-8', errors='ignore') as f:
                f.write(f'{source_url} -> {e}\n')

    async def init(self):
        print(" [ WAIT ] Scraping proxies... ")
        self.proxies.clear()

        tasks = [self.scrap(url, proxy_type) for proxy_type, urls in self.proxy_urls.items() for url in urls]
        await asyncio.gather(*tasks)

        self.proxies = list(set(self.proxies))
        random.shuffle(self.proxies)
        self.proxy_iter = itertools.cycle(self.proxies)

        print(f"[ INFO ] Total proxies obtenidos: {len(self.proxies)}")

    async def validate_proxy(self, session, proxy, proxy_type):
        test_url = "https://www.google.com"
        proxy_url = f"{proxy_type}://{proxy}"

        try:
            async with session.get(test_url, proxy=proxy_url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                return response.status == 200
        except Exception:
            return False

    async def check_proxies(self):
        valid_proxies = set()
        semaphore = asyncio.Semaphore(500)  
        async def validate(proxy_type, proxy):
            async with semaphore:
                async with aiohttp.ClientSession() as session:
                    is_valid = await self.validate_proxy(session, proxy, proxy_type)
                    if is_valid:
                        valid_proxies.add((proxy_type, proxy))
                        print(f"✅ Proxy válido ({proxy_type}): {proxy}")

                        with open("vproxies.txt", "a") as f:
                            f.write(f"{proxy_type}://{proxy}\n")

        tasks = [validate(proxy_type, proxy) for proxy_type, proxy in self.proxies]
        await asyncio.gather(*tasks)

        self.proxies = list(valid_proxies)
        print(f"✅ Total proxies válidos: {len(self.proxies)}")



if __name__ == "__main__":
    scraper = ProxyScraper()
    asyncio.run(scraper.init())  
    asyncio.run(scraper.check_proxies())  
