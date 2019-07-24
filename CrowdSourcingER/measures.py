import py_stringmatching as sm

alnum_tok = sm.AlphanumericTokenizer()
qg3_tok = sm.QgramTokenizer(qval=3)

jac = sm.Jaccard()
lev = sm.Levenshtein()

def calcola_similarita(string1, string2):
    a = jac.get_sim_score(alnum_tok.tokenize(string1),alnum_tok.tokenize(string2))
    b = lev.get_sim_score(string1,string2)
    c = jac.get_sim_score(qg3_tok.tokenize(string1),qg3_tok.tokenize(string2))
    return [{"alnum_jac" : a},{"alnum_lev" : b}, {"qg3_jac" : c}]

def add_features(elem):
    line,count = elem
    title1 = line[4]
    director1 = line[3]
    date1=line[5]
    title2=line[7]
    director2=line[6]
    date2=line[8]
    return (line+(calcola_similarita(title1,title2),calcola_similarita(director1,director2),\
    calcola_similarita(date1,date2)),count)

def precision(true):
    tp = true.map(lambda row:("true",row.response))\
                .reduceByKey(lambda x,y:x+y)\
                .collect()[0][1]

    fp = true.filter(lambda row: row.response==0).count()
    return ((tp/(tp+fp))*100)
