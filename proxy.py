import aiohttp
import asyncio
import random
import re
import itertools
import argparse
import time
import json

REGEX = re.compile(r'(\d{1,3}(?:\.\d{1,3}){3}:\d{2,5})')

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
class ProxyScraper:
    def __init__(self, concurrent=500, max_ping=None, country=None, use_geo=False):
        self.concurrent = concurrent
        self.max_ping = max_ping
        self.country = country.upper() if country else None
        self.use_geo = use_geo
        self.proxies = []
        self.grouped_by_country = {}
        self.raw_list = []
        self.proxy_iter = None
        proxy_urls = {
    "http": [
        "https://api.proxyscrape.com/?request=displayproxies&proxytype=http",
        "https://api.proxyscrape.com/?request=displayproxies&proxytype=",
        "https://raw.githubusercontent.com/r00tee/Proxy-List/main/Https.txt",
        "https://raw.githubusercontent.com/MrMarble/proxy-list/main/all.txt",
        "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
        "https://raw.githubusercontent.com/gitrecon1455/ProxyScraper/main/proxies.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
        "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
        "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/elliottophellia/proxylist/master/results/http/global/http_checked.txt",
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
        "https://api.openproxylist.xyz/http.txt",
        "https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
        "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
        "https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/http.txt",
        "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
        "https://proxy-spider.com/api/proxies.example.txt",
        "https://proxyspace.pro/http.txt",
        "https://proxyspace.pro/https.txt",
        "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt",
        "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt",
        "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/https.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
        "http://alexa.lr2b.com/proxylist.txt",
        "https://multiproxy.org/txt_all/proxy.txt",
        "http://proxysearcher.sourceforge.net/Proxy%20List.php?type=http",
        "https://raw.githubusercontent.com/RX4096/proxy-list/main/online/all.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
        "https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/https.txt",
        "https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/https.txt",
        "https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/http.txt",
        "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
        "http://rootjazz.com/proxies/proxies.txt",
        "http://spys.me/proxy.txt",
        "https://sheesh.rip/http.txt",
        "http://worm.rip/http.txt",
        "http://www.proxyserverlist24.top/feeds/posts/default",
        "https://www.proxyscan.io/download?type=http",
        "https://www.my-proxy.com/free-anonymous-proxy.html",
        "https://www.my-proxy.com/free-transparent-proxy.html",
        "https://www.my-proxy.com/free-proxy-list.html",
        "https://www.my-proxy.com/free-proxy-list-2.html",
        "https://www.my-proxy.com/free-proxy-list-3.html",
        "https://www.my-proxy.com/free-proxy-list-4.html",
        "https://www.my-proxy.com/free-proxy-list-5.html",
        "https://www.my-proxy.com/free-proxy-list-6.html",
        "https://www.my-proxy.com/free-proxy-list-7.html",
        "https://www.my-proxy.com/free-proxy-list-8.html",
        "https://www.my-proxy.com/free-proxy-list-9.html",
        "https://www.my-proxy.com/free-proxy-list-10.html",
        "https://www.freeproxychecker.com/result/http_proxies.txt"
    ],
    "socks4": [
        "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4",
        "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks4/data.txt",
        "https://openproxylist.xyz/socks4.txt",
        "https://proxyspace.pro/socks4.txt",
        "https://www.proxy-list.download/api/v1/get?type=socks4",
        "https://proxyhub.me/en/all-socks4-proxy-list.html",
        "https://proxy-tools.com/proxy/socks4",
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=socks4",
        "https://spys.me/socks.txt",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
        "https://api.openproxylist.xyz/socks4.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
        "https://www.socks-proxy.net/",
        "https://cdn.jsdelivr.net/gh/B4RC0DE-TM/proxy-list/SOCKS4.txt",
        "https://cdn.jsdelivr.net/gh/jetkai/proxy-list/online-proxies/txt/proxies-socks4.txt",
        "https://cdn.jsdelivr.net/gh/roosterkid/openproxylist/SOCKS4_RAW.txt",
        "https://cdn.jsdelivr.net/gh/saschazesiger/Free-Proxies/proxies/socks4.txt",
        "https://cdn.jsdelivr.net/gh/TheSpeedX/PROXY-List/socks4.txt",
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
        "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4&country=all",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks4.txt",
        "http://worm.rip/socks4.txt",
        "https://www.proxyscan.io/download?type=socks4",
        "https://www.my-proxy.com/free-socks-4-proxy.html",
        "http://www.socks24.org/feeds/posts/default",
        "https://www.freeproxychecker.com/result/socks4_proxies.txt",
        "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks4.txt",
        "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks4.txt",
        "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS4.txt"
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
        "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt",
        "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/socks5.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
        "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
        "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS5.txt",
        "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks5.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
        "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks5.txt",
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all&simplified=true",
        "https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks5.txt",
        "https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/socks.txt",
        "http://worm.rip/socks5.txt",
        "http://www.socks24.org/feeds/posts/default",
        "https://www.freeproxychecker.com/result/socks5_proxies.txt",
        "https://www.proxyscan.io/download?type=socks5"
    ]
}

    async def fetch(self, url, session, proxy_type):
        try:
            async with session.get(url, headers={"User-Agent": generate_user_agent()}, timeout=10) as response:
                text = await response.text()
                for proxy in REGEX.findall(text):
                    self.proxies.append((proxy_type, proxy))
        except Exception:
            pass

    async def scrape(self):
        print("🔎 Scraping proxies...")
        self.proxies.clear()
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.fetch(url, session, ptype)
                for ptype, urls in self.proxy_urls.items()
                for url in urls
            ]
            await asyncio.gather(*tasks)

        self.proxies = list(set(self.proxies))
        random.shuffle(self.proxies)
        self.proxy_iter = itertools.cycle(self.proxies)
        print(f"✅ Proxies encontrados: {len(self.proxies)}")

    async def validate(self, session, proxy, proxy_type, semaphore):
        proxy_url = f"{proxy_type}://{proxy}"
        test_url = "http://httpbin.org/ip"

        async with semaphore:
            try:
                start_time = time.monotonic()
                async with session.get(test_url, proxy=proxy_url, timeout=8) as res:
                    if res.status == 200:
                        elapsed = time.monotonic() - start_time
                        ip_data = await res.json()
                        ip = ip_data.get("origin", "").split(",")[0]

                        proxy_country = "??"
                        if self.use_geo and ip:
                            try:
                                async with session.get(f"https://ipinfo.io/{ip}/json", timeout=5) as geo:
                                    data = await geo.json()
                                    proxy_country = data.get("country", "??").upper()
                            except:
                                pass

                        if (self.max_ping is None or elapsed <= self.max_ping) and \
                                (self.country is None or proxy_country == self.country):

                            full_proxy = f"{proxy_type}://{proxy}"
                            self.raw_list.append(full_proxy)

                            if self.use_geo:
                                if proxy_country not in self.grouped_by_country:
                                    self.grouped_by_country[proxy_country] = []
                                self.grouped_by_country[proxy_country].append(full_proxy)

                            print(f"✔️  {full_proxy} | {proxy_country} | {elapsed:.2f}s")
            except Exception:
                pass

    async def check(self):
        print("⚙️  Validando proxies...")
        semaphore = asyncio.Semaphore(self.concurrent)
        async with aiohttp.ClientSession(headers={"User-Agent": generate_user_agent()}) as session:
            tasks = [
                self.validate(session, proxy, ptype, semaphore)
                for ptype, proxy in self.proxies
            ]
            await asyncio.gather(*tasks)

        print(f"🎯 Proxies válidos: {len(self.raw_list)}")

        with open("proxys.txt", "w") as f:
            for proxy in self.raw_list:
                f.write(proxy + "\n")

        if self.use_geo:
            with open("vproxies.json", "w") as f:
                json.dump(self.grouped_by_country, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Proxy Scraper + Checker con opciones")
    parser.add_argument("-c", "--check", action="store_true", help="Activar chequeo de proxies")
    parser.add_argument("-g", "--geo", action="store_true", help="Obtener país de cada proxy (requiere --check)")
    parser.add_argument("-v", "--concurrent", type=int, default=500, help="Máximo de validaciones concurrentes")
    parser.add_argument("-m", "--max", type=float, help="Tiempo máximo de respuesta en segundos")
    parser.add_argument("-p", "--country", type=str, help="Filtrar proxies por país (ej: US, BR, DE)")

    args = parser.parse_args()

    scraper = ProxyScraper(
        concurrent=args.concurrent,
        max_ping=args.max,
        country=args.country,
        use_geo=args.geo
    )

    start_time = time.time()
    asyncio.run(scraper.scrape())

    if args.check:
        asyncio.run(scraper.check())
    else:
        with open("proxys.txt", "w") as f:
            for ptype, proxy in scraper.proxies:
                f.write(f"{ptype}://{proxy}\n")
        print(f"📄 proxys.txt guardado sin validación ({len(scraper.proxies)} proxies)")

    print(f"⏱️ Tiempo total: {time.time() - start_time:.2f} segundos")
