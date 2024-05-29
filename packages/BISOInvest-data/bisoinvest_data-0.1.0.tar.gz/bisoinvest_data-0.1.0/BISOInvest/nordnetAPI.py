import requests
import pandas as pd
import numpy as np
import json
#from pandas.io.json import json_normalize
s1 = requests.Session()



def get_data(url):
    # Henter ut første spørring for å få gyldige cookies
    try:
        response = s1.get(url)
        data = response.text
        c = response.cookies
        h = response.headers
    except requests.exceptions.RequestException as error:  
        print("Det ser ut som domenepekeren ma oppdateres")
        return error
    return data, c, h




def make_url1():
    # Lager url for første spørring 
    #url = f'https://www.shareville.no/medlemmer/BISOInvest/portfolios/85292/yield'
    url = 'https://www.shareville.no/api/v1/portfolios/85292/performance'
    return url

def format_data():
    url = make_url1()
    data, c, h = get_data(url)
    BISO_details = json.loads(data)
    rows = []
    for i in BISO_details['y5']:
        rows.append(i)
    df = pd.DataFrame(data = rows)
    df = df.set_index(df.date)
    df.drop('date', axis=1, inplace = True)
    print(df)
    return df

format_data()



