from agents import OpenAIChatCompletionsModel, Agent, Runner, trace
from dotenv import load_dotenv
import gradio as gr
from openai import AsyncOpenAI
import os

#from noagent import Me
from openaiagent import Me

load_dotenv(override=True)

if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat,type="messages").launch()