import pandas as pd
from yattag import Doc
from collections import OrderedDict


df=pd.read_csv('final_df.csv')

for 



doc, tag, text = Doc().tagtext()

ppts=OrderedDict()


for index,row in df.iterrows():
    ppt=row['ppt']

    

html='''

with tag('html'):


    with tag('head'):
        with tag('title'):
            text('Your Customized Notes')


    with tag('body'):




'''



result = doc.getvalue()

print(result)