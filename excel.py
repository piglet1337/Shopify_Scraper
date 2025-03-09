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

def get_new_pd_dataframes(df):
    bucket7 = []
    notBucket7 = []
    failed = []
    df = extract_domain_column(df)
    df.apply(findShops_InsertIntoDF, args=[bucket7, notBucket7, failed])
    bucket7DF = pandas.DataFrame(bucket7)
    notBucket7DF = pandas.DataFrame(notBucket7)
    failedDF = pandas.DataFrame(failed)
    return (bucket7DF, notBucket7DF, failedDF)
    
if __name__ == "__main__":
    input = "domains_export.xlsx"
    df = read_excel(input)
    dataframes = get_new_pd_dataframes(df)
    with pandas.ExcelWriter("myShopify.xlsx", engine='xlsxwriter') as writer:
            dataframes[0].to_excel(writer, sheet_name='bucket7')
            dataframes[1].to_excel(writer, sheet_name='notBucket7')
            dataframes[2].to_excel(writer, sheet_name='failed')