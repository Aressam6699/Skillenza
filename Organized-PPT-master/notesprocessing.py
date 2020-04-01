from readppts import readppts
from titles_processing import titles_processing
from simislides import findsimiliarslides
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from collections import OrderedDict
import re
import numpy as np
import spacy
import os
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
from gensim.models import LdaModel
from gensim import models, similarities
from nltk.stem.porter import PorterStemmer
import time
from nltk import FreqDist
from scipy.stats import entropy
import matplotlib.pyplot as plt
import seaborn as sns
from getimpphrases import getImpPhrases
import warnings
import time
from os.path import isfile, join
from nltk.corpus import stopwords
stop_words=stopwords.words('english')

tmp_file = 'embeddings/word2vec-glove.6B.300d.txt'


sns.set_style("darkgrid")
spacy_nlp = spacy.load("en_core_web_sm")
stop_words=stopwords.words('english')
glove_model = gensim.models.KeyedVectors.load_word2vec_format(tmp_file)
#glove_model = KeyedVectors.load_word2vec_format(tmp_file)

def remove_clean(f):
    escapes = ''.join([chr(char) for char in range(1, 32)])
    translator = str.maketrans('', '', escapes)
    f = f.translate(translator)
    f=f.strip()
    if len(f)==0:
        f=''
    return f


def cleanseddf(temp):
    
    unique=[]

    for ind in temp.index:

        textini=temp['text'][ind]
        textini=textini.lower().split()
        textini=[w for w in textini if w not in stop_words]

        unique.append((ind,textini))
    tocheck=[]
    
    
    for i in range(len(unique)):
        for j in range(i+1,len(unique)):
                distance=glove_model.wmdistance(unique[i][1],unique[j][1])
                if distance<3:
                    if unique[j][0] not in tocheck:
                        tocheck.append(unique[j][0])
    for x in tocheck:
        temp.drop(temp[temp['slidenumber']==x].index, axis=0, inplace=True)

    return temp


def remove_unwanted_titles(unwanted,final_list_of_titles):
    
    refreshed=[]
    for i in final_list_of_titles:
        x=i[1]
        if x in unwanted:
            continue
        else:
            refreshed.append(i)
    return refreshed


def htmlstatement(tup):
    if tup[0]==1:
        s='<h1>'+tup[1]+'</h1>'
    elif tup[0]==2:
        s='<h2>'+tup[1]+'</h2>'
    elif tup[0]==3:
        s='<h3>'+tup[1]+'</h3>'
    elif tup[0]==4:
        text=tup[1].split('\n')
        s=''''''
        for i in text:
            
            s+='<p>'+i+'</p>\n'
    elif tup[0]==5:
        cur_path=os.getcwd()
        os.chdir('templates')
        s=''''''
        for img in tup[1]:
            b = os.path.getsize(img)
            b=b//1000
            if b<3:
                #print('yes')
                continue
            
            s+='<img src='+ img +' alt="Cannot Load image"><br><br>'+'\n'
        os.chdir(cur_path)
    elif tup[0]==6:
        s='''<table>'''+'\n'
        for table in tup[1]:
            for row in range(len(table)):
                s+='<tr>'+'\n'
                for col in range(len(table[0])):
                    s+='<td>'
                    s+=table[row][col]
                    s+='</td>'+' '
                    #print(table[row][col])
                s+='\n'+'</tr>'+'\n'
        s+='</table><br>'
    elif tup[0]==11:
        text=tup[1].split('\n')
        s=''''''
        for i in text:
            
            s+='<p id="p01">'+i+'</p>\n'
        
    else:
        s='<br><br><br><hr><hr><br><br><br>'
    return s




def main(directory):

    start=time.time()

    contents,links=readppts(directory)
    final_list_of_titles, similiar_titles=titles_processing(contents)       

    sim_slides=findsimiliarslides(contents,similiar_titles,final_list_of_titles)    

    print('Read all pptx files')
    #final_list_of_titles=remove_unwanted_titles()

    new_content=OrderedDict() 

    for ppt in contents:
        for slide in contents[ppt]:
            try:
                for maybe in sim_slides:
                    if ppt==maybe:
                        if slide in sim_slides[maybe]:
                            er=5/0
            except ZeroDivisionError:
                continue
            tup=(ppt,contents[ppt][slide][0][0])
            if tup in final_list_of_titles:
                new_content.update({ppt:contents[ppt]})
    contents=new_content

    data=[]
    for ppttit in contents:
        row=[]
        ppt=contents[ppttit]
        for slide in ppt:
            paras=ppt[slide]
            title=paras[0]
            title=title[-1]
            #print(title)
            subtitle=paras[1]
            if len(subtitle)>0:
                subtitle=subtitle[0]
            else:
                subtitle=''
            text=paras[2]
            if len(text)>0:
                t=''''''
                for line in text:
                    if line.isdigit():
                        break
                    elif line.strip()==title:
                        break
                    elif line.strip()==subtitle:
                        break
                        
                    t+=line
                    t+='\n'
                text=t
                if len(text)<3:
                    text=''
            else:
                text=''
            #print(text)
            
            images=paras[3]
            tables=paras[4]
            
            row=[ppttit,slide,title,subtitle,text,images,tables]
            data.append(row)

    df=pd.DataFrame(data)
    df.columns=['ppt','slidenumber','title','subtitle','text','images','tables']

    df['index1'] = df.index
    df_dup=df
    cols=df_dup.columns

    pptandtitles=df_dup[['ppt','title']]
    pptandtitles=pptandtitles.drop_duplicates()

    pptandtitles=list(np.asarray(pptandtitles))
    final_df=[]
    for i in pptandtitles:
        temp=df_dup[(df_dup['ppt']==i[0])&(df_dup['title']==i[1])]
        temp=cleanseddf(temp)
        #c+=len(temp)
        for index, row in temp.iterrows():
            #print(list(row[cols]))
            final_df.append(list(row[cols]))
    
    final_df = pd.DataFrame(final_df,columns=cols)

    total_text=''''''

    all_images=[]

    for index,row in final_df.iterrows():
        text=row['text']
        imgs=row['images']
        if text:
            text=str(text)
            if len(text)>2:
                total_text+=text
                total_text+='\n'
        all_images+=imgs

    sentences=getImpPhrases(total_text)
    sentences=' .'.join(sentences)

    order=[]

    for index,row in final_df.iterrows():
    
        ppt=row['ppt']
        title=row['title']
        subtitle=row['subtitle']
        text=row['text']
        if text:
            text=str(text)
        images=row['images']
        tables=row['tables']
        
        if (1,ppt) not in order:
            order.append((1,ppt))
        if (2,title) not in order:
            order.append((2,title))
        if len(subtitle)>0:
            if len(subtitle[-1])>1:
                if (3,subtitle) not in order:
                    order.append((3,subtitle[-1]))
        if len(text)>2:
            if (4,text) not in order:
                if(11,text) not in order:
                    if text in sentences:
                        order.append((11,text))

                    else:
                        if (11,text) not in order:
                            order.append((4,text))
                    #total_text+=text
                    #total_text+='\n'
        if len(images)>0:
            if(5,images) not in order:
                order.append((5,images))
        if len(tables)>0:
            if(6,tables) not in order:
                order.append((6,tables))
        order.append(tuple([7]))

    finalhtmlcode=''''''
    for i in order:
        finalhtmlcode+=htmlstatement(i)+'\n'

    final_df.to_csv('final.csv')
    with open('fin.txt', "w", encoding="utf-8") as f:
        f.write(total_text)
    finalhtmlcode='''

<!DOCTYPE html>
<html>
<head>
<style>
h1 {
  color:#edf2f7;
  font-family: verdana;
  font-size: 300%;
  text-align: center;	
}

h2 {
  color: #edf2f7;
  font-family: verdana;
  font-size: 200%;
  text-align: center;
}
p  {
  color: black;
  font-family: courier;
  font-size: 100%;
  margin-top: 1px;
  margin-bottom: 1px;
  margin-right: 150px;
  margin-left: 80px;
  text-align: center;
}

#p01 {
  color: #edf2f7;
  background-color: yellow;
  font-family: courier;
  font-size: 100%;
  margin-top: 1px;
  margin-bottom: 1px;
  margin-right: 150px;
  margin-left: 80px;
  text-align: center;
}

body {
  background-color: #0275D8;
}
img {
  display: block;
  margin-left: auto;
  margin-right: auto;
  margin-top: 20px;
  margin-bottom: 20px;
  width: 40%;
}

table 
{
  border: 1px solid black;
  border-collapse: collapse;
  width: 60%;
  text-align:center;
  align:center;
  margin-top: 20px;
  margin-bottom: 20px;
  margin-left: auto;
  margin-right: auto;
}

th {
  text-align: center;'
  border: 1px solid black;
  background-color: lightblue;
  color: white;
  
}

tr:hover {background-color: #f5f5f5;}
tr:nth-child(even) {background-color: yellow;}

td {
  
  vertical-align: bottom;
  border: 1px solid black;
}

</style>
</head>
<body>

<div>
    <button type="button" onclick="window.location.href='{{ url_for( 'links' ) }}';">See related links</button>
</div>

{% if trigger %}
<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
 <div class="modal-dialog modal-dialog-centered" role="document">
  <div class="modal-content">
   <div class="modal-header">
    <h5 class="modal-title" id="exampleModalLongTitle">Modal title</h5>
    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button>
   </div>
   <div class="modal-body">
    ...
   </div>
   <div class="modal-footer">
    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
   </div>
  </div>
 </div>
</div>
{% endif %}

''' + finalhtmlcode + '''
</body></html>
'''

    #finalhtmlcode=remove_clean(finalhtmlcode)
    try:

        with open('templates/finalhtmlfile.html', "w", encoding="utf-8") as f:
            f.write(finalhtmlcode)
    except UnicodeEncodeError:
        finalhtmlcode=remove_clean(finalhtmlcode)
        with open('templates/finalhtmlfile.html', "w", encoding="utf-8") as f:
            f.write(finalhtmlcode)




    
    end=time.time()
    timetaken=end-start
    print('Successfully created notes file: ')

    
    cwd='./templates'
    print(cwd)
    for file in os.listdir(cwd):
        #print(file)
        if file.endswith(".png") or file.endswith(".jpg"):
            if file not in all_images:
                os.remove('./templates/'+file)
    print("--- %s seconds ---" % (time.time() - start))

    
def essen2():
    mypath = "./upload"

    directory = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]

    #directory=['1.pptx','15.pptx','16.pptx','22.pptx','21.pptx','23.pptx']
    main(directory)



