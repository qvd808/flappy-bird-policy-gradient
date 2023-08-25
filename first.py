from dotenv import load_dotenv
from langchain import HuggingFaceHub, LLMChain
from langchain.prompts import PromptTemplate
import os

HUGGINGFACEHUB_API_TOKEN = "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"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN


llm = HuggingFaceHub(repo_id= "heegyu/LIMA2-13b-hf")

hub_chain = LLMChain("What is the meaning of life?")