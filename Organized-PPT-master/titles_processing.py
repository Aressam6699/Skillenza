from collections import OrderedDict
import spacy
import re
import warnings
warnings.filterwarnings('ignore')

nlp = spacy.load("en_core_web_sm")

def gettitles(pptcontent):
    titles=[]
    for slide in pptcontent:
        titles+=pptcontent[slide][0]
    #print(titles)
    return titles
        

def titles_processing(contents):
    
    c=0
    final_list_of_titles=[]
    similiar_titles=[]
    
    escapes = ''.join([chr(char) for char in range(1, 32)])
    translator = str.maketrans('', '', escapes)
    
    for ppt in contents:
        titles=gettitles(contents[ppt])
        g=[]
        for f in titles:
            f = f.translate(translator)
            f=f.strip()
            if len(f)>2:
                g.append(f)
        seen = set()
        unique_data = []
        for x in g:
            if x not in seen:
                unique_data.append(x)
                seen.add(x)
        titles=unique_data

        if c==0:
            ddd=[]
            for i in titles:
                ddd.append((ppt,i))
            final_list_of_titles+=ddd
        else:
            p=[]
            for i in final_list_of_titles:
                
                curr = nlp(i[1])
                cc=' '.join([str(t) for t in curr if not t.is_stop])
                flop1=nlp(cc)
                cc=cc.split()


                if len(cc)<1:
                    continue

                for j in titles:
                    new = nlp(j)
                    nc=' '.join([str(t) for t in new if not t.is_stop])
                    
                    flop2=nlp(nc)
                    nc=nc.split()
                    if len(nc)<1:
                        continue

                    inter=len(list(set(cc) & set(nc)))
                    universe=len(list(set(cc+nc)))
                    percent=inter/universe
                    
                    similarity=flop1.similarity(flop2)
                    
                    #print(similarity)
                    
                    
                    if similarity>0.7 or percent>0.4:
                        #print(percent,' - ',i,' & ',j)
                        similiar_titles.append((i[1],j))
                    p.append(j)
            ggg=[]
            for i in p:
                ggg.append((ppt,i))
            final_list_of_titles+=ggg              
        c+=1
        
        
    seen = set()
    unique_data = []
    for x in similiar_titles:
        if x not in seen:
            unique_data.append(x)
            seen.add(x)
    similiar_titles=unique_data
    return final_list_of_titles, similiar_titles
        
            
  
#final_list_of_titles, similiar_titles=titles_processing(contents)       



