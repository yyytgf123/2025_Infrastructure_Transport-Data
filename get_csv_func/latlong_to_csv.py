import pandas as pd
from trans_lat_long import get_xy

#법정동 + 지번
df = pd.read_csv('csv/apart_data.csv')
def data_set_csv():
    ad = df['법정동'] + " " + df['지번']
    add = pd.DataFrame(ad)
    add.to_csv("csv/addr.csv", header=False, index=False)

lat_long_store = []
df = pd.read_csv("csv/addr.csv", encoding='utf-8', names=["주소"])
def lat_long():
    for i in range(df.shape[0]):
        x, y = get_xy(df["주소"][i])
        lat_long_store.append([y,x])
    dff = pd.DataFrame(lat_long_store)
    dff.to_csv("csv/lat_long.csv", header=False, index=False)

# lat_long()