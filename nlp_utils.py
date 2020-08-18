from PyDictionary import PyDictionary
dictionary=PyDictionary()
import nltk
from nltk import word_tokenize
import numpy as np

def get_words(sent):
  res = []
  text = word_tokenize(sent)
  taglist = nltk.pos_tag(text)
  for i in range(len(taglist)):
    if taglist[i][1] == "JJ" or taglist[i][1] == "JJR" or taglist[i][1] == "JJS"  or taglist[i][1] == "NN" or taglist[i][1] == "NNS" or taglist[i][1] == "NNP" or taglist[i][1]=='NNPS':
      ss = dictionary.synonym(taglist[i][0])
      if ss:
        ss.insert(0,taglist[i][0])
        res.append(ss)
      else:
        res.append([taglist[i][0]])
    else:
      res.append([taglist[i][0]])
  return res,taglist,sent

def diversify_sent(wordlist,taglist,sent,n):
  sents = [sent]
  for i in range(n):
    s = ""
    for j in wordlist:
      s+=np.random.choice(j)+" "
    sents.append(s)
  return sents

def diversify(heads,n):
  res = {}
  for head in heads:
    r,t,s = get_words(head)
    res[head] = diversify_sent(r,t,s,n)
  return res
