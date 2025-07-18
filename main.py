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
    with gr.Blocks(theme=gr.themes.Soft()) as chat:
        gr.Markdown("""
                    ## 👋 Hi, I'm Ramya Rajaram's AI Twin
                    I'm here to answer your questions about my career, background, skills, and projects.
                    Feel free to chat with me — this helps both of us save time before a formal interview!
                    """)
        gr.ChatInterface(me.chat, type="messages",head="Ramya Rajaram's AI Twin - Conversational Portfolio Assistant",chatbot=gr.Chatbot(height=700,type="messages"))
    chat.launch()
    