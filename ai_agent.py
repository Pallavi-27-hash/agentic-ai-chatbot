# ai_agent.py
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

# Load API keys from .env
load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    # Automatically switch to Groq if OpenAI hits quota
    if provider == "OpenAI":
        try:
            llm = ChatOpenAI(model=llm_id)
        except Exception as e:
            print("OpenAI failed, switching to Groq:", e)
            llm = ChatGroq(model="llama-3.3-70b-versatile")
    elif provider == "Groq":
        llm = ChatGroq(model=llm_id)
    else:
        raise ValueError("Invalid provider")

    tools = [TavilySearch(max_results=2)] if allow_search else []

    agent = create_react_agent(
        model=llm,
        tools=tools
    )

    state = {
        "messages": [
            ("system", system_prompt),
            ("user", query)
        ]
    }

    response = agent.invoke(state)
    messages = response.get("messages", [])
    ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]
    return ai_messages[-1] if ai_messages else None