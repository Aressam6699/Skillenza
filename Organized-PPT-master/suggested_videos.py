
import requests
from getimpphrases import getImpPhrases
import pandas as pd

def remove_clean(df):
    
    tot=[]
    
    escapes = ''.join([chr(char) for char in range(1, 32)])
    translator = str.maketrans('', '', escapes)
    for f in df:
        f = f.translate(translator)
        f=f.strip()
        if len(f)==0:
            continue
        tot.append(f)
    return tot
    
def related_videos():


    try:
        df=pd.read_csv('fin.csv')
        df=df['ppt']
    except FileNotFoundError:
        print('Upload files first')




    df=list(df)
    df=remove_clean(df)




    text=''''''
    for i in df:
        text+=i
        text+='\n '





    search_term=getImpPhrases(text)
    #print(search_term)
    max_len = -1
    for ele in search_term: 
        if len(ele) > max_len: 
            max_len = len(ele) 
            res = ele 
    res



    search_term=res

    subscription_key = 'a50d176bc7314fd7acf6f7da2e52b7fe'
    assert subscription_key
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/videos/search"
    #search_term = "Machine Learning Models for Classification"



    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}

    params  = {"q": search_term, "count":5, "pricing": "free", "videoLength":"short"}


    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    import json
    r = json.dumps(search_results)
    with open("cont.json", "w") as write_file:
        json.dump(r, write_file)

    return search_results




