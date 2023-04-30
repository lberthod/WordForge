# based on this github : https://github.com/nicknochnack/Langchain-Crash-Course
# Bring in deps
import os 

import streamlit as st 
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory
from langchain.utilities import SerpAPIWrapper
from langchain.agents import Tool
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool
    
os.environ['OPENAI_API_KEY'] = st.secrets["auth"]

# App framework
st.set_page_config(
   page_title="wordForge",
   page_icon="🧊",
)

st.title('🔗💬 WORD FORGE')
st.write('wordForge is a AI applications tools to help your to create your contents for your product page in your ecommerce.')
st.info('WordForge is requesting the information below in order to generate the most accurate content possible for you. All of the information is optional and helps improve the accuracy of the generated output.')
st.title('Content s')
st.info('In this  input, you will give some information about the structure and the tone of communication for the text')

language = st.radio(
    "Which language do you want to use",
    ('English', 'French', 'German','Italian' ))

size = st.slider('On a scale of 1 to 4, what size description do you want?', 1, 4, 2)
prompt_tone = st.text_area('Explain your tone of the communication') 

tone_list = st.multiselect(
    'Add some tone you will use?',
    ['Affirmative', 'Negative', 'Interrogative', 'Exclamatory','Sarcastic', 'Formal', 'Relax' , 'Authoritative','Rational', 'Emotional'],
    ['Affirmative'])

st.title('Explain your product')
st.info('In this  input, you can give information abour your product and your company to help wordForge to generate a precise text for you')

prompt_title = st.text_input('Title of product') 
prompt_explanation_product = st.text_area('Explain your product') 
prompt_explanation_market = st.text_area('Explain the market') 
prompt_characteristic = st.text_area('Characteristic of the product') 
prompt_supplyer = st.text_area('Who is the supplyer') 

persona_list = st.multiselect(
    'Add some adjectivs for your persona?',
    ['Young', 'Active', 'Interrogative', 'Outgoing','Environmentalist', 'Loyal', 'Relax' , 'Innovative','High-income', 'Urban'],
    ['Active'])

prompt_seo= st.text_area('What is SEO keyword') 

# Prompt templates
title_template = PromptTemplate(
    input_variables = ['topic'], 
    template='You are an expert in communication. You need to write the title of this product : : {topic}'
)

summary_template = PromptTemplate(
    input_variables = ['title', 'prompt_tone', 'tone_list', 'prompt_explanation_product', 'prompt_explanation_market', 'prompt_characteristic', 'prompt_seo', 'prompt_supplyer'], 
    template='You are an honest professional copywriter. You make perfect documents in flowing text. write me the 100 words description of the description Focus on your ideal buyer Entice with benefits Avoid "yeah,yeah" sentences ustify using superlatives Appeal to your readers imagination Cut through the rational barriers with mini-stories Seduce with sensory words Tempt with social proof of maximum 100 words for the {title} by writing in a manner {prompt_tone} based on a style of writing {tone_list} knowing that the explanation of the product is the following {prompt_explanation_product} considering that the market is the following {prompt_explanation_market} by explaining the characteristics of the following products {prompt_characteristic} by integrating the following words {prompt_seo} at least twice to improve SEO. supplier is {prompt_supplyer}')

characteristics_template = PromptTemplate(
    input_variables = ['title' , 'prompt_characteristic','prompt_supplyer'], 
    template='You are an honest professional copywriter. Write me a quality bulleted list for the features of this product. nicely and cleanly formatting for the {title} with the following product characteristic {prompt_characteristic}. You must write only on the transmitted characteristics. supplier is {prompt_supplyer} ')

resume30_template = PromptTemplate(
    input_variables = ['summary' , 'prompt_seo', 'prompt_tone', 'tone_list'], 
    template=' Rewrite this text in 40 words: {summary} in a professional copywriterr quality text.  Based on this {summary}. {prompt_tone} based on a style of writing {tone_list}. by integrating the following words at least 2 or 3 time : {prompt_seo} for SEO referencement '    
)

resume50_template = PromptTemplate(
    input_variables = ['summary' , 'prompt_seo', 'prompt_tone', 'tone_list'], 
    template=' Rewrite this text in 75 words: {summary} in a professional copywriterr quality text.  {prompt_tone} based on a style of writing {tone_list}. by integrating the following words at least 2 or 3 time : {prompt_seo} for SEO referencement   '    
)  

resume75_template = PromptTemplate(
    input_variables = ['summary', 'prompt_seo', 'prompt_tone', 'tone_list' ], 
    template=' Rewrite this text in 10 words: {summary} in a professional copywriterr quality text.  Based on this {summary}. {prompt_tone} based on a style of writing {tone_list}  . by integrating the following words at least 2 or 3 time : {prompt_seo} for SEO referencement '    
)  

resume100_template = PromptTemplate(
    input_variables = ['summary', 'prompt_seo', 'prompt_tone', 'tone_list'], 
    template=' Write the first part this text in 120 words: {summary} in a professional copywriterr quality text.  Based on this {summary}. {prompt_tone} based on a style of writing {tone_list}  . by integrating the following words at least 2 or 3 time : {prompt_seo} for SEO referencement '    
)

resume_two_100_template = PromptTemplate(
    input_variables = ['rep4', 'summary', 'prompt_seo', 'prompt_tone', 'tone_list'], 
    template=' Your are  a professional copywriterr quality . Write the second paragraph after this text : {rep4} . Write another kind of sentence than his a previous paragraph. Based on this summary : {summary}. {prompt_tone} based on a style of writing {tone_list}. by integrating the following words at least 2 or 3 time : {prompt_seo} for SEO referencement'    
)

resume_three_100_template = PromptTemplate(
    input_variables = ['rep4', 'rep5', 'summary', 'prompt_seo', 'prompt_tone', 'tone_list'], 
    template=' Your are  a professional copywriterr quality . Write another innovant and quality  paragraph after this text : {rep4}  {rep5}. Write another kind of sentence than his a previous paragraph.  Based on this summary : {summary}. {prompt_tone} based on a style of writing {tone_list}. by integrating the following words at least 2 or 3 time : {prompt_seo} for SEO referencement'    
)

# Memory 
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
summary_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')
characteristics_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')
resume30_memory = ConversationBufferMemory(input_key='summary', memory_key='chat_history')
resume50_memory = ConversationBufferMemory(input_key='summary', memory_key='chat_history')
resume75_memory = ConversationBufferMemory(input_key='summary', memory_key='chat_history')
resume100_memory = ConversationBufferMemory(input_key='summary', memory_key='chat_history')
resume_two_100_memory = ConversationBufferMemory(input_key='summary', memory_key='chat_history')
resume_three_100_memory = ConversationBufferMemory(input_key='summary', memory_key='chat_history')

# Llms
llm = OpenAI(temperature=0.9) 
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)
summary_chain = LLMChain(llm=llm, prompt=summary_template, verbose=True, output_key='summary', memory=summary_memory)
characteristics_chain = LLMChain(llm=llm, prompt=characteristics_template, verbose=True, output_key='characteristics', memory=characteristics_memory)
resume30_chain = LLMChain(llm=llm, prompt=resume30_template, verbose=True, output_key='rep', memory=resume30_memory)
resume50_chain = LLMChain(llm=llm, prompt=resume50_template, verbose=True, output_key='rep2', memory=resume50_memory)
resume75_chain = LLMChain(llm=llm, prompt=resume75_template, verbose=True, output_key='rep3', memory=resume75_memory)
resume100_chain = LLMChain(llm=llm, prompt=resume100_template, verbose=True, output_key='rep4', memory=resume100_memory)
resume100_two_chain = LLMChain(llm=llm, prompt=resume100_template, verbose=True, output_key='rep5', memory=resume100_memory)
resume100_three_chain = LLMChain(llm=llm, prompt=resume100_template, verbose=True, output_key='rep6', memory=resume100_memory)

# Show stuff to the screen if there's a prompt
if st.button('Start running'):

    title = title_chain.run(prompt_title)
    st.write('Size of text ', size)
    st.info('Titre : \n' +  title)
    summary = summary_chain.run(title=title, prompt_tone=prompt_tone, tone_list=tone_list, prompt_explanation_product=prompt_explanation_product, prompt_explanation_market=prompt_explanation_market, prompt_characteristic=prompt_characteristic, prompt_seo=prompt_seo, prompt_supplyer=prompt_supplyer)
    st.info('Main Description : \n ' + summary)

    if size  == 1:
        rep = resume30_chain.run(summary=summary, prompt_seo=prompt_seo, prompt_tone=prompt_tone, tone_list=tone_list)
        st.info('Short Description : \n ' + rep)

    if size  == 2:
        rep3 = resume75_chain.run(summary=summary, prompt_seo=prompt_seo, prompt_tone=prompt_tone, tone_list=tone_list)
        st.info('Medium Description : \n ' + rep3)
     
    if size  == 3:
        rep4 = resume100_chain.run(summary=summary, prompt_seo=prompt_seo, prompt_tone=prompt_tone, tone_list=tone_list)
        rep5 = resume100_two_chain.run(rep4=rep4 ,summary=summary, prompt_seo=prompt_seo, prompt_tone=prompt_tone, tone_list=tone_list)
        st.info('Large Description : \n ' + rep4 + '\n\n' + rep5)

    if size  == 4:
        rep4 = resume100_chain.run(summary=summary, prompt_seo=prompt_seo, prompt_tone=prompt_tone, tone_list=tone_list)
        rep5 = resume100_two_chain.run(rep4=rep4 ,summary=summary, prompt_seo=prompt_seo, prompt_tone=prompt_tone, tone_list=tone_list)
        rep6 = resume100_three_chain.run(rep4=rep4 , rep5=rep5 ,summary=summary, prompt_seo=prompt_seo, prompt_tone=prompt_tone, tone_list=tone_list)
        st.info('Large Description : \n ' + rep4 + '\n\n' + rep5 + '\n\n' + rep6)

    if prompt_characteristic  != "":
        characteristics = characteristics_chain.run(title=title,prompt_characteristic=prompt_characteristic ,prompt_supplyer=prompt_supplyer)
        st.info('Characterisics : \n' +  characteristics)
