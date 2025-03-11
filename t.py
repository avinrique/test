
from datetime import date
import re
import copy
import requests
import google.generativeai as genai
import os
import io
from PIL import Image
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
import urllib
import warnings
from pathlib import Path as p
from pprint import pprint
import pandas as pd

#langchain
from langchain_core.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma




warnings.filterwarnings("ignore")
os.environ["GOOGLE_API_KEY"] = "AIzaSyD02mt7Sejc3Ky6G7te8adqlk5BQr1ekj8"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model2 = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=1)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")




pdf_file = "./data/apass.pdf"
pdf_loader = PyPDFLoader(pdf_file)
pages = pdf_loader.load_and_split()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=0)
context = "\n\n".join(str(p.page_content) for p in pages)
texts = text_splitter.split_text(context)





prompt_template = """Answer the question as precise as possible using the provided context. If the answer is
                    not contained in the context, say "answer not available in context" \n\n
                    Context: \n {context}?\n
                    Question: \n {question} \n
                    Answer:
                  """

prompt = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)




vector_index = Chroma.from_texts(texts, embeddings).as_retriever()



while True:
    question = input(" Emter you question regarding this ")
    docs = vector_index.get_relevant_documents(question)
    stuff_chain = load_qa_chain(model2, chain_type="stuff", prompt=prompt)
    
    stuff_answer = stuff_chain(
        {"input_documents": docs, "question": question}, return_only_outputs=True
    )
    pprint(stuff_answer)







































































# question = "just describe the given pdf."
# stuff_ answer = stuff_chain(
#     {"input_documents": pages[2:10], "question": question}, return_only_outputs=True
# )
# pprint(stuff_answer)











# #initialing headers and checking statuscode
# chat.send_message(f"todays date is {date.today()}  and my name is avinav gupta , i am a student of bmsit banglore 3rd sem , my hobbies are playing basketball ,chess , call of duty and other games , reading books novels and books on pschyology , i am a programmer i know python , js well. i know a bit of java and c . i know a webdevlopment , a bit of penetration testing a, script writing , prompt engineering , a very very bit of app and game developemnt and 3d modeling , and i am trying to learn ai, i know how to program raspberry pi and i know linux . i also know a bit of automation. well i am a kinda guy who likes to learn new things. and i am from nepal born in katmandu and lived in biratnagar, you will address me as a boss and i will address you as ryan" , safety_settings={'HARASSMENT':'block_none' ,})
# chat.send_message(f"you are also a helpful assistant that helps me in my most of the works , answer like you are jarvis ")
# while True :
#     text = input("enter the prompt")
#     response = text
#     response2 = model.generate_content(f"""list all the task that are to be performed in the  prompt , where the prompt is : {response}""")
#     print(response2.text)