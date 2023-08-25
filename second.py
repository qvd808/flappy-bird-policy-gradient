from langchain.document_loaders import TextLoader
from dotenv import load_dotenv
load_dotenv()
loader = TextLoader("test.txt")
documents = loader.load()

from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter()
splits = splitter.split_documents(documents)

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

embeddings = OpenAIEmbeddings()
index = FAISS.from_documents(documents=splits, embedding=embeddings)

from langchain.llms import HuggingFaceLLM

llm = HuggingFaceLLM(model_name="deepset/bert-base-cased-squad2")

from langchain.chains import QuestionAnsweringChain

qa_chain = QuestionAnsweringChain(llm=llm, index=index)

qa_chain.run(question="What is Langchain?")
