import os
from getpass import getpass
from langchain.llms.huggingface_hub import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Setup
# if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
#     HUGGINGFACEHUB_API_TOKEN = getpass(prompt="Hugging Face access token: ")
#     os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN
os.environ["HUGGINGFACEHUB_API_TOKEN"]= "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"

# Prepare example
question = "Who won the FIFA World Cup in the year 1994? "
template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

# Flan by Google
# repo_id = "google/flan-t5-xxl"  # See https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads for some other options
repo_id = "Vision-CAIR/MiniGPT-4"
llm = HuggingFaceHub(
    repo_id=repo_id,
    model_kwargs={"temperature": 0.5, "max_length": 64},
)
llm_chain = LLMChain(prompt=prompt, llm=llm)

print(llm_chain.run(question))