from openai import OpenAI
from pypdf import PdfReader

class Me:
    def __init__(self):
        self.openai = OpenAI()
        self.name = "Ramya"
        reader = PdfReader("uploads/linkedin.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        with open("uploads/summary.txt", "r") as f:
            self.summary = f.read()
    
    def system_prompt(self):
        system_prompt = f"""You are acting as {self.name}. You are answering questions on {self.name}'s website, \
		particularly questions related to {self.name}'s career, background, skills and experience. \
		Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
		You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
		Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
		If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
		If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. 
        """
        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}"
		
        return system_prompt
    
    def chat(self,message,history):
        messages = [{"role":"system", "content": self.system_prompt()} + history + [{"role":"user","content":message}]]
        response = self.openai.chat.completions.create(messages=messages,model="gpt-4o-mini")
        return response.choices[0].message.content

