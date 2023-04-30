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

st.title('🔗 WORD FORGE')
st.write(', *World!* :sunglasses: WordForge help your to create your contents about your product in your e-commerce.')
st.info('WordForge is requesting the information below in order to generate the most accurate content possible for you. All of the information is optional and helps improve the accuracy of the generated output.')



st.title('Content s')

size = st.slider('How much paragraph do you want?', 1, 4, 2)




prompt_tone = st.text_area('Explain your tone of the communication') 

tone_list = st.multiselect(
    'Which tone do you use?',
    ['Affirmative', 'Negativees', 'Interrogative', 'Exclamatory','Sarcastic', 'Formal', 'Relax' , 'Authoritative','Rational', 'Emotional'],
    ['Affirmative'])




st.title('Explain your product')
st.info('oki')

prompt_title = st.text_input('Title of product') 
prompt_explanation_product = st.text_area('Explain your product') 
prompt_explanation_market = st.text_area('Explain the market') 
prompt_characteristic = st.text_area('Characteristic of the product') 
prompt_supplyer = st.text_area('Who is the supplyer') 
prompt_USP = st.text_area('What is your USP') 
prompt_persona = st.text_area('What is your Persona') 
prompt_seo= st.text_area('What is SEO keyword') 




# Prompt templates
title_template = PromptTemplate(
    input_variables = ['topic'], 
    template='Ecris moi le titre du produit : {topic}'
)

summary_template = PromptTemplate(
    input_variables = ['title', 'prompt_tone', 'tone_list', 'prompt_explanation_product', 'prompt_explanation_market', 'prompt_characteristic', 'prompt_seo'], 
    template='Tu es un honnête professionnel copywriter. Tu fais des documents parfais. ecris moi le premier paragraphe de 30 mots  de la description Focus on your ideal buyer Entice with benefits Avoid "yeah,yeah" phrases ustify using superlatives Appeal to your readers imagination Cut through the rational barriers with mini-stories Seduce with sensory words Tempt with social proof de maximum 30 mots pour le  {title}  en écrivant de manière de manière {prompt_tone} en te basant sur un style d ecritre {tone_list} en sachant que l explication du produit est la suivante {prompt_explanation_product} en considérant que le marché est le suivant {prompt_explanation_market} en expliquant les caractéristique du produits suivant {prompt_characteristic} en intégrant les mots suivants {prompt_seo} au minimum 2 fois pour  pour améliorer le SEO '
)

summary2_template = PromptTemplate(
    input_variables = ['title', 'prompt_tone', 'tone_list', 'prompt_explanation_product', 'summary'], 
    template='Ecris moi le second paragraphe de 100 mots de la description {summary} en faisant une transition douce  pour le  {title}  en écrivant de manière de manière {prompt_tone} en te basant sur un style d ecritre {tone_list} en sachant que l explication du produit est la suivante {prompt_explanation_product} '
)

summary3_template = PromptTemplate(
    input_variables = ['title', 'prompt_tone', 'tone_list', 'prompt_explanation_product', 'summary' , 'summary2'], 
    template='Ecris moi la suite de la description {summary} {summary2} en faisant une transition douce  pour le  {title}  en écrivant de manière de manière {prompt_tone} en te basant sur un style d ecritre {tone_list} en sachant que l explication du produit est la suivante {prompt_explanation_product} '
)

characteristics_template = PromptTemplate(
    input_variables = ['title' , 'prompt_characteristic'], 
    template='Ecris moi une liste a puce pour les caractéristique de ce produit. met en forme joliment et proprement pour le  {title}  dont les caractéristique du produits suivant {prompt_characteristic}. Tu dois écrire que sur les caractéristiques transmises '
)

competence_template = PromptTemplate(
    input_variables = ['title'], 
    template='En tant qu expert du sujet ecris moi les 3  competences principales que les étudiants universitaire vont acquéri en suivant le cours  : {title} . ecris une phrase explicative pour chaque '
)

evaluation_template = PromptTemplate(
    input_variables = ['title' ], 
    template='En tant qu expert et enseignant. Ecris moi 4 types d examen pour les etudiants universitaire pour le cours  : {title} en te basant une evaluation en pédagogie orale, ecrite, en groupe, seul, projet basé sur l acquisition des compétences '
)

scenario_template = PromptTemplate(
    input_variables = ['title' ], 
    template='En tant qu expert et enseignant. Ecris moi les quatres titre de lecons du cours  : {title}. Transmet une liste à puce.'
)

scenario1_template = PromptTemplate(
    input_variables = ['title' ], 
    template='En tant qu expert et enseignant. Ecris moi un court paragraphe sur le scenario de la première lecon du cours  : {title} en te basant sur des modalités pédagogiques variés et innovantes. C est la lecon 1 sur 4. chaque lecon dure 1h30'
)
scenario2_template = PromptTemplate(
    input_variables = ['title' ], 
    template='En tant qu expert et enseignant. Ecris moi les  trois objectifs de la première lecon du cours  : {title} . C est la lecon 1 sur 4. chaque lecon dure 1h30. ecris que trois objectifs'
)
scenario3_template = PromptTemplate(
    input_variables = ['title' ], 
    template='En tant qu expert et enseignant. Ecris moi trois et uniquement trois  modalités pédagogiques  de la première lecon du cours  : {title} en te basant sur des modalités pédagogiques variés et innovantes. C est la lecon 1 sur 4. chaque lecon dure 1h30. Il y au maximum 4 modalité pédagogique'
)

resume30_template = PromptTemplate(
    input_variables = ['summary' ], 
    template=' Reecris ce texte en 30 mots :  {summary} '
)


# Memory 
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
summary_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')
summary2_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')
summary3_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')
characteristics_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')
evaluation_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')
competence_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')
scenario_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')
scenario1_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')
scenario2_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')
scenario3_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')
resume30_memory = ConversationBufferMemory(input_key='summary', memory_key='chat_history')
#scenario4_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')


# Llms
llm = OpenAI(temperature=0.9) 
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)
summary_chain = LLMChain(llm=llm, prompt=summary_template, verbose=True, output_key='summary', memory=summary_memory)
summary2_chain = LLMChain(llm=llm, prompt=summary2_template, verbose=True, output_key='summary2', memory=summary2_memory)
summary3_chain = LLMChain(llm=llm, prompt=summary3_template, verbose=True, output_key='summary3', memory=summary3_memory)
characteristics_chain = LLMChain(llm=llm, prompt=characteristics_template, verbose=True, output_key='summary3', memory=characteristics_memory)
evaluation_chain = LLMChain(llm=llm, prompt=evaluation_template, verbose=True, output_key='title', memory=evaluation_memory)
competence_chain = LLMChain(llm=llm, prompt=competence_template, verbose=True, output_key='title', memory=competence_memory)
scenario_chain = LLMChain(llm=llm, prompt=scenario_template, verbose=True, output_key='title', memory=scenario_memory)
scenario1_chain = LLMChain(llm=llm, prompt=scenario1_template, verbose=True, output_key='title', memory=scenario1_memory)
scenario2_chain = LLMChain(llm=llm, prompt=scenario2_template, verbose=True, output_key='title', memory=scenario2_memory)
scenario3_chain = LLMChain(llm=llm, prompt=scenario3_template, verbose=True, output_key='title', memory=scenario3_memory)
resume30_chain = LLMChain(llm=llm, prompt=resume30_template, verbose=True, output_key='rep', memory=resume30_memory)
#scenario4_chain = LLMChain(llm=llm, prompt=scenario4_template, verbose=True, output_key='title', memory=scenario4_memory)


# Show stuff to the screen if there's a prompt
if st.button('Start running'):

    title = title_chain.run(prompt_title)
    summary = summary_chain.run(title=title, prompt_tone=prompt_tone, tone_list=tone_list, prompt_explanation_product=prompt_explanation_product, prompt_explanation_market=prompt_explanation_market, prompt_characteristic=prompt_characteristic, prompt_seo=prompt_seo)
    rep = resume30_chain.run(summary=summary)
  
  #  summary2 = summary2_chain.run(title=title, prompt_tone=prompt_tone, tone_list=tone_list, prompt_explanation_product=prompt_explanation_product, summary=summary)
  #  summary3 = summary3_chain.run(title=title, prompt_tone=prompt_tone, tone_list=tone_list, prompt_explanation_product=prompt_explanation_product, summary=summary, summary2=summary2) ds

   # characteristics = characteristics_chain.run(title=title,  prompt_explanation_product=prompt_explanation_product, prompt_explanation_market=prompt_explanation_market, prompt_characteristic=prompt_characteristic)
   # evaluation = evaluation_chain.run(title=title)
  #  competence = competence_chain.run(title=title)
  #  scenario = scenario_chain.run(title=title)
  #  scenario1 = scenario1_chain.run(title=title)
  #  scenario2 = scenario2_chain.run(title=title)
 #  scenario3 = scenario3_chain.run(title=title)
   # scenario4 = scenario4_chain.run(title=title)

    st.info('Titre : \n' +  title)
    st.info('Description : \n ' + summary)
  #  st.info('Characteristics : \n' +  characteristics)

 

  #  with st.expander('Evaluation du cours'): 
  #      st.info(evaluation_memory.buffer)

  #  with st.expander('Compétence du cours'): 
 #      st.info(competence_memory.buffer)
#
  #  with st.expander('Résumé du scénario du cours'): 
    #    st.info(scenario_memory.buffer)

   # with st.expander('Introduction de la lecon 1'): 
   #     st.info(scenario1_memory.buffer)

   # with st.expander('Objectifs de la lecon 1'): 
  #      st.info(scenario2_memory.buffer)

   # with st.expander('Modalité de la lecon 1'): 
     #   st.info(scenario3_memory.buffer)

