import streamlit as st
import gpt_2_simple as gpt2
import tensorflow as tf
import nlp_utils
import SessionState

tf.reset_default_graph()
sess2 = gpt2.start_tf_sess()
gpt2.load_gpt2(sess2,run_name ="run1")

# Function to Generate Headlines
def text_analyzer(my_text,temp,top_k,n_samples,batch_size,length,r=gpt2):

  gen = r.generate(sess2,
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


st.title("Automated Headline Generation")

#tokenization
st.subheader("Generate a Headline For Your Text")
message = st.text_area("Enter your text","Type Here")
temp = st.slider("Select Temperature",0.1,0.9)
top_k = st.slider("Select K[Top K Sentences Selected]",35,45)
n_samples = st.slider("Select Number of Samples",1,10)
batch_size = st.slider("Select Batch Size",1,10)
length = st.slider("Select Length",150,300)

state = SessionState.get(nlp_result = [])

if st.button("Generate"):
  state.nlp_result = text_analyzer(message,temp,top_k,n_samples,batch_size,length,gpt2)
  st.json(state.nlp_result)


diverse_n = st.slider("Select Number of Sentences to Diversify :",1,10)

if st.button("Diversify"):
  nlp_result2 = nlp_utils.diversify(state.nlp_result,diverse_n)
  st.json(nlp_result2)


st.sidebar.subheader("About App")
st.sidebar.text("NLP App with GPT2 under the hood")
st.sidebar.info("Made with <3 by Citrusberry")


st.sidebar.subheader("Courtesy")
st.sidebar.text("Citrusberry Business Solutions")
