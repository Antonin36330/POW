import os
from dotenv import load_dotenv
import sys
from langchain.memory import ChatMessageHistory
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.prompts import PromptTemplate
from langchain import PromptTemplate
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationSummaryBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from bs4 import BeautifulSoup
import requests
import json
import slack_sdk
import re

load_dotenv()

browserless_api_key = os.getenv("BROWSERLESS_API_KEY")
serper_api_key = os.getenv("SERP_API_KEY")

def find_links(text):
    pattern = r'https?://[^\s<>")]+|www\.[^\s<>")]+'
    return re.findall(pattern, text)

def script_verifier(script):

    chat = ChatOpenAI(temperature=0, model_name=os.getenv("GPT_VERSION"))

    prompt=f"""
    From this transcript:

    0:02 So, hi team now handling Jordan of Hubei chat so they wanted us to delete the following campaigns so I'll just go over to the admin page and go umm so I went over to the admin page and then went to you their campaigns view more umm and then they have this campaign Yay.
    0:58 Soooooo. Thanks watching! Okay, and click here, and then. Mm hmm. You can click the add there, and then. So they wanted this test test.
    1:35 And. And just delete. And delete. Come back. The next we have. Okay we're done. You okay now it's pretty really good.
    2:28 Umm, it's finder 2. You So I'm fit finder 1, 2. So I'm just going here and then, So they wanted us to fit finder 1, 2.
    3:11 So okay. I want this to be deleted. Just click. Thank you. There. This is done. If we click, it's deleted.
    3:44 And then, we also want to delete the stress. Shhhhhhhh shhhhhh. Just in YC. Shylah. Shylah NYC. Shylah NYC. And everything.
    4:28 So ready deleted. And next. We have last. Stay here at home. Okay, let's just, Okay, stay here at home. Thank you.
    5:14 Then if we check fresh, in case of, okay so that's the last one i'm just going to check again here they have here no.
    6:06 And then if they have this, no. Let's check here no. And last, You Okay. So ready deleted and last one.
    6:31 Okay so, You will inform them. So, hi Jordan. Jordan.. Scovidys. So done. Thank you.

    Check if this SOP list is completed:

    Example Evaluation Response
    [Done] Help with support task: identify what feature the customer is asking about. Use ChatGPT to help with this if necessary
    [Done] Check the support wiki for that feature section or support faqs to see if a help doc is there, follow those steps. Especially the information gathering step.
    [Done] If a related SOP is not there and if you're not sure of the answer, ask the private channel
    channel for help sharing your loom and best guess at the answer, and let the customer know we're looking into it and will get back to them.
    [Done] Create draft of your response,
    [Not Done] run it through ChatGPT to check for grammar, example here.
    [Link to the time-stamped for the Team Lead to review]
    [Done] Email customer with solution or create support card in trello if necessary (e.g. we need more info from them and card doesn't already exist), share it in private channel
    [Done] Share loom to private channel
    channel, get feedback if necessary
    [N/A] Create SOP in support wiki if it doesn't exist or add it as an FAQ item within the product feature FAQ it's related to if it doesn't already exist there, if you don't have time to do it now create a card in notion and add it to the roadmap.
    [N/A] Share the Notion card or screenshot (of where it is in Support wiki) and link to SOP in private channel

    Answer only with the SOP list with ticks and crosses
    """

    history = ChatMessageHistory()

    history.clear()

    history.add_user_message(prompt)

    ai_response0 = chat(history.messages).content

    return ai_response0