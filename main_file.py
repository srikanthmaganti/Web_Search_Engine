from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import math
import operator
import string
import pickle
import easygui as eg
import json
each_doc_length={}   #Each document length
total_docs=3000      #Total no of documents
idf={}               #Store IDF values


with open('tf.pickle', 'rb') as f:
    tf=pickle.load(f)
    #tf_idf=pickle.load(f)
with open('docnum_tokens.pickle', 'rb') as f:
    docs=pickle.load(f)

with open('url_dict.pickle', 'rb') as f:
    links=pickle.load(f)

tf_idf=tf 
def calc_tf_idf(word, doc):
    # putting tfidf into inverted index
    tf_idf[word][doc] = tf[word][doc] * idf[word]
    return tf_idf[word][doc]

def calc_idf(tf):
    doc_freq,idf={},{}
    for key in tf.keys():
        doc_freq[key] = len(tf[key].keys())
        idf[key] = math.log(total_docs/ doc_freq[key], 2)

    return idf


def calc_doc_lengths(docs_tokens):
    for doc_num in range(total_docs+1):
        tokens_set,length,tokens=[],0,docs_tokens[str(doc_num)]
        for token in tokens:
            if token not in tokens_set:
                length+=calc_tf_idf(token,str(doc_num))**2
                tokens_set.append(token)
        each_doc_length[str(doc_num)] = math.sqrt(length)       
    return each_doc_length




def calc_cosine_similarities(query,doc_length):
    query_sos=0
    cnt = Counter()
    cos_sim = {}
    #inverted_indextfidf=compute_all_tf_idf()
    for each_word in query:
        cnt[each_word] =cnt[each_word] + 1
    for word in cnt.keys():
        query_sos =query_sos + (cnt[word]*idf.get(word, 0)) ** 2
    query_sos=math.sqrt(query_sos)
    
    for each_word in query:
        #word_in_query = idf.get(each_word, 0)
        if idf.get(each_word,0)!=0:
            for doc in tf_idf[each_word].keys():
                cos_sim[doc] = cos_sim.get(doc, 0) + tf_idf[each_word][doc] * idf.get(each_word,0)
      
    for each_doc in cos_sim.keys():
        cos_sim[each_doc] = cos_sim[each_doc] / ((doc_length[each_doc])*(query_sos))
             
    return cos_sim

def retrieve_most_relevant(query_tokens,doc_length):
    similarity=calc_cosine_similarities(query_tokens,doc_length)
    order=sorted(similarity.items(), key=operator.itemgetter(1), reverse=True)
    return order
# def score(pageranks, query):
#     prob_query = {}
#     ranks = {}
#     query = word_tokenize(query)
#     query = stemmer_porter(query)
#     for word in query:
#         if word=='uic':
#             prob_query[word]=0
#         else:
#             prob_query[word] = 1/len(query)
#     for doc in pageranks:
#         ranks[doc] = sum(prob_query[word]*pageranks[doc][word] if word in pageranks[doc] else 0 for word in query)
#     return ranks
# def return_links_pagerank(ranks,more_results):
#     if more_results:
#         top = 200
#     else:
#         top = 10
#     results = sorted(ranks.items(), key=lambda x: (-x[1], x[0]))[0:top]
#     return results
def stemmer_porter(arr):  # function to apply stemming on the words
    stemmer = PorterStemmer()
    arr = [stemmer.stem(i) for i in arr]
    return arr
# def load_json(name):
#     with open(name+'.json') as json_data:
#         return json.load(json_data)


def print_output(top):
    linkvals=[]
    if len(top)<20:
        for i in range(len(top)):
            l=top[i][0]
            if(links[int(l)]==None):
                return linkvals
                exit()
            elif(links[int(l)]!=None):
                #print(links[int(l)])
                linkvals.append(links[int(l)])
            else:
                return linkvals
        return linkvals
    for i in range(20):
        l=top[i][0]
        if(links[int(l)]==None):
            return linkvals
            exit()
        elif(links[int(l)]!=None):
            #print(links[int(l)])
            linkvals.append(links[int(l)])
        else:
            return linkvals
    return linkvals

def exit_engine():
    exit
def get_input(msg, title):
    text = eg.enterbox(msg, title)
    if text is None:
        exit
    
    return text
def display_main_menu():
    
    msg ="                               Choose one option                                             "
    
    title = "Search in UIC"
    choices = ["search query", "Exit"]
    choice = eg.buttonbox(msg, title, choices=choices)
    return choice
def load_json(name):
    with open(name+'.json') as json_data:
        return json.load(json_data)

def execute_function(main_menu_choice):
    switcher = {
        
        'search query': search,
        'Exit': exit_engine,
    }
    # Get the function from switcher dictionary
    func = switcher.get(main_menu_choice, lambda: "nothing")
    return func()
def return_links(tfidf_val,more_results):
    if more_results:
        top = 20
    else:
        top = 10
    results = tfidf_val[0:top]
    return results
def search():
    msg ="                                      Query on UIC                                             "
    
    title = "Search in UIC"
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    text=get_input(msg, title)
    if text is None:
        exit
    query = text
    for c in string.punctuation:

        query=query.replace(c,"")           #Removes Punctuations

    query = ''.join(i for i in query if not i.isdigit())          #Removes Numbers from the text
    query=query.lower()
    #ranks_pagerank=score(pageranks,query)
    #print(pageranks[str(2861)])
    #print(ranks_pagerank)
    #pagerank_results,pagerank=return_links_pagerank(ranks_pagerank,True),[]
    #for i in pagerank_results:
        #pagerank.append(links[int(i[0])])

    f = word_tokenize(query)
    f= [ps.stem(x) for x in f if x not in stop_words]              #Removes stop words and performs stemming

    unique=set(f)                                                       #To remove duplicates
    top=retrieve_most_relevant(unique,doc_length)
    tfrank=print_output(top)
    tfidfrank=["SHOW MORE RESULTS"]+tfrank
    #main_tfidfrank=tfidfrank[:10]
    #ranks = score(pageranks, text)
    #querypagerank=["SHOW MORE RESULTS"]+pagerank
    
    more_results=False
    results = return_links(tfidfrank,more_results)
    r=[i[0] for i in results]
    
    r=["SHOW MORE RESULTS"]+r
    
    msg="Confirm query: "+str(text)+" "
    title="Search in UIC"
    choices = ["Confirm query","Retype query"]
    choice = eg.buttonbox(msg, title, choices=choices)
    if choice=="Confirm query":
        if len(top)<10:
            msg = "Cosine Similarity \nGiven query:"+str(text)+"\nThere are only "+str(len(top))+" results of your query"
            x=eg.choicebox(msg, "SearchEngine results", results)
        else:

            msg = "Cosine Similarity \nGiven query:"+str(text)+"\nTop 10 results of your query"
            x=eg.choicebox(msg, "SearchEngine results", results)
        
        if x=="SHOW MORE RESULTS":
            eg.msgbox(msg="You have chosen for show more results")
            more_results=True
            results = return_links(tfidfrank,more_results)
            #r=[i[0] for i in results]
            msg = "Cosine Similarity \nGiven query:"+str(text)+"\nTop 20 results of your query"
            l=eg.choicebox(msg, "SearchEngine results", results)
            if l:
                choice=display_main_menu()
                execute_function(choice)
                
            
        if x!="SHOW MORE RESULTS":
            choice=display_main_menu()
            execute_function(choice)
    else:
        choice=display_main_menu()
        execute_function(choice)
    # else:
    #     msg = "PageRank\n"+str(text)+"\nTop 10 results of your query"
    #     x=eg.choicebox(msg, "SearchEngine results", querypagerank[:10])
        
    #     if x=="SHOW MORE RESULTS":
    #         eg.msgbox(msg="You have chosen for show more results")
    #         #more_results=True
    #         #results = return_links(tfidfrank,more_results)
            
            
    #         msg = "PageRank\n"+str(text)+"\nTop 20 results of your query"
    #         l=eg.choicebox(msg, "SearchEngine results", querypagerank)
    #         if l:
    #             choice=display_main_menu()
    #             execute_function(choice)
                
            
    #     if x!="SHOW MORE RESULTS":
    #         choice=display_main_menu()
    #         execute_function(choice)
        
    
    return True


if __name__=="__main__":

    idf=calc_idf(tf)
    doc_length=calc_doc_lengths(docs)
    #pageranks = load_json("querydependentrank")
    search()


