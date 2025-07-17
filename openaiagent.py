from agents import Agent, InputGuardrailTripwireTriggered, Runner, trace, function_tool, input_guardrail, GuardrailFunctionOutput
from pypdf import PdfReader
import os
import requests
import re

pushover_url = "https://api.pushover.net/1/messages.json"
EMAIL_REGEX = r"\b[\w.-]+?@\w+?\.\w+?\b"
LINKEDIN_URL = os.getenv("LINKEDIN_URL")

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

@function_tool
def validate_email(text: str) -> bool:
    match = re.search(EMAIL_REGEX, text)
    if match:
        email = match.group(0)
        return re.search(EMAIL_REGEX, email) is not None
    return False

# This guardrail checks if the email has already been recorded in the current session.
# If it has, it prevents the agent from recording it again.
# Added session logic here because the email may be submitted mid-conversation and not only as initial input.
# Although input_guardrail is designed to run before the agent's execution, this app restarts the agent on each message, so guardrail runs each time.
@input_guardrail
async def guardrail_against_spam_email(ctx, agent, message):
    session = ctx.context.get("session")
    if session and session.email_recorded:
        if re.search(EMAIL_REGEX, message):
            return GuardrailFunctionOutput(
                output_info={"reason": (
                            "Thanks! I've already recorded an email for this session and will get in touch using that. "
                            "No need to share another one. 😊\n\n"
                            "Feel free to ask me anything else about my background, skills, or projects!"
                            )},
                tripwire_triggered=True
            )
    elif session and not session.email_recorded:
        if re.search(EMAIL_REGEX, message):
            session.email_recorded = True

    return GuardrailFunctionOutput(output_info={}, tripwire_triggered=False)


class Me:

    def __init__(self) -> None:
        self.name = "Ramya Rajaram"
        self.email_recorded = False
        reader = PdfReader("uploads/resume.pdf")
        self.resumetext = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.resumetext += text

    def system_prompt(self):
            system_prompt = f"""You are acting as {self.name}. You are answering questions on {self.name}'s website, \
            particularly questions related to {self.name}'s career, background, skills and experience. \
            Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
            You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
            Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
            If you don't know the answer to any question, use your record_question tool to record the question that you couldn't answer, \
            even if it's about something trivial or unrelated to career. \
            If the user is engaging in discussion, try to steer them towards getting in touch via email; validate the email using your 'validate_email' tool. \
            If the email address is invalid, politely inform the user and ask them to provide a valid email address. \
            if the user provides a valid email address, use your 'record_email' tool to record the email address. \
            After recording the email, give an appropriate response. \
            If the user asks for your name, you can respond with your name, but do not share any personal information like phone number or address. \
            If the user asks for your email address, do not share it, but instead provide them your {LINKEDIN_URL} and ask them to contact you there. \
            """
            system_prompt += f"\n\n## LinkedIn Profile:\n{self.resumetext}\n\n"
            system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}"
            
            return system_prompt

    async def chat(self,message,history): #history not needed here as Agent takes care of it internally
        agent = Agent(name="me",instructions=self.system_prompt(),
                      model="gpt-4o-mini",tools=[record_email, record_question, validate_email],
                      input_guardrails=[guardrail_against_spam_email])
        try:
            with trace("conversational portfolio"):
                result = await Runner.run(agent,message,context={"session": self})
                return result.final_output
        except InputGuardrailTripwireTriggered as e: #to prevent tool invocation but also continue the conversation without ending it
            return f"{e.guardrail_result.output.output_info.get('reason', 'No reason provided') }"

 