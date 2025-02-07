import findAllShops
import pygsheets

def appendGoogleSheet(credentials, sheetname, worksheetname, row):
    gc = pygsheets.authorize(service_file=credentials)
    sh = gc.open(sheetname)
    worksheet1 = sh.worksheet("title", worksheetname)
    worksheet1.append_table(values=row)

if __name__ == "__main__":
    credentials = "profound-veld-450200-k3-0accad6787dc.json"
    sheetname = "test for shopify"
    worksheetname = "Sheet1"

    shopify_url = "www.publicdesire.com"
    shops = findAllShops.find_all_shopify_shops(shopify_url)

    row = [shopify_url] + list(shops)

    appendGoogleSheet(credentials, sheetname, worksheetname, row)
