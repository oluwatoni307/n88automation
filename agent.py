from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from prompt import *
from model import *

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
api_key = os.getenv("OPENAI_API_KEY")

model = init_chat_model("gpt-4o-mini", model_provider="openai", api_key=api_key)


def choicefunc(transcript):
    choicemodel = model.with_structured_output(Choose)
    # Initial summary
    choice_prompt = ChatPromptTemplate(
        [
            ("system", choice_prompt),
            ("human", " {input}"),
        ]
    )
    chooser = choice_prompt | choicemodel

    choice: Choose = chooser.invoke({"input": transcript})
    return choice.choice


def process(transcript):
    processmodel = model.with_structured_output(SalesBrief)
    # Initial summary
    process_template = ChatPromptTemplate(
        [
            ("system", process_prompt),
            ("human", " {input}"),
        ]
    )
    processor = process_template | processmodel

    data: SalesBrief = processor.invoke({"input": transcript})
    return data


def briefDesigner(salesData):
    # Initial summary
    brief_prompt = ChatPromptTemplate(
        [
            ("system", brief_generation),
            ("human", " {input}"),
        ]
    )
    salesAgent = brief_prompt | model | StrOutputParser()

    salesBrief = salesAgent.invoke({"input": salesData})
    return salesBrief


def emailDesigner(salesData):
    # Initial summary
    email_template = ChatPromptTemplate(
        [
            ("system", email_prompt),
            ("human", " {input}"),
        ]
    )
    emailAgent = email_template | model | StrOutputParser()

    email = emailAgent.invoke({"input": salesData})
    return email


def fullprocess(trancript):
    ischoice = choicefunc(trancript)
    data = {"ischoice": ischoice, "process": None, "brief": None, "email": None}
    if ischoice:
        structuredData = process(trancript)
        brief = briefDesigner(structuredData)
        email = emailDesigner(structuredData)
        data["process"] = structuredData
        data["brief"] = brief
        data["email"] = email
    return data
