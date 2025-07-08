from agents import Agent, Runner, trace, function_tool
from pypdf import PdfReader
import os
import requests

pushover_url = "https://api.pushover.net/1/messages.json"
@function_tool
def record_email(text:str):
    
    requests.post(
        pushover_url,
        data={
            "token":os.getenv("PUSHOVER_TOKEN"),
            "user":os.getenv("PUSHOVER_USER"),
            "message":text
        }
    )

@function_tool
def record_question(question:str):
    requests.post(
        pushover_url,
        data={
            "token":os.getenv("PUSHOVER_TOKEN"),
            "user":os.getenv("PUSHOVER_USER"),
            "message":question
        }
    )

class Me:

    def __init__(self) -> None:
        self.name = "Ramya Rajaram"
        reader = PdfReader("uploads/linkedin.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        with open("uploads/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()

    def system_prompt(self):
            system_prompt = f"""You are acting as {self.name}. You are answering questions on {self.name}'s website, \
            particularly questions related to {self.name}'s career, background, skills and experience. \
            Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
            You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
            Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
            If you don't know the answer to any question, use your record_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
            If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_email tool. After recording the email, give an appropriate response. \
            """
            system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
            system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}"
            
            return system_prompt

    async def chat(self,message,history): #history not needed here as Agent takes care of it internally
        agent = Agent(name="me",instructions=self.system_prompt(),model="gpt-4o-mini",tools=[record_email, record_question])
        with trace("conversational portfolio"):
            result = await Runner.run(agent,message)
            return result.final_output

 