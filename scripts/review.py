import subprocess
from langchain_core.prompts import ChatPromptTemplate
import os
import smtplib
from email.message import EmailMessage
from langchain_mistralai import ChatMistralAI
import traceback

llm = ChatMistralAI(
    model="mistral-small-2506",
    mistral_api_key=os.getenv("MISTRAL_API_KEY")
)

def getDiff():
    diff = subprocess.check_output(["git", "show"], text=True)
    print("Diff length:", len(diff))
    return diff


def send_email(html_content):
    try:
        sender = "robindutt93@gmail.com"
        receiver = "robinkumar.work01@gmail.com"
        password = os.getenv("MAIL_APP_PASSWORD")

        print("Checking password:", bool(password))

        if not password:
            raise ValueError("MAIL_APP_PASSWORD not found")

        msg = EmailMessage()
        msg['Subject'] = 'Code Review Feedback'
        msg['From'] = sender
        msg['To'] = receiver

        msg.set_content("Fallback text")
        msg.add_alternative(html_content or "<p>No content</p>", subtype='html')

        print("Connecting to Gmail...")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, password)
            print("Logged in successfully")

            smtp.send_message(msg)
            print("Email sent successfully")

    except Exception as e:
        print("Email failed")
        print(traceback.format_exc())


def main():
    print("Script started")

    diff = getDiff()
    prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a senior software engineer.

Return the code review in clean HTML format with:
- Section headings
- Bullet points
- Clear formatting
- Use <h2>, <ul>, <li>, <b> tags
- Make it visually structured and readable
- Summary
- Issues
- Suggestions
- Code Quality Score (out of 10)
- Provide update suggestions with code snippets if possible
- Use clean HTML formatting
"""),

    ("user", "Review this code and provide structured feedback:\n\n{diff}")
])
    chain = prompt | llm

    response = chain.invoke({
        "diff": diff
    })

    html = response.content
    print("LLM output preview:", html[:200])

    send_email(html)


main()