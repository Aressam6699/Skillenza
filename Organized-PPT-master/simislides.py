
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
import spacy
import re
import warnings
warnings.filterwarnings('ignore')

nlp = spacy.load("en_core_web_sm")


def clean(doc):
    doc = re.sub(r'^https?:\/\/.*[\r\n]*', '', doc, flags=re.MULTILINE)
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

def remove_clean(f):
    escapes = ''.join([chr(char) for char in range(1, 32)])
    translator = str.maketrans('', '', escapes)
    f = f.translate(translator)
    f=f.strip()
    if len(f)==0:
        f=''
    return f
    
    


def lda(doc_complete,nt=2):
    
    
    doc_clean = [clean(doc).split() for doc in doc_complete] 
    
    dictionary = corpora.Dictionary(doc_clean)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    Lda = gensim.models.ldamodel.LdaModel

    # Running and Trainign LDA model on the document term matrix.
    ldamodel = Lda(doc_term_matrix, num_topics=nt, id2word = dictionary, passes=50)
    #print(ldamodel.print_topics(num_topics=nt, num_words=3))
    
    tops=[]
    #print(tops)
    
    for i, row in enumerate(ldamodel[doc_term_matrix]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                tops.append(int(topic_num))
            else:
                break
    return tops
    
    
def findsimiliarslides(contents,similiar_titles,final_list_of_titles):
    
    sim_slides=[]
    
    for simi in similiar_titles:
        #print(simi)
        
        tit1=simi[0]
        tit2=simi[1]
        #print('_____________________')
        #print(tit1)
        #print(tit2)
        for title in final_list_of_titles:
            if tit1==title[1]:
                ppt1tit=title[0]
            if tit2==title[1]:
                ppt2tit=title[0]
        
        ppt1=contents[ppt1tit]
        ppt2=contents[ppt2tit]
        
        #print(ppt1tit)
        #print(ppt2tit)
        
        #print(ppt1[257])
        for slide1 in ppt1:
            
            #print(ppt1[slide][0])
            if tit1 in ppt1[slide1][0]:
                ppt1text=ppt1[slide1][2]
                ppt1img=ppt1[slide1][3]
                break
            #print('______________')

        for slide2 in ppt2:
            
            #print(ppt2[slide2][2])
            if tit2 in ppt2[slide2][0]:
                #print('yes')
                ppt2text=ppt2[slide2][2]
                ppt2img=ppt2[slide2][3]
                break
        
        text1=' '.join(ppt1text)
        text2=' '.join(ppt2text)
        #print(ppt1img)
        #print('=====')
        #print(ppt2img)
        #print('=====')
        
        
        spt1=nlp(text1)
        spt2=nlp(text2)
        similarity=spt1.similarity(spt2)
        if similarity>0.8:
            #print('k')
            sim_slides.append({ppt2tit:slide2})
            continue
            
        
        ntopics=2
        if len(text1)>500 and len(text2)>500:
            ntopics=3
        
        
        if len(text1)>0 and len(text2)>0:
            #print('yes')
            tops=lda([text1,text2],ntopics)
            if tops[0]==tops[1]:
                if len(text1)>len(text2):
                    if len(ppt1img)>=len(ppt2img):
                        sim_slides.append({ppt2tit:slide2})
                    elif len(ppt1img)<len(ppt2img):
                        if len(text1)<150:
                            sim_slides.append({ppt1tit:slide1})
                            
                    
                else:
                    if len(ppt2img)>=len(ppt1img):
                        sim_slides.append({ppt1tit:slide1})
                    elif len(ppt2img)<len(ppt1img):
                        if len(text2)<150:
                            sim_slides.append({ppt2tit:slide2})

    
    sim_slides_restructured={}

    for i in sim_slides:
        for val in i:
            title=val
            pid=i[title]

            if title not in sim_slides_restructured.keys():
                sim_slides_restructured.update({title:[pid]})
            else:
                cur=sim_slides_restructured[title]
                if pid in cur:
                    continue
                cur.append(pid)
                sim_slides_restructured.update({title:cur})
    return sim_slides_restructured
                
 