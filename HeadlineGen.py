import streamlit as st
import gpt_2_simple as gpt2
import tensorflow as tf
import nlp_utils
# import SessionState
import spacy
import re
import string

spacy.prefer_gpu()
nlp = spacy.load("en_core_web_sm")
tf.reset_default_graph()
sess2 = gpt2.start_tf_sess()

@st.cache
def load_gpt():
  gpt2.load_gpt2(sess2,run_name ="run1")

# Function to Generate Headlines
@st.cache
def text_analyzer(my_text,temp,top_k,n_samples,batch_size,length):

  load_gpt()
  gen = gpt2.generate(sess2,
              temperature=temp,
              top_k=top_k,
              nsamples=n_samples,
              batch_size=batch_size,
              length=length,
              prefix='<|startoftext|>~^'+my_text+" ===============SUMMARY=================",
              truncate="<|endoftext|>",
              include_prefix=False,
              sample_delim='\n',
              return_as_list=True)
  return(gen)

def fill_nums(text,head):
  if "#" in head :
    nslist = re.findall(r'\d+', text)
    hs = head.split()
    fin = []
    for i in hs:
      if "#" in i:
        ilen = len(i)
        for j in nslist :
          if ilen==len(j):
            fin.append(j)
      else:
        fin.append(i)
    return " ".join(fin)
  return head
  
def rank(main_sent,gen_list):
  res = {
      "Sentence" : [],
      "Scores" : []
  }
  for i in range(len(gen_list)):
    res["Sentence"].append(gen_list[i])
    res["Scores"].append(nlp(main_sent).similarity(nlp(gen_list[i])))
  return res



"""Main Streamlit App"""

activities = ["Headline Generation","Headline From URL"]
choice = st.sidebar.selectbox("Select Activity",activities)
st.title("Automated Text Generation")


if choice == 'Headline Generation':
  st.subheader("Generate a Headline For Your Text")
  message = st.text_area("Enter your text","Type Here")
  temp = st.slider("Select Temperature",0.1,0.9)
  top_k = st.slider("Select K[Top K Sentences Selected]",35,45)
  n_samples = st.slider("Select Number of Samples",1,10)
  batch_size = st.slider("Select Batch Size",1,10)
  length = st.slider("Select Length",150,300)

  # state = SessionState.get(Z = [],Y=[])
  Z,X=[],[]

  if st.button("Generate"):
    nlp_result = text_analyzer(message,temp,top_k,n_samples,batch_size,length)
    main_result = []
    for i in nlp_result:
      main_result.append(fill_nums(message,i))
    result = rank(message,main_result)
    Z = [x for _,x in sorted(zip(result["Scores"],result["Sentence"]),reverse=True)]
    Y = sorted(result["Scores"])
    st.success('**Best Generated Headline : **'+string.capwords(str(Z[-1])))
    st.markdown("  \n _(Score : "+str(Y[-1]*100)+"%)_")
    st.markdown("**More :**")
    for i in range(len(Z)-1,0,-1):
        st.markdown('**Generated Headline : **'+string.capwords(str(Z[i]))+"  \n _(Score : "+str(Y[i]*100)+"%)_")

if choice == 'Next Word Prediction':
  st.subheader("Generate the next part of the Text")
  message = st.text_area("Enter your text","Type Here")
  temp = st.slider("Select Temperature",0.1,0.9)
  top_k = st.slider("Select K[Top K Sentences Selected]",35,45)
  n_samples = st.slider("Select Number of Samples",1,10)
  batch_size = st.slider("Select Batch Size",1,10)
  length = st.slider("Select Length",150,300)

  # state = SessionState.get(Z = [],Y=[])
  Z,X=[],[]

  if st.button("Generate"):
    nlp_result = text_analyzer(message,temp,top_k,n_samples,batch_size,length)
    result = rank(message,nlp_result)
    Z = [x for _,x in sorted(zip(result["Scores"],result["Sentence"]),reverse=True)]
    Y = sorted(result["Scores"])
    st.markdown('**Generated Headline : **'+string.capwords(str(Z[0])))
    st.markdown("\nScore : _"+str(Y[0])+"_")
    st.markdown("**More :**")
    for i in range(len(Z)):
        st.markdown('**Generated Headline : **'+string.capwords(str(Z[i]))+"\nScore : _"+str(Y[i])+"_")


# diverse_n = st.slider("Select Number of Sentences to Diversify :",1,10)

# if st.button("Diversify"):
#   nlp_result2 = nlp_utils.diversify(state.nlp_result,diverse_n)
#   st.json(nlp_result2)


st.sidebar.subheader("About App")
st.sidebar.text("NLP App with GPT2 under the hood")
st.sidebar.info("Made with <3 by Citrusberry")


st.sidebar.subheader("Courtesy")
st.sidebar.text("Citrusberry Business Solutions")
