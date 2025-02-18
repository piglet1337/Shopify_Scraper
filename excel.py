import pandas
import findAllShops

def read_excel(file):
    data_frame = pandas.read_excel(file, header = 1)
    return data_frame

def extract_domain_column(df):
    return df['domain']

def findShops_InsertIntoDF(x, bucket7, notBucket7, failed):
    shops = list(findAllShops.find_all_shopify_shops(x))
    if len(shops) == 0:
        failed.append({0:x})
        return
    if len(shops) == 1:
        notBucket7.append({0:x,1:shops[0]})
        return
    row = {0:x}
    i = 1
    for shop in shops:
        row[i] = shop
        i += 1
    bucket7.append(row)
    

if __name__ == "__main__":
    bucket7 = []
    notBucket7 = []
    failed = []

    df = read_excel('domains_export.xlsx')
    df = extract_domain_column(df)
    df.apply(findShops_InsertIntoDF, args=[bucket7, notBucket7, failed])
    bucket7DF = pandas.DataFrame(bucket7)
    notBucket7DF = pandas.DataFrame(notBucket7)
    failedDF = pandas.DataFrame(failed)
    print(bucket7DF)
    print(notBucket7DF)
    with pandas.ExcelWriter('myShopify.xlsx', engine='xlsxwriter') as writer:
        bucket7DF.to_excel(writer, sheet_name='bucket7')
        notBucket7DF.to_excel(writer, sheet_name='notBucket7')
        failedDF.to_excel(writer, sheet_name='failed')