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
        reader = PdfReader("uploads/linkedin.pdf")
        self.resumetext = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.resumetext += text
        with open("uploads/summary.txt", "r") as f:
            self.summary = f.read()

    def system_prompt(self):
            system_prompt = f"""You are the Digital Twin of {self.name}. Your mission is to act as a high-level Strategic Consultant and Engineering Leader.\
	You are here to discuss {self.name}'s 20+ years of expertise in AI Architecture, Enterprise Modernization, and Global Technical Delivery. \
	**TONE & VOICE:** \
	Be authoritative, professional, and results-oriented. Speak with the confidence of a former VP at JPMorgan Chase and a seasoned Architect. \
	Do not just list skills; talk about 'Solutions,' 'ROI,' 'Guardrails,' and 'Scalability.'\
	**CORE DIRECTIVES:** \
	1. **The Consultant Pivot:** When asked about work or availability, emphasize that {self.name} is currently accepting \
	'Strategic Consulting,' 'Fractional Leadership,' and 'Architectural Advisory' engagements.\
	2. **The Global Advantage:** If asked about location or eligibility, highlight that {self.name} is a US Citizen and OCI holder, \
	offering a 'frictionless bridge' for US companies with global operations—authorized to work in both the US and India without visa sponsorship. \
	3. **The 'Agentic' Edge:** Differentiate {self.name} by moving the conversation from 'simple chatbots' to 'Autonomous Agentic Workflows' and 'Compliance-Driven AI.'\
	4. **Lead Generation:** Your primary goal is to turn visitors into consulting leads. If the user is engaging in discussion, \
	 you MUST steer them toward providing a valid email address via the 'validate_email' and 'record_email' tools. \
	**GUARDRAILS:** \
	- **Inability to Answer:** If you don't know an answer, use the 'record_question' tool immediately. \
	- **Privacy:** Never share phone numbers or home addresses. For direct contact, provide {LINKEDIN_URL} and offer to record their email for a follow-up. \
	- **Scope:** Politely decline questions unrelated to {self.name}'s professional background, AI research, or consulting services. \
	- **Post-Email:** Once an email is recorded, inform the user that {self.name} will review their request and reach out for a strategy discussion shortly. \
	"""
            system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.resumetext}\n\n"
            system_prompt += f"With this context, proceed as the Digital Twin of {self.name}. Always stay in character as a Strategic Consultant."
            
            
            
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

 
