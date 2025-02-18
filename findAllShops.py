import urllib.request
import re

def get_html(shopify_url):
    if not shopify_url.startswith("https://"):
        shopify_url = "https://" + shopify_url
    try:
        req = urllib.request.Request(shopify_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0')
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8')
        req.add_header('Accept-Language', 'en-US,en;q=0.5')
        
        html_as_string = urllib.request.urlopen(req).read().decode('utf-8')
        # fp = urllib.request.urlopen(shopify_url)
        # mybytes = fp.read()

        # html_as_string = mybytes.decode("utf8")
        # fp.close()
    except Exception as e:
        print(e)
        return None
    return html_as_string

def find_links(html):
    links = re.findall('https:\/\/[\w_-]+(?:(?:\.[\w_-]+)+)[\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-]', html)
    return links

def normalize_link(link):
    normalized_link = link.replace("https://", "").replace("www.", "")
    if normalized_link.endswith("/"):
        normalized_link = normalized_link[:-1]
    return normalized_link

def thin_links(links, shopify_url):
    common_paths = ["collections", "products", "pages", "cart", "checkout", "google", "instagram", "snapchat", "facebook", "youtube", "tiktok", "search", "cdn", "linkedin", "myshopify", "pinterest", "twitter", "apple", "blog"]
    url = normalize_link(shopify_url)
    domains = url.split(".")[:-1]
    thin_links = [normalize_link(shopify_url)]
    for link in links:
        link = normalize_link(link)
        if link in thin_links:
            continue
        for domain in domains:
            if domain in link:
                if any(path in link for path in common_paths):
                    continue
                thin_links.append(link)
                break
    return thin_links

def get_shop(url):
    html_as_string = get_html(url)
    if not html_as_string:
        return None
    match = re.search(r"Shopify.shop = (.*);", html_as_string)
    if match:
        shopify_shop = match.group(1)
        return shopify_shop

def get_all_shops(links):
    shops = set()
    i = 0
    for link in links:
        shop = get_shop(link)
        if shop:
            shops.add(shop)
        if i == 5 and len(shops) <= 1:
            return set()
        i += 1
    return shops

def find_all_shopify_shops(shopify_url):
    html = get_html(shopify_url)
    if (html == None):
        print("couldn't get html")
        return set()
    links = find_links(html)
    links = thin_links(links, shopify_url)
    shops = get_all_shops(links)
    print(shops)
    return shops

if __name__ == "__main__":
    shopify_url = "https://sendegaro.com/"
    shops = find_all_shopify_shops(shopify_url)
    print(shops)