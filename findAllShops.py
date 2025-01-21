import urllib.request
import re

def get_html(shopify_url):
    if not shopify_url.startswith("https://"):
        shopify_url = "https://" + shopify_url
    try:
        fp = urllib.request.urlopen(shopify_url)
        mybytes = fp.read()

        html_as_string = mybytes.decode("utf8")
        fp.close()
    except Exception as e:
        return None
    return html_as_string

def find_links(html):
    links = re.findall('https:\/\/[\w_-]+(?:(?:\.[\w_-]+)+)[\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-]', html)
    return links

def thin_links(links, shopify_url):
    common_paths = ["/collections/", "/products/", "/pages/", "/cart/", "/checkout/"]
    url = shopify_url.replace("https://", "")
    url = url.replace("www.", "")
    domains = url.split(".")[:-1]
    thin_links = [shopify_url]
    for link in links:
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
    for link in links:
        shop = get_shop(link)
        if shop:
            shops.add(shop)
    return shops

def find_all_shopify_shops(shopify_url):
    html = get_html(shopify_url)
    links = find_links(html)
    links = thin_links(links, shopify_url)
    shops = get_all_shops(links)
    return shops

if __name__ == "__main__":
    shopify_url = "www.publicdesire.com"
    shops = find_all_shopify_shops(shopify_url)
    print(shops)